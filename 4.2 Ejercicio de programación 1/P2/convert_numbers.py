"""
Programa para convertir números de decimal a binario y hexadecimal.
"""

import sys
import time
import os


def read_data_from_file(filename):
    """Lee números de un archivo y los convierte."""
    results = []
    invalid_count = 0
    valid_count = 0

    try:
        with open(filename, 'r', encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    number = int(line)

                    binary = decimal_to_binary(number)
                    hexadecimal = decimal_to_hexadecimal(number)

                    results.append({
                        'decimal': number,
                        'binary': binary,
                        'hexadecimal': hexadecimal
                    })
                    valid_count += 1

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

    return results, invalid_count, valid_count


def decimal_to_binary(number):
    """Convierte un número decimal a binario usando complemento a dos."""
    if number == 0:
        return "0"

    if number > 0:
        binary = ""
        temp = number
        while temp > 0:
            remainder = temp % 2
            binary = str(remainder) + binary
            temp = temp // 2
        return binary

    positive = abs(number)
    bits_needed = 8
    temp = positive
    bit_count = 0

    while temp > 0:
        temp = temp // 2
        bit_count += 1

    if bit_count > 0:
        bits_needed = ((bit_count + 7) // 8) * 8

    max_value = 1
    for _ in range(bits_needed):
        max_value = max_value * 2

    twos_complement = max_value + number
    binary = ""
    temp = twos_complement
    while temp > 0:
        remainder = temp % 2
        binary = str(remainder) + binary
        temp = temp // 2

    return binary


def decimal_to_hexadecimal(number):
    """Convierte un número decimal a hexadecimal usando complemento a dos."""
    if number == 0:
        return "0"

    hex_digits = "0123456789ABCDEF"

    if number > 0:
        hexadecimal = ""
        temp = number
        while temp > 0:
            remainder = temp % 16
            hexadecimal = hex_digits[remainder] + hexadecimal
            temp = temp // 16
        return hexadecimal

    bits_needed = 40
    max_value = 1

    for _ in range(bits_needed):
        max_value = max_value * 2
    twos_complement = max_value + number

    hexadecimal = ""
    temp = twos_complement
    while temp > 0:
        remainder = temp % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        temp = temp // 16

    while len(hexadecimal) < 10:
        hexadecimal = "F" + hexadecimal
    return hexadecimal


def format_results_table(results):
    """Formatea los resultados en una tabla."""
    separator = "-" * 25
    table_lines = []
    table_lines.append(f"\n{'Decimal':<15} {'Binario':<25} {'Hexadecimal':<15}")
    table_lines.append(separator)

    for result in results:
        line = (f"{result['decimal']:<15} "
                f"{result['binary']:<25} "
                f"{result['hexadecimal']:<15}")
        table_lines.append(line)

    return table_lines


def write_results_to_file(filename, results, elapsed_time,
                          invalid_count, valid_count):
    """Escribe los resultados en un archivo."""
    try:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'w', encoding="utf-8") as file:
            file.write("=" * 25 + "\n")
            file.write("RESULTADOS DE CONVERSIÓN\n")
            file.write("=" * 25 + "\n\n")
            file.write(f"Total de números procesados: {valid_count}\n")
            file.write(f"Total de errores encontrados: {invalid_count}\n")
            file.write("-" * 25 + "\n")

            for line in format_results_table(results):
                file.write(line + "\n")

            file.write("-" * 25 + "\n")
            file.write(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 25 + "\n")
    except IOError as e:
        print(f"Error: No se pudo escribir en el archivo '{filename}': {e}")


def print_results_to_console(results, elapsed_time,
                             invalid_count, valid_count):
    """Muestra los resultados en consola."""
    print("=" * 25)
    print("RESULTADOS DE CONVERSIÓN")
    print("=" * 25)
    print(f"\nTotal de números procesados: {valid_count}")
    print(f"Total de errores encontrados: {invalid_count}")
    print("-" * 25)

    for line in format_results_table(results):
        print(line)

    print("-" * 25)
    print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
    print("=" * 25)


def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "./Resultados/ConvertionResults.txt"

    start_time = time.time()

    print(f"Leyendo datos de '{input_filename}'...\n")

    results, invalid_count, valid_count = read_data_from_file(input_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time

    if not results:
        print("Error: No se encontraron números válidos en el archivo.")
        print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
        sys.exit(1)

    print(f"Se procesaron {valid_count} números válidos.\n")
    print("Generando conversiones...\n")

    print_results_to_console(results, elapsed_time, invalid_count, valid_count)
    write_results_to_file(output_filename, results, elapsed_time,
                          invalid_count, valid_count)

    print(f"\nLos resultados se guardaron en '{output_filename}'")


if __name__ == "__main__":
    main()
