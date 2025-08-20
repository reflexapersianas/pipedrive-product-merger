from pipedrive import PipedriveAPI
from utils.truncate_string import truncate_string, MAX_NAME_LENGTH

def fetch_product_deal_attachments(products: dict) -> dict:
    api = PipedriveAPI()
    products_ids = products.keys()

    for idx, product_id in enumerate(products_ids):
        deal_ids = products[product_id]['deal_ids']
        deal_attachments = {}

        print(f"[-] ({(idx + 1):>3}/{len(products_ids)}) [ID {product_id:>3}] {truncate_string(products[product_id]['name']):<{MAX_NAME_LENGTH}}: Extracting attachments to Deals...")

        for deal_id in deal_ids:
            product_deal_attachments = api.get_product_deal_attachments(product_id, deal_id)
            deal_attachments[deal_id] = product_deal_attachments
            print(f"\t[-] [Deal {deal_id}] Found {len(product_deal_attachments)} attachments: {product_deal_attachments}")

        products[product_id] = deal_attachments

    return products


if __name__ == "__main__":
    import json

    input_path = 'output/2_deal_ids.json'
    output_path = "output/3_deal_product_attachments.json"

    with open(input_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    data = fetch_product_deal_attachments(products)

    with open(output_path, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\n[i] Data written to {output_path} ({len(data)} records)")
