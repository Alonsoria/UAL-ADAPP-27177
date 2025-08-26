Este archivo de python incluye la libreria de rapidfuzz y sirve para hacer comparación difusa (fuzzy matching) de cadenas de texto, es decir, comparar qué tan parecidos son dos textos aunque no sean idénticos. La primera funcion es la que conecta a la base de datos, luego viene la funcion fuzzy_match que sirve para buscar el mejor resutado, basicamente comparando el dato insertado con la base de datos, y viendo dato por dato cual es la similitud de el dato insertado con el dato extraido, al final la funcion te entrega el dato que mas similitudes tiene. La funcion llamada execute_dynamic_matching es lo que hace que la funcion de fuzzy_matching haga su trabajo, ya que esta se encarga de hacer el matching en las tablas y la fuzzy matching se encarga de ver si el dato cumple ocn las similitudes necesarias.

Variables de entorno y parametros
server
Dirección o nombre del servidor SQL de Azure al que te quieres conectar.

database
Nombre de la base de datos en el servidor SQL.

username
Usuario autorizado para acceder a la base de datos.

password
Contraseña del usuario de la base de datos.

sourceSchema
Esquema de la tabla de origen

sourceTable
Nombre de la tabla de origen desde donde se extraen los datos a comparar.

destSchema
Esquema de la tabla de destino

destTable
Nombre de la tabla de destino donde se buscarán coincidencias.

src_dest_mappings
Diccionario que mapea las columnas de la tabla de origen con las columnas de la tabla de destino para la comparación.
