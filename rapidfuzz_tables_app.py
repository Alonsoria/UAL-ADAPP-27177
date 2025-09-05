import myFuctionsModule
import pandas as pd

# -------------------------
# Configuración y ejecución
# -------------------------
params_dict = {
    "server": "localhost",
    "port": 3306,
    "username": "root",
    "password": "",
    "sourceDatabase": "crm",
    "sourceTable": "Clientes",
    "destDatabase": "dbo",
    "destTable": "Usuarios",
    "src_dest_mappings": {
        "nombre": "first_name",
        "apellido": "last_name",
        "email": "email"
    }
}
resultados = myFuctionsModule.execute_dynamic_matching(params_dict, score_cutoff=80)

user_choice = input("How would you like to display the results? Enter 'df' for DataFrame or 'dict' for dictionary: ").strip().lower()
as_dataframe = True if user_choice == 'df' else False

try:
    num_rows = int(input("How many rows do you want to display/export? Enter a number: ").strip())
except ValueError:
    num_rows = None

if num_rows == 0:
    print("El archivo está vacío. No se mostrarán ni exportarán resultados.")
else:
    myFuctionsModule.display_results(resultados, as_dataframe=as_dataframe, num_rows=num_rows)

    # Mostrar columnas disponibles y pedir selección

    columnas_disponibles = list(pd.DataFrame(resultados).columns)
    print("\nColumnas disponibles para exportar:")
    print(", ".join(columnas_disponibles))

    columnas_input = input("¿Qué columnas quieres exportar? Usa 'columna:nombreNuevo' o solo 'columna'. Ejemplo: nombre:Name,email:Email\n").strip()

    rename_map = {}
    if columnas_input:
        selected_columns = []
        for col in columnas_input.split(","):
            parts = col.strip().split(":")
            original = parts[0].strip()
            if original in columnas_disponibles:
                selected_columns.append(original)
                if len(parts) == 2:
                    rename_map[original] = parts[1].strip()
    else:
        selected_columns = None
        rename_map = None


    export_choice = input("Do you want to export the results? Enter 'csv' for CSV, 'xlsx' for Excel, or 'n' for no export: ").strip().lower()
    if export_choice == 'csv':
        filename = input("Enter the filename for the CSV (default: resultados.csv): ").strip()
        if not filename:
            filename = "resultados.csv"
        myFuctionsModule.export_results_to_csv(resultados, filename, selected_columns=selected_columns, rename_map=rename_map, num_rows=num_rows)
    elif export_choice == 'xlsx':
        filename = input("Enter the filename for the Excel file (default: resultados.xlsx): ").strip()
        if not filename:
            filename = "resultados.xlsx"
        myFuctionsModule.export_results_to_xlsx(
            resultados,
            filename,
            selected_columns=selected_columns,
            rename_map=rename_map,
            num_rows=num_rows
    )

matched, unmatched = myFuctionsModule.separate_matched_records(resultados, threshold=97.0)

print("\nMatched Records (>=97%):")
print(matched)

print("\nUnmatched Records (<97%):")
print(unmatched)

myFuctionsModule.export_matched_or_unmatched(
    resultados,
    selected_columns=selected_columns,
    rename_map=rename_map,
)

action = input("Do you want to 'export' results or 'import' a file into DB? ").strip().lower()

if action == "export":
    myFuctionsModule.export_matched_or_unmatched(
        resultados,
        selected_columns=selected_columns,
        rename_map=rename_map
    )

elif action == "import":
    file_path = input("Enter the path of the file to import (CSV/XLSX): ").strip()

    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "crm"   # <-- cámbialo si usas otra base
    }

    myFuctionsModule.import_file_and_insert_to_db(file_path, db_config)

else:
    print("Invalid choice. Exiting.")
