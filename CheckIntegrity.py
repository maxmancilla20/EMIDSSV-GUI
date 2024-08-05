import pandas as pd

# Leer los datos del archivo Excel
file_path = 'EMIDSS_V_Data.xlsx'  # Reemplaza con la ruta correcta a tu archivo Excel
data = pd.read_excel(file_path)

# Mostrar los primeros registros del DataFrame
print(data.head())

# Verificar si hay valores faltantes en los datos
print("\nValores faltantes por columna:")
print(data.isnull().sum())

# Verificar si hay valores anómalos (por ejemplo, fuera de un rango esperado)
print("\nDescripción estadística de los datos:")
print(data.describe())
