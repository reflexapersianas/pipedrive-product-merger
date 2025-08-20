from pipedrive import PipedriveAPI

MAX_NAME_LENGTH = 140

def truncate_string(text: str) -> str:
    max_length = MAX_NAME_LENGTH
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text

def fetch_deal_ids(products: dict) -> dict:
    products_ids = products.keys()
    api = PipedriveAPI()

    for idx, product_id in enumerate(products_ids):
        deals = api.get_deals_from_product(product_id)
        products[product_id]['deal_ids'] = list(map(lambda deal: deal['id'], deals))
        products[product_id]['deal_count'] = len(products[product_id]['deal_ids'])

        p = products[product_id]
        print(f"[-] ({(idx + 1):>3}/{len(products_ids)}) [ID {product_id:>3}] {truncate_string(p['name']):<{MAX_NAME_LENGTH}}: {len(p['deal_ids'])} deals")

    return products


if __name__ == "__main__":
    import json

    input_path = 'output/1_excel_data.json'
    output_path = "output/2_deal_ids.json"

    with open(input_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    data = fetch_deal_ids(products)

    with open(output_path, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\n[i] Data written to {output_path} ({len(data)} records)")
