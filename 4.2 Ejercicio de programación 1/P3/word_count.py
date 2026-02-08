"""
Programa de Conteo de Palabras
Cuenta la frecuencia de palabras distintas en un archivo de texto.
"""

import sys
import time


def normalize_word(word):
    """Normaliza una palabra removiendo puntuación y convirtiendo a minúsculas."""
    normalized = ""
    for char in word:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z' or '0' <= char <= '9':
            if 'A' <= char <= 'Z':
                normalized += chr(ord(char) + 32)
            else:
                normalized += char
    return normalized


def extract_words_from_line(line):
    """Extrae palabras de una línea separando por espacios."""
    words = []
    current_word = ""

    for char in line:
        if char in (' ', '\n', '\t'):
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += char

    if current_word:
        words.append(current_word)

    return words


def add_or_update_word(normalized_word, words_list, counts_list):
    """Agrega una palabra nueva o actualiza su contador."""
    for i, existing_word in enumerate(words_list):
        if existing_word == normalized_word:
            counts_list[i] += 1
            return

    words_list.append(normalized_word)
    counts_list.append(1)


def read_data_from_file(filename):
    """Lee palabras de un archivo y cuenta su frecuencia."""
    words_list = []
    counts_list = []
    invalid_count = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    raw_words = extract_words_from_line(line)

                    for raw_word in raw_words:
                        normalized_word = normalize_word(raw_word)
                        if normalized_word:
                            add_or_update_word(normalized_word, words_list, counts_list)

                except ValueError as e:
                    invalid_count += 1
                    print(f"Advertencia: Error en línea {line_number}: {e} - Omitido")

    except FileNotFoundError:
        print(f"Error: Archivo '{filename}' no encontrado.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permiso denegado para leer el archivo '{filename}'.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: No se pudo leer el archivo '{filename}': {e}")
        sys.exit(1)

    if invalid_count > 0:
        print(f"\nTotal de líneas con errores omitidas: {invalid_count}\n")

    # Combinar palabras y conteos en tuplas
    result = []
    for i, word in enumerate(words_list):
        result.append((word, counts_list[i]))

    return result


def sort_results(word_count_list):
    """Ordena los resultados por frecuencia (descendente) y alfabéticamente."""
    n = len(word_count_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            if word_count_list[j][1] < word_count_list[j + 1][1]:
                word_count_list[j], word_count_list[j + 1] = \
                    word_count_list[j + 1], word_count_list[j]
            elif word_count_list[j][1] == word_count_list[j + 1][1]:
                if word_count_list[j][0] > word_count_list[j + 1][0]:
                    word_count_list[j], word_count_list[j + 1] = \
                        word_count_list[j + 1], word_count_list[j]

    return word_count_list


def write_results_to_file(filename, word_count_list, elapsed_time):
    """Escribe los resultados en un archivo."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            total_words = sum(count for _, count in word_count_list)

            file.write("=" * 25 + "\n")
            file.write("RESULTADOS DE FRECUENCIA DE PALABRAS\n")
            file.write("=" * 25 + "\n\n")
            file.write(f"Total de palabras procesadas: {total_words}\n")
            file.write(f"Total de palabras distintas: {len(word_count_list)}\n")
            file.write(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n\n")
            file.write(f"{'Palabra':<30} {'Frecuencia':>10}\n")
            file.write("-" * 25 + "\n")

            for word, count in word_count_list:
                file.write(f"{word:<30} {count:>10}\n")

            file.write("-" * 25 + "\n")
            file.write(f"Total de palabras procesadas: {total_words}")
            file.write(f"\nTotal de palabras distintas: {len(word_count_list)}\n")
            file.write(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n")
            file.write("=" * 25 + "\n")
    except IOError as e:
        print(f"Error: No se pudo escribir en el archivo '{filename}': {e}")


def print_results_to_console(word_count_list, elapsed_time):
    """Muestra los resultados en consola."""
    total_words = sum(count for _, count in word_count_list)

    print("=" * 25)
    print("RESULTADOS DE FRECUENCIA DE PALABRAS")
    print("=" * 25)
    print(f"Total de palabras procesadas: {total_words}")
    print(f"\nTotal de palabras distintas: {len(word_count_list)}\n")
    print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos\n\n")
    print(f"{'Palabra':<30} {'Frecuencia':>10}")
    print("-" * 25)

    for word, count in word_count_list:
        print(f"{word:<30} {count:>10}")
    print("-" * 25)
    print(f"Total de palabras procesadas: {total_words}")
    print(f"\nTotal de palabras distintas: {len(word_count_list)}\n")
    print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
    print("-" * 25)


def main():
    """Función principal."""
    if len(sys.argv) != 2:
        print("Uso: python wordCount.py TCn.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "./Resultados/WordCountResults.txt"

    start_time = time.time()

    print(f"Leyendo datos de '{input_filename}'...\n")

    word_count_list = read_data_from_file(input_filename)

    if not word_count_list:
        print("Error: No se encontraron palabras válidas en el archivo.")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo de Ejecución: {elapsed_time:.6f} segundos")
        sys.exit(1)

    print(f"Se encontraron {len(word_count_list)} palabras distintas.\n")
    print("Ordenando resultados...\n")

    sorted_results = sort_results(word_count_list)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print_results_to_console(sorted_results, elapsed_time)
    write_results_to_file(output_filename, sorted_results, elapsed_time)

    print(f"\nLos resultados se guardaron en '{output_filename}'")


if __name__ == "__main__":
    main()
