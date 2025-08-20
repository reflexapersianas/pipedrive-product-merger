from src.pipedrive import PipedriveAPI

def update_product_names(products: dict) -> dict:
    api = PipedriveAPI()
    all_products = api.get_all_products()

    product_ids = products.keys()

    try:
        for product_id in product_ids:
            pipedrive_name = all_products[product_id]['name']
            if pipedrive_name != products[product_id]['name']:
                print(f"[!] Disparidade de nomes para o produto {product_id}")
                print(f"\t[-] Nome no Pipedrive: {pipedrive_name}")
                print(f"\t[-] Nome no arquivo: {products[product_id]['name']}")
            products[product_id]['name'] = pipedrive_name

            id_replacement = str(products[product_id]['id_replacement'])
            products[product_id]['name_replacement'] = all_products[id_replacement]['name']
    except KeyError as e:
        print(f"[!] O seguinte produto não existe no serviço: [{products[product_id]['name']}] (ID {product_id})")
        return {}

    return products


if __name__ == "__main__":
    import json

    products_path = "output/2_deal_ids.json"

    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    updated_products = update_product_names(products)

    if updated_products:
        with open(products_path, "w", encoding="utf-8") as f:
            json.dump(updated_products, f, ensure_ascii=False, indent=4)