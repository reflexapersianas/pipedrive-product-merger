
def verify_circular_substituition(products: dict) -> int:
    circular_count = 0
    for product_id, product in products.items():
        if str(product['id_replacement']) in products:
            print(f"[!] Substituição circular detectada para o produto {product_id}")
            print(f"\t[-] Produto original: {product['name']}")
            print(f"\t[-] Produto substituto: {products[str(product['id_replacement'])]['name']}")
            circular_count += 1
    return circular_count


if __name__ == "__main__":
    import json

    products_path = "output/2_deal_ids.json"

    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    circular_count = verify_circular_substituition(products)
    if circular_count > 0:
        print(f"[i] {circular_count} substituições circulares detectadas.")
    else:
        print("[i] Nenhuma substituição circular detectada.")