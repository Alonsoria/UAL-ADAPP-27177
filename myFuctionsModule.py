from rapidfuzz import process, fuzz
import mysql.connector
import pandas as pd
import os 

def connect_to_mysql(host, database, username, password, port=3306):
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port
    )
    return connection

def fuzzy_match(queryRecord, choices, score_cutoff=0):
    scorers = [fuzz.WRatio, fuzz.QRatio, fuzz.token_set_ratio, fuzz.ratio]
    processor = lambda x: str(x).lower()
    processed_query = processor(queryRecord)
    choices_data = []

    for choice in choices:
        dict_choices = dict(choice)
        queryMatch = ""
        dict_match_records = {}
        for k, v in dict_choices.items():
            if k != "DestRecordId":
                val = str(v) if v is not None else ""
                queryMatch += val
                dict_match_records[k] = v

        choices_data.append({
            'query_match': queryMatch,
            'dest_record_id': dict_choices.get('DestRecordId'),
            'match_record_values': dict_match_records
        })

    best_match = None
    best_score = score_cutoff

    for scorer in scorers:
        result = process.extractOne(
            query=processed_query,
            choices=[item['query_match'] for item in choices_data],
            scorer=scorer,
            score_cutoff=score_cutoff,
            processor=processor
        )

        if result:
            match_value, score, index = result
            if score >= best_score:
                matched_item = choices_data[index]
                best_match = {
                    'match_query': queryRecord,
                    'match_result': match_value,
                    'score': score,
                    'match_result_values': matched_item['match_record_values']
                }
        else:
            best_match = {
                'match_query': queryRecord,
                'match_result': None,
                'score': 0,
                'match_result_values': {}
            }
    return best_match

def execute_dynamic_matching(params_dict, score_cutoff=0):
    conn = connect_to_mysql(
        host=params_dict.get("server", "localhost"),
        database=params_dict.get("database", ""),
        username=params_dict.get("username", "root"),
        password=params_dict.get("password", ""),
        port=params_dict.get("port", 3306)
    )
    cursor = conn.cursor(dictionary=True)

    if 'src_dest_mappings' not in params_dict or not params_dict['src_dest_mappings']:
        raise ValueError("Debe proporcionar src_dest_mappings con columnas origen y destino")

    src_cols = ", ".join(params_dict['src_dest_mappings'].keys())
    dest_cols = ", ".join(params_dict['src_dest_mappings'].values())

    db = params_dict.get("database", "")
    sql_source = f"SELECT {src_cols} FROM {params_dict['sourceDatabase']}.{params_dict['sourceTable']}"
    sql_dest   = f"SELECT {dest_cols} FROM {params_dict['destDatabase']}.{params_dict['destTable']}"

    cursor.execute(sql_source)
    source_data = cursor.fetchall()

    cursor.execute(sql_dest)
    dest_data = cursor.fetchall()

    conn.close()

    matching_records = []

    for record in source_data:
        dict_query_records = {}
        query = ""

        for src_col in params_dict['src_dest_mappings'].keys():
            val = record.get(src_col)
            query += str(val) if val is not None else ""
            dict_query_records[src_col] = val

        fm = fuzzy_match(query, dest_data, score_cutoff)
        dict_query_records.update(fm)
        dict_query_records.update({
            'destTable': params_dict['destTable'],
            'sourceTable': params_dict['sourceTable']
        })
        matching_records.append(dict_query_records)

    return matching_records

def display_results(resultados, as_dataframe=True, selected_columns=None, num_rows=None):
    df = pd.DataFrame(resultados)

    # Filtrar por columnas elegidas
    if selected_columns:
        df = df[selected_columns]

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    if as_dataframe:
        print(df)
    else:
        print(df.to_dict(orient="records"))


def display_results(resultados, as_dataframe=True, num_columns=None, num_rows=None):
    """
    Display resultados as a DataFrame or dictionary.
    :param resultados: The result data (list of dicts or dict)
    :param as_dataframe: If True, display as DataFrame; else as dictionary
    :param num_columns: Number of columns to display (int or None for all)
    :param num_rows: Number of rows to display (int or None for all)
    """
    df = pd.DataFrame(resultados)

    if num_columns is not None and num_columns > 0:
        df = df.iloc[:, :num_columns]

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    if as_dataframe:
        print(df)
    else:
        print(df.to_dict(orient="records"))

def export_results_to_csv(resultados, filename="resultados.csv", selected_columns=None, rename_map=None, num_rows=None):
    import pandas as pd, os

    if num_rows == 0: 
        print("No se exportó CSV: número de filas = 0 (archivo vacío).")
        return

    df = pd.DataFrame(resultados)

    # --- Add Full Name column if nombre & apellido exist ---
    if "nombre" in df.columns and "apellido" in df.columns:
        df["Full Name"] = df["nombre"].astype(str) + " " + df["apellido"].astype(str)

    # --- Convert score to percentage if exists ---
    if "score" in df.columns:
        df["score"] = (df["score"] * 100).round(2).astype(str) + "%"

    if selected_columns is not None:
        if len(selected_columns) == 0:
            print("Error: No puedes exportar un archivo con 0 columnas seleccionadas.")
            return

        if "score" not in selected_columns and "score" in df.columns:
            selected_columns.append("score")

        if "Full Name" not in selected_columns and "Full Name" in df.columns:
            selected_columns.append("Full Name")

        df = df[selected_columns]

        if rename_map:
            df = df.rename(columns=rename_map)

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    if not filename.endswith(".csv"):
        filename += ".csv"

    output_dir = "archivos csv"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"Results exported to {filepath}")


def export_results_to_excel(resultados, filename="resultados.xlsx", selected_columns=None, rename_map=None, num_rows=None):
    import pandas as pd, os

    if num_rows == 0:  
        print("No se exportó Excel: número de filas = 0 (archivo vacío).")
        return

    df = pd.DataFrame(resultados)

    # --- Add Full Name column ---
    if "nombre" in df.columns and "apellido" in df.columns:
        df["Full Name"] = df["nombre"].astype(str) + " " + df["apellido"].astype(str)

    # --- Convert score to percentage (as string) ---
    if "score" in df.columns:
        df["score"] = (df["score"] * 100).round(2).astype(str) + "%"

    # --- Filter selected columns ---
    if selected_columns is not None:
        if len(selected_columns) == 0:
            print("Error: No puedes exportar un archivo con 0 columnas seleccionadas.")
            return

        if "score" not in selected_columns and "score" in df.columns:
            selected_columns.append("score")

        if "Full Name" not in selected_columns and "Full Name" in df.columns:
            selected_columns.append("Full Name")

        df = df[selected_columns]

        if rename_map:
            df = df.rename(columns=rename_map)

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    # --- Ensure filename extension ---
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # --- Ensure output dir exists ---
    output_dir = "archivos xlsx"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    try:
        df.to_excel(filepath, index=False, engine="openpyxl")  # force engine
        print(f"Results exported to {filepath}")
    except ImportError:
        print("❌ Necesitas instalar 'openpyxl'. Corre: pip install openpyxl")
    except Exception as e:
        print(f"❌ Error al exportar a Excel: {e}")
