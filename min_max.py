import pandas as pd
import numpy as np

n_datos = 5
datos = {
    'Estatura': np.round(np.random.uniform(1.50, 2.00, n_datos), 2),
    'Peso': np.round(np.random.uniform(50, 100, n_datos), 3),
    'Sexo': np.random.choice(['Hombre', 'Mujer'], n_datos),
    'Salario': np.random.randint(15000, 80000, n_datos)
}

df_original = pd.DataFrame(datos)

df_procesado = df_original.copy()

df_procesado['Hombre'] = df_procesado['Sexo'].apply(lambda x: 1 if x == 'Hombre' else 0)
df_procesado['Mujer'] = df_procesado['Sexo'].apply(lambda x: 1 if x == 'Mujer' else 0)

df_procesado = df_procesado.drop('Sexo', axis=1)

def min_max_scaling(x):
    return (x - x.min()) / (x.max() - x.min())

df_normalizado = df_procesado.apply(min_max_scaling)
df_normalizado_final = df_normalizado.drop(['Hombre', 'Mujer'], axis=1).copy()
df_normalizado_final['Sexo'] = df_normalizado['Hombre']

print("--- TABLA 1: DATOS ORIGINALES ---")
print(df_original)
print("\n" "\n")

print("--- TABLA INTERMEDIA: COLUMNAS SEPARADAS ---")
print(df_procesado)
print("\n" "\n")

print("--- TABLA 2: DATOS NORMALIZADOS (0 - 1) ---")
print(df_normalizado_final)