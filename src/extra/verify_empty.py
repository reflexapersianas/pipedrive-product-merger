from src.pipedrive import PipedriveAPI
from colorama import Fore, Style, init

init(autoreset=True)

def verify_empty_products(products: dict) -> dict:
    api = PipedriveAPI()

    not_empty_products = {}

    for product_id, product in products.items():
        name = product.get('name', 'Unknown Product')
        if api.is_product_empty(product_id):
            print(f"{Fore.GREEN}[-] Produto vazio: {product_id} - {name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[+] Produto não vazio: {product_id} - {name}{Style.RESET_ALL}")
            not_empty_products[product_id] = product

    return not_empty_products


if __name__ == "__main__":
    import json

    products_path = "output/2_deal_ids copy.json"

    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    not_empty_products = verify_empty_products(products)
    print(f"\n\n")

    if (len(not_empty_products) > 0):
        for product_id, product in not_empty_products.items():
            print(f"{Fore.RED}[+] Produto não vazio: {product_id} - {product['name']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[-] Todos os produtos estão vazios.{Style.RESET_ALL}")