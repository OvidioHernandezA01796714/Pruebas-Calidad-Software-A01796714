import json
import sys
import time


def load_file_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def build_price_catalogue(data):
    prices = {}
    for item in data:
        try:
            name = item.get('title')
            price = item.get('price')
            if name and price is not None:
                prices[name] = float(price)
        except (ValueError, TypeError) as e:
            print(f"Error al procesar el artículo: {item} - {e}")
    return prices


def compute_sales(catalogue, sales_data):
    total = 0.0
    results = []

    for sale in sales_data:
        try:
            product = sale.get('Product')
            quantity = sale.get('Quantity')

            if product is None or quantity is None:
                print(f"Error, valores faltantes. {sale}")
                continue

            quantity = int(quantity)

            if product not in catalogue:
                print(f"Producto no encontrado en el catálogo: '{product}' ")
                continue

            price = catalogue[product]
            subtotal = price * quantity
            total += subtotal
            results.append((product, quantity, price, subtotal))

        except (ValueError, TypeError) as e:
            print(f"Error al procesar: {sale} - {e}")

    return total, results


def format_output(total, elapsed_time, results):
    output = []
    output.append("COSTO TOTAL DE VENTAS")
    output.append("=" * 25)
    output.append("")

    for product, qty, price, subtotal in results:
        line = f"{product}: {qty} x ${price:.2f} = ${subtotal:.2f}"
        output.append(line)
        output.append("-" * 55)

    output.append("")
    output.append("=" * 25)
    output.append(f"TOTAL: ${total:.2f}")
    output.append("-" * 25)
    output.append(f"Tiempo: {elapsed_time:.4f} segundos")
    output.append("=" * 25)

    return '\n'.join(output)


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    try:
        catalogue_data = load_file_json(catalogue_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar el JSON de catálogo: {e}")
        sys.exit(1)

    try:
        sales_data = load_file_json(sales_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al procesar el JSON de ventas: {e}")
        sys.exit(1)

    catalogue = build_price_catalogue(catalogue_data)
    total, results = compute_sales(catalogue, sales_data)

    elapsed_time = time.time() - start_time

    output = format_output(total, elapsed_time, results)

    print(output)

    with open('./Resultados/SalesResults.txt', 'w', encoding='utf-8') as file:
        file.write(output)


if __name__ == '__main__':
    main()