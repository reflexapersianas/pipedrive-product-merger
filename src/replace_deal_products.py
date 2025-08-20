import sys
from pipedrive import PipedriveAPI
from colorama import Fore, Style, init
from datetime import datetime

class Tee:
    def __init__(self, *files):
        self.files = files
    
    def write(self, text):
        for file in self.files:
            file.write(text)
            file.flush()
    
    def flush(self):
        for file in self.files:
            file.flush()

init(autoreset=True)

def replace_deal_products(products: dict, attachment_map: dict) -> list:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = open(f"product_replacement_{timestamp}.log", "w", encoding="utf-8")

    original_stdout = sys.stdout
    sys.stdout = Tee(original_stdout, log_file)

    api = PipedriveAPI()
    products_ids = products.keys()
    not_processed = []
    process_count = 0
    
    for idx, product_id in enumerate(products_ids):
        product = products[product_id]
        deal_ids = product['deal_ids']
        id_replacement = product['id_replacement']
        product_name = product.get("name", "")
        new_product_name = product.get("name_replacement", "")
        params = []
        
        print(f"\n\n\n{Fore.RESET}[{(idx + 1):>3}/{len(products_ids)}]")
        print(f"{Fore.RED}[-] {product_name} ({product_id}) {Fore.RESET}")
        print(f"{Fore.GREEN}[+] {new_product_name} ({id_replacement})")
        
        for deal_id in deal_ids:
            deal_product_attachment_ids = attachment_map[product_id][str(deal_id)]
            for attachment_id in deal_product_attachment_ids:
                params.append((deal_id, attachment_id, id_replacement))
            print(f"{Fore.BLACK}  Deal {deal_id}: {len(deal_product_attachment_ids)} items")
        
        if process_count > 0:
            should_process = True
            process_count -= 1
        else:
            should_process = False
        
        if params and not should_process:
            sys.stdout = original_stdout
            answer = input(f"{Fore.YELLOW}Process this replacement?{Style.RESET_ALL} (y/n or number): ").strip().lower()
            sys.stdout = Tee(original_stdout, log_file)
            
            if answer == 'y':
                should_process = True
            elif answer == 'n':
                not_processed.append((product_id, id_replacement))
                print(f"{Fore.RED}Skipped{Style.RESET_ALL}")
                continue
            else:
                try:
                    process_count = int(answer) - 1
                    should_process = True
                except ValueError:
                    print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
                    continue
        
        if should_process:
            total = len(params)
            for i, param in enumerate(params, 1):
                api.replace_product_deal_attachment(*param)

                bar_len = 40  
                filled = int(bar_len * i / total)
                bar = '█' * filled + '░' * (bar_len - filled)

                sys.stdout.write(f"\r[{bar}] {i}/{total} ({i/total:.0%})")
                sys.stdout.flush()

            print(f"\n{Fore.GREEN}✓ Replaced{Style.RESET_ALL}")
    
    if not_processed:
        print(f"\n{Fore.YELLOW}Not processed: {len(not_processed)} products{Style.RESET_ALL}")
    
    return not_processed

if __name__ == "__main__":
    import json

    products_path = "output/2_deal_ids.json"
    attachments_path = "output/3_deal_product_attachments.json"

    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    with open(attachments_path, "r", encoding="utf-8") as f:
        attachments = json.load(f)

    replace_deal_products(products, attachments)