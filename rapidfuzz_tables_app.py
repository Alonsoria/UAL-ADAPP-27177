import myFuctionsModule
import pandas as pd  # Add pandas import

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

# Convert resultados to DataFrame and display
df = pd.DataFrame(resultados)
print(df)
