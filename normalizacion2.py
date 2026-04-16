import pandas as pd
import numpy as np

n_datos = 30
df_original = pd.DataFrame({
    'Estatura': np.round(np.random.uniform(1.50, 2.00, n_datos), 2),
    'Peso': np.round(np.random.uniform(50, 100, n_datos), 3),
    'Sexo': np.random.choice(['Hombre', 'Mujer'], n_datos),
    'Salario': np.random.randint(15000, 80000, n_datos),
    'paga': np.random.choice(['si', 'no'], n_datos)
})


def pedir(mensaje, tipo=float, opciones=None):
    while True:
        valor = input(mensaje).strip()
        if opciones:
            valor_l = valor.lower()
            if valor_l in opciones:
                return opciones[valor_l]
            print("Valor inválido.")
            continue
        try:
            return tipo(valor)
        except ValueError:
            print("Valor inválido.")


def minmax(columna):
    rango = columna.max() - columna.min()
    return np.zeros(len(columna)) if rango == 0 else (columna - columna.min()) / rango


def k_impar(total):
    if total <= 0:
        return 1
    impares = np.arange(1, total + 1, 2)
    k = int(np.random.choice(impares))
    if k % 2 == 0:
        k = k - 1 if k > 1 else 1
    return k


print("--- CAPTURA DE DATOS DEL USUARIO ---")
registro_usuario = {
    'Estatura': pedir("Estatura: ", float),
    'Peso': pedir("Peso: ", float),
    'Sexo': pedir("Sexo (Hombre/Mujer): ", str, {'hombre': 'Hombre', 'mujer': 'Mujer'}),
    'Salario': pedir("Salario: ", int),
    'paga': np.nan
}

df_con_usuario = pd.concat([df_original, pd.DataFrame([registro_usuario])], ignore_index=True)
indice_usuario = len(df_con_usuario) - 1

df_procesado = pd.concat(
    [
        df_con_usuario[['Estatura', 'Peso', 'Salario']],
        pd.get_dummies(df_con_usuario['Sexo'])[['Hombre', 'Mujer']].astype(int)
    ],
    axis=1
)

df_normalizado = df_procesado.apply(minmax)

columnas_distancia = ['Estatura', 'Peso', 'Salario', 'Hombre', 'Mujer']
matriz = df_normalizado[columnas_distancia].to_numpy(dtype=float)
usuario = matriz[indice_usuario]
matriz_sin_usuario = np.delete(matriz, indice_usuario, axis=0)
distancias = np.sqrt(np.sum((matriz_sin_usuario - usuario) ** 2, axis=1))

df_distancias_ordenado = pd.DataFrame({
    'Indice': [i for i in range(len(df_original))],
    'Distancia': distancias,
    'paga': df_original['paga'].values
}).sort_values('Distancia').reset_index(drop=True)

k = k_impar(len(df_original))
vecinos = df_distancias_ordenado.head(k)
muestra_prueba = vecinos[['Indice', 'Distancia', 'paga']].join(
    df_original[['Estatura', 'Peso', 'Sexo', 'Salario']],
    on='Indice'
)[['Indice', 'Estatura', 'Peso', 'Sexo', 'Salario', 'paga', 'Distancia']]
conteo_si = (vecinos['paga'] == 'si').sum()
conteo_no = (vecinos['paga'] == 'no').sum()
decision_credito = 'SI se le da crédito' if conteo_si > conteo_no else 'NO se le da crédito'

df_normalizado_sin_paga = df_normalizado.copy()

print("--- TABLA 1: DATOS ORIGINALES ---")
print(df_original)
print("\n" "\n")

print("--- TABLA INTERMEDIA: COLUMNAS SEPARADAS ---")
print(df_procesado)
print("\n" "\n")

print("--- TABLA 2: DATOS NORMALIZADOS (0 - 1) CON USUARIO (SIN COLUMNA paga) ---")
print(df_normalizado_sin_paga)
print("\n" "\n")

print("--- DISTANCIAS DEL USUARIO VS DEMÁS REGISTROS (MENOR A MAYOR) ---")
print(df_distancias_ordenado)
print("\n" "\n")

print(f"--- VECINOS TOMADOS (k={k}) ---")
print(vecinos)
print("\n" "\n")

print("--- DECISIÓN FINAL ---")
print(f"Vecinos con paga='si': {conteo_si}")
print(f"Vecinos con paga='no': {conteo_no}")
print(decision_credito)