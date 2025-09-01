import myFuctionsModule
import pandas as pd

def display_results(resultados, as_dataframe=True):
    """
    Display resultados as a DataFrame or dictionary.
    :param resultados: The result data (list of dicts or dict)
    :param as_dataframe: If True, display as DataFrame; else as dictionary
    """
    if as_dataframe:
        df = pd.DataFrame(resultados)
        print(df)
    else:
        print(resultados)

def export_results_to_csv(resultados, filename="resultados.csv"):
    """
    Export resultados to a CSV file.
    :param resultados: The result data (list of dicts)
    :param filename: Name of the CSV file
    """
    df = pd.DataFrame(resultados)
    df.to_csv(filename, index=False)
    print(f"Results exported to {filename}")

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

# Ask user for preferred display format
user_choice = input("How would you like to display the results? Enter 'df' for DataFrame or 'dict' for dictionary: ").strip().lower()
as_dataframe = True if user_choice == 'df' else False

# Display the results in the chosen format
display_results(resultados, as_dataframe=as_dataframe)

# Ask user if they want to export to CSV
export_choice = input("Do you want to export the results to a CSV file? (y/n): ").strip().lower()
if export_choice == 'y':
    filename = input("Enter the filename for the CSV (default: resultados.csv): ").strip()
    if not filename:
        filename = "resultados.csv"
    export_results_to_csv(resultados, filename)