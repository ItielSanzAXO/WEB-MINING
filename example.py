import random
import pandas as pd

pd.set_option('display.max_columns', None)
def generar_datos(n):
    sexos = ["Mujer", "Hombre"]
    estados = ["Soltero", "Casado", "Divorciado", "Viudo"]
    paga_opciones = ["Si", "No"]
    datos = []
    for _ in range(n):
        persona = {
            "Sexo": random.choice(sexos),
            "Edad": random.randint(18, 70),
            "EstadoCivil": random.choice(estados),
            "Peso": random.randint(45, 110),
            "Estatura": random.randint(150, 200),
            "Salario": random.randint(5000, 50000),
            "Paga": random.choice(paga_opciones)
        }
        datos.append(persona)
    return pd.DataFrame(datos)


# --- 2. Normalización min-max ---
def normalizar(df, columnas):
    df_norm = df.copy()
    for col in columnas:
        minimo = df[col].min()
        maximo = df[col].max()
        if maximo != minimo:
            df_norm[col] = (df[col] - minimo) / (maximo - minimo)
        else:
            df_norm[col] = 0
    return df_norm


# --- 3. Codificación de categorías ---
def codificar(df):
    df_encoded = df.copy()
    df_encoded["Sexo"] = df_encoded["Sexo"].map({"Mujer": 0, "Hombre": 1})
    df_encoded["EstadoCivil"] = df_encoded["EstadoCivil"].map(
        {"Soltero": 0, "Casado": 1, "Divorciado": 2, "Viudo": 3}
    )
    df_encoded["Paga"] = df_encoded["Paga"].map({"No": 0, "Si": 1})
    return df_encoded


# --- 4. Distancia Euclidiana ---
def distancia_euclidiana(fila1, fila2, columnas):
    suma = 0
    for col in columnas:
        suma += (fila1[col] - fila2[col]) ** 2
    return suma ** 0.5


# --- 5. Programa principal ---
if __name__ == "__main__":
    n = int(input("¿Cuántos registros deseas generar?: "))
    df = generar_datos(n)

    print("\n📋 Datos generados:")
    print(df)

    # --- Preguntar datos al usuario ---
    print("\n👤 Ingresa tus datos:")
    sexo = input("Sexo (Mujer/Hombre): ").strip().capitalize()
    estado = input("Estado civil (Soltero/a, Casado/a, Divorciado/a, Viudo/a): ").strip().capitalize()
    if "solter" in estado.lower():
        estado = "Soltero"
    elif "casad" in estado.lower():
        estado = "Casado"
    elif "divorciad" in estado.lower():
        estado = "Divorciado"
    elif "viud" in estado.lower():
        estado = "Viudo"

    edad = int(input("Edad: "))
    peso = int(input("Peso (kg): "))
    estatura = int(input("Estatura (cm): "))
    salario = int(input("Salario: "))
    paga = input("¿Paga? (Si/No): ").strip().capitalize()

    usuario = pd.DataFrame([{
        "Sexo": sexo,
        "Edad": edad,
        "EstadoCivil": estado,
        "Peso": peso,
        "Estatura": estatura,
        "Salario": salario,
        "Paga": paga
    }])

    # --- Unir usuario con los datos ---
    df_total = pd.concat([df, usuario], ignore_index=True)

    # Codificar categorías
    df_encoded = codificar(df_total)

    # Normalizar todo
    columnas_num = ["Sexo", "Edad", "EstadoCivil", "Peso", "Estatura", "Salario", "Paga"]
    df_norm = normalizar(df_encoded, columnas_num)

    print("\n📊 Datos normalizados (incluyendo al usuario):")
    print(df_norm)

    # Calcular distancias
    usuario_norm = df_norm.iloc[-1]
    distancias = []
    similitudes = []
    distancia_max = (len(columnas_num)) ** 0.9  # distancia máxima posible

    for i in range(len(df_norm) - 1):
        d = distancia_euclidiana(df_norm.iloc[i], usuario_norm, columnas_num)
        distancias.append(d)
        similitud = (1 - d / distancia_max) * 100
        similitudes.append(similitud)

    # Agregar distancias y similitudes al DF original
    df["DistanciaUsuario"] = distancias
    df["Similitud(%)"] = similitudes

    # Lista de todas las columnas a mostrar
    columnas_a_mostrar = ["Sexo", "Edad", "EstadoCivil", "Peso", "Estatura", "Salario", "Paga", "DistanciaUsuario",
                          "Similitud(%)"]

    # --- Mostrar resultados ordenados y con todas las columnas ---
    print("\n📊 Distancias y similitudes (ordenadas por cercanía):")
    print(df[columnas_a_mostrar].sort_values(by="DistanciaUsuario"))

    # --- Mostrar la persona más parecida ---
    idx_min = df["DistanciaUsuario"].idxmin()
    print("\n✅ La persona más parecida al usuario es:")
    print(df.loc[idx_min, columnas_a_mostrar])