import math

def calcular_promedio(valores):
	return sum(valores) / len(valores)

def calcular_varianza(valores, promedio):
	return sum((valor - promedio) ** 2 for valor in valores) / len(valores)

def calcular_desviacion_estandar(varianza):
	return math.sqrt(varianza)

def calcular_umbral_deteccion(promedio, desviacion_estandar, factor_umbral):
	return promedio + (factor_umbral * desviacion_estandar)

def evaluar_transaccion(historial_aprobadas, cantidad_a_evaluar, factor_umbral):
	promedio = calcular_promedio(historial_aprobadas)
	varianza = calcular_varianza(historial_aprobadas, promedio)
	desviacion_estandar = calcular_desviacion_estandar(varianza)
	umbral = calcular_umbral_deteccion(promedio, desviacion_estandar, factor_umbral)

	aprobada = cantidad_a_evaluar <= umbral

	return {
		"promedio": promedio,
		"varianza": varianza,
		"desviacion_estandar": desviacion_estandar,
		"umbral": umbral,
		"aprobada": aprobada,
	}

def pedir_float_positivo(mensaje):
	while True:
		entrada = input(mensaje).strip()
		try:
			valor = float(entrada)
			if valor < 0:
				print("Ingresa un numero mayor o igual a 0.")
				continue
			return valor
		except ValueError:
			print("Entrada invalida. Ingresa un numero valido.")

def pedir_si_no(mensaje):
	while True:
		opcion = input(mensaje).strip().lower()
		if opcion in ("s", "si"):
			return True
		if opcion in ("n", "no"):
			return False
		print("Respuesta invalida. Escribe 's' para si o 'n' para no.")

def main():
	historial_aprobadas = [150.0, 250.0, 350.0]
	print("PROYECTO: Deteccion de anomalias")
	print(f"Historial inicial de aprobadas: {historial_aprobadas}")

	factor_umbral = pedir_float_positivo("Ingresa el factor de umbral (ejemplo 1.5): ")

	while True:
		cantidad_a_evaluar = pedir_float_positivo("Ingresa la cantidad a evaluar: ")

		resultado = evaluar_transaccion(
			historial_aprobadas, cantidad_a_evaluar, factor_umbral
		)

		print("\n--- Resultado del analisis ---")
		print(f"Promedio actual de aprobadas: {resultado['promedio']:.2f}")
		print(f"Varianza actual: {resultado['varianza']:.2f}")
		print(f"Desviacion estandar actual: {resultado['desviacion_estandar']:.2f}")
		print(f"Umbral de deteccion calculado: {resultado['umbral']:.2f}")

		if resultado["aprobada"]:
			print("Transaccion APROBADA")
			historial_aprobadas.append(cantidad_a_evaluar)
			nuevo_promedio = calcular_promedio(historial_aprobadas)
			print(
				"La cantidad aprobada se agrego al historial para futuras evaluaciones."
			)
			print(f"Nuevo promedio con la compra aprobada: {nuevo_promedio:.2f}")
		else:
			print("Transaccion RECHAZADA")
			print("La cantidad rechazada NO se agrega al historial de aprobadas.")

		print(f"Historial actual de aprobadas: {historial_aprobadas}")

		continuar = pedir_si_no("\nDeseas evaluar otra transaccion? (s/n): ")
		if not continuar:
			print("Programa finalizado.")
			break


if __name__ == "__main__":
	main()
