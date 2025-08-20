from src.pipedrive import PipedriveAPI
from src.utils.truncate_string import truncate_string, MAX_NAME_LENGTH

def update_pipedrive_product_names(products: dict) -> None:
    api = PipedriveAPI()
    all_products = api.get_all_products()

    products_to_replace = []

    for product_id, product in products.items():
        try:
            pipedrive_name = all_products[product_id]['name']
            if pipedrive_name != product['name']:
                print(f"[!] Substituição (ID {product_id:<3}) [{truncate_string(pipedrive_name):<{MAX_NAME_LENGTH}}] -> [{truncate_string(product['name']):<{MAX_NAME_LENGTH}}] encontrada.")
                products_to_replace.append((product_id, product['name']))
        except KeyError as e:
            continue

    for product_id, new_name in products_to_replace:
        new_product = api.update_product_name(product_id, new_name)
        if new_product:
            if new_product.get('name') == new_name:
                print(f"[+] Produto (ID {product_id:<3}) [{truncate_string(new_name):<{MAX_NAME_LENGTH}}] atualizado com sucesso.")
            else:
                print(f"[x] Produto {product_id} era pra ser [{truncate_string(new_name):<{MAX_NAME_LENGTH}}], mas retornou [{truncate_string(new_product.get('name', '')):<{MAX_NAME_LENGTH}}].")
        else:
            print(f"[x] Erro ao atualizar produto (ID {product_id:<3}) [{truncate_string(new_name):<{MAX_NAME_LENGTH}}].")


if __name__ == "__main__":
    import json

    products_path = "output/0_excel_data.json"

    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    update_pipedrive_product_names(products)