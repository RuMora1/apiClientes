import pyodbc

#'DESKTOP-RJ8E821/SQLSERVER'
# Cambia estos valores según tu entorno
server = 'localhost'  # o 'NOMBREPC\\SQLEXPRESS' si usas una instancia específica
database = 'DB_CLIENTES'  # tu base de datos

try:
    conexion = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    print("✅ Conexión exitosa a SQL Server con autenticación de Windows.")
    conexion.close()
except Exception as e:
    print("❌ Error al conectar:", e)