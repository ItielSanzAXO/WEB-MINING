import pandas as pd
import numpy as np

np.random.seed(42)

n_datos = 5
datos = {
    'Estatura': np.random.uniform(1.50, 2.00, n_datos),
    'Peso': np.random.uniform(50, 100, n_datos),
    'Sexo': np.random.choice(['Hombre', 'Mujer'], n_datos),
    'Salario': np.random.uniform(15000, 80000, n_datos)
}

df_original = pd.DataFrame(datos)

df_procesado = df_original.copy()

df_procesado['Hombre'] = df_procesado['Sexo'].apply(lambda x: 1 if x == 'Hombre' else 0)
df_procesado['Mujer'] = df_procesado['Sexo'].apply(lambda x: 1 if x == 'Mujer' else 0)

df_procesado = df_procesado.drop('Sexo', axis=1)

def min_max_scaling(column):
    return (column - column.min()) / (column.max() - column.min())

df_normalizado = df_procesado.apply(min_max_scaling)

print("--- TABLA 1: DATOS ORIGINALES ---")
print(df_original)
print("\n" + "="*50 + "\n")

print("--- TABLA INTERMEDIA: COLUMNAS PREPARADAS ---")
print("(Nota: 'Sexo' se expandió a 'Hombre' y 'Mujer')")
print(df_procesado)
print("\n" + "="*50 + "\n")

print("--- TABLA 2: DATOS NORMALIZADOS (0 - 1) ---")
print(df_normalizado)