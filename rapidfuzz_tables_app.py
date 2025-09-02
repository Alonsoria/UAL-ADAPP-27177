import myFuctionsModule
import pandas as pd
import os  # 👈 necesario para manejar carpetas

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


def export_results_to_csv(resultados, filename="resultados.csv", num_columns=None, num_rows=None):
    if num_rows == 0:  # 👈 validación
        print("⚠ No se exportó CSV: número de filas = 0 (archivo vacío).")
        return

    df = pd.DataFrame(resultados)

    if num_columns is not None and num_columns > 0:
        df = df.iloc[:, :num_columns]

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    if not filename.endswith(".csv"):
        filename += ".csv"

    # 👇 Crear carpeta "archivos csv" si no existe
    output_dir = "archivos csv"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    df.to_csv(filepath, index=False)
    print(f"Results exported to {filepath}")


def export_results_to_excel(resultados, filename="resultados.xlsx", num_columns=None, num_rows=None):
    if num_rows == 0:  # 👈 validación
        print("⚠ No se exportó Excel: número de filas = 0 (archivo vacío).")
        return

    df = pd.DataFrame(resultados)

    if num_columns is not None and num_columns > 0:
        df = df.iloc[:, :num_columns]

    if num_rows is not None and num_rows > 0:
        df = df.head(num_rows)

    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # 👇 Crear carpeta "archivos xlsx" si no existe
    output_dir = "archivos xlsx"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    try:
        df.to_excel(filepath, index=False)
        print(f"Results exported to {filepath}")
    except ImportError:
        print("Error: Necesitas instalar 'openpyxl' para exportar a Excel. Usa: pip install openpyxl")


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

# Preguntar formato de visualización
user_choice = input("How would you like to display the results? Enter 'df' for DataFrame or 'dict' for dictionary: ").strip().lower()
as_dataframe = True if user_choice == 'df' else False

# Preguntar número de filas
try:
    num_rows = int(input("How many rows do you want to display/export? Enter a number or 0 for all: ").strip())
except ValueError:
    num_rows = None

# ⚠ Validación extra antes de continuar
if num_rows == 0:
    print("El archivo está vacío. No se mostrarán ni exportarán resultados.")
else:
    # Mostrar resultados
    display_results(resultados, as_dataframe=as_dataframe, num_rows=num_rows)

    # Preguntar si exportar
    export_choice = input("Do you want to export the results? Enter 'csv' for CSV, 'xlsx' for Excel, or 'n' for no export: ").strip().lower()
    if export_choice == 'csv':
        filename = input("Enter the filename for the CSV (default: resultados.csv): ").strip()
        if not filename:
            filename = "resultados.csv"
        export_results_to_csv(resultados, filename, num_rows=num_rows)
    elif export_choice == 'xlsx':
        filename = input("Enter the filename for the Excel file (default: resultados.xlsx): ").strip()
        if not filename:
            filename = "resultados.xlsx"
        export_results_to_excel(resultados, filename, num_rows=num_rows)