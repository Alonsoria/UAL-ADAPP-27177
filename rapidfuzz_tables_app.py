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
print(display_results(resultados, as_dataframe=as_dataframe))