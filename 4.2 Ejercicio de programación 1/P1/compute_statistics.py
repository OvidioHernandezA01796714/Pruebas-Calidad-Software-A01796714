"""
Calculadora de Estadísticas
Este programa calcula promedio, mediana, moda, 
desviación estándar y varianza.

Uso:
    python computeStatistics.py TCn.txt
"""

import sys
import time


def read_data_from_file(filename):
    """
    Lee números de un archivo y descarta datos inválidos.
    """
    data = []
    invalid_count = 0

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    number = float(line)
                    data.append(number)
                except ValueError:
                    invalid_count += 1
                    print(f"Advertencia: Dato inválido en línea {line_number}: "
                          f"'{line}' - Omitido")

    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: No se pudo leer el archivo '{filename}': {e}")
        sys.exit(1)

    if invalid_count > 0:
        print(f"\nTotal de entradas inválidas omitidas: {invalid_count}\n")

    return data


def calculate_mean(data):
    """Calcula el promedio."""
    if not data:
        return 0

    total = 0
    for value in data:
        total += value

    return total / len(data)


def calculate_median(data):
    """Calcula la mediana."""
    if not data:
        return 0

    sorted_data = data.copy()
    n = len(sorted_data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_data[j] > sorted_data[j + 1]:
                sorted_data[j], sorted_data[j + 1] = \
                    sorted_data[j + 1], sorted_data[j]

    middle = n // 2

    if n % 2 == 0:
        median = (sorted_data[middle - 1] + sorted_data[middle]) / 2
    else:
        median = sorted_data[middle]

    return median


def calculate_mode(data):
    """Calcula la moda."""
    if not data:
        return None

    frequency = {}
    for value in data:
        if value in frequency:
            frequency[value] += 1
        else:
            frequency[value] = 1

    max_frequency = 0
    for count in frequency.values():
        max_frequency = max(max_frequency, count)

    if max_frequency == 1:
        return None

    for value, count in frequency.items():
        if count == max_frequency:
            return value
    return None


def calculate_variance(data, mean):
    """Calcula la varianza."""
    if not data:
        return 0

    sum_squared_diff = 0
    for value in data:
        diff = value - mean
        sum_squared_diff += diff * diff

    return sum_squared_diff / (len(data) - 1)


def calculate_standard_deviation(data, mean):
    """Calcula la desviación estándar poblacional."""
    if not data:
        return 0

    sum_squared_diff = 0
    for value in data:
        sum_squared_diff += (value - mean) ** 2

    variance = sum_squared_diff / len(data)
    return variance ** 0.5


def write_results_to_file(filename, results, elapsed_time):
    """Escribe los resultados en un archivo."""
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write("=" * 25 + "\n")
            file.write("RESULTADOS DE ESTADÍSTICAS\n")
            file.write("=" * 25 + "\n\n")
            file.write(f"Cantidad:            {results['count']}\n")
            file.write(f"Promedio:            {results['mean']:.6f}\n")
            file.write(f"Mediana:             {results['median']:.6f}\n")
            file.write(f"Moda:                {results['mode']}\n")
            file.write(f"Varianza:            {results['variance']:.6f}\n")
            file.write(f"Desviación Estándar: {results['std_dev']:.6f}\n\n")
            file.write(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 25 + "\n")
    except IOError as e:
        print(f"Error: No se pudo escribir en el archivo '{filename}': {e}")


def print_results_to_console(results, elapsed_time):
    """Muestra los resultados en consola."""
    print("=" * 25)
    print("RESULTADOS DE ESTADÍSTICAS")
    print("=" * 25)
    print(f"Cantidad:            {results['count']}")
    print(f"Promedio:            {results['mean']:.6f}")
    print(f"Mediana:             {results['median']:.6f}")
    print(f"Moda:                {results['mode']}")
    print(f"Varianza:            {results['variance']:.6f}")
    print(f"Desviación Estándar: {results['std_dev']:.6f}")
    print()
    print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
    print("=" * 25)


def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py TCn.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "./Resultados/StatisticsResults.txt"

    start_time = time.time()

    print(f"Leyendo datos de '{input_filename}'...\n")
    data = read_data_from_file(input_filename)

    if not data:
        print("Error: No se encontraron datos válidos en el archivo.")
        sys.exit(1)

    print(f"Se cargaron {len(data)} números válidos.\n")

    print("Calculando estadísticas...\n")

    mean = calculate_mean(data)
    median = calculate_median(data)
    mode = calculate_mode(data)
    variance = calculate_variance(data, mean)
    std_dev = calculate_standard_deviation(data, mean)

    end_time = time.time()
    elapsed_time = end_time - start_time

    results = {
        'count': len(data),
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance,
        'std_dev': std_dev
    }

    print_results_to_console(results, elapsed_time)
    write_results_to_file(output_filename, results, elapsed_time)

    print(f"\nLos resultados se guardaron en '{output_filename}'")


if __name__ == "__main__":
    main()
