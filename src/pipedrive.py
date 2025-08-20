import os
import requests


class PipedriveAPI:
    _PAGE_LIMIT = 500

    def __init__(self):
        pipedrive_subdomain = os.getenv("PIPE_SUBDOMAIN")

        if not pipedrive_subdomain:
            print("The environment variable PIPE_SUBDOMAIN is not set.")
            print("[i] Your Pipedrive subdomain is the part before '.pipedrive.com' in your Pipedrive URL.")
            pipedrive_subdomain = input("Please enter your Pipedrive subdomain: ").strip()
            os.environ["PIPE_SUBDOMAIN"] = pipedrive_subdomain  # save for current session

        self.base_url = f"https://{pipedrive_subdomain}.pipedrive.com/api"
        self.api_token = os.getenv("PIPE_TOKEN")

        if not self.api_token:
            print("The environment variable PIPE_TOKEN is not set.")
            print("[i] Your Pipedrive API token can be found in your Pipedrive account settings.")
            self.api_token = input("Please enter your Pipedrive API token: ").strip()
            os.environ["PIPE_TOKEN"] = self.api_token  # save for current session

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            'x-api-token': self.api_token
        })
    
    def request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        
        if method == 'GET':
            response = self.session.get(url, params=data)
        elif method == 'PATCH':
            response = self.session.patch(url, json=data)
        elif method == 'DELETE':
            response = self.session.delete(url)
        else:
            raise ValueError("Invalid HTTP method specified. Available methods are [GET, POST, PATCH]")
        
        response.raise_for_status()
        return response.json()
    
    def get(self, url, params=None):
        return self.request(url, data=params)

    def patch(self, url, data=None):
        return self.request(url, method='PATCH', data=data)
    
    def delete(self, url):
        return self.request(url, method='DELETE')

    def get_deals_from_product_paginated(self, product_id: int, page: int) -> list:
        response = self.get(f"/v1/products/{product_id}/deals", 
            { 
                'limit': self._PAGE_LIMIT, 
                'start': page * self._PAGE_LIMIT
            }
        )

        if (response.get('success', False) == True):
            has_more_data = response['additional_data']['pagination']['more_items_in_collection']
            data = response.get('data')
            data = data if isinstance(data, list) else []
            return (data, has_more_data)
        else:
            data = response.get('data', {})
            message = data.get('message', 'Unknown error')
            code = data.get('code', 'Unknown code')
            raise Exception(f"Error fetching deals for product {product_id}: {message} (Code: {code})")
        
    def get_deals_from_product(self, product_id: int) -> list:
        page = 0
        deals = []
        has_more_data = True

        while has_more_data and page < 5:  # max 5 tries, 2500 deals
            data, has_more_data = self.get_deals_from_product_paginated(product_id, page)
            deals.extend(data)
            page += 1
        if page >= 5:
            raise Exception(f"Error fetching deals for product {product_id}: Too many pages")

        return deals
    
    def is_product_empty(self, product_id: int) -> bool:
        return not bool(self.get_deals_from_product(product_id))
    
    def get_products_from_deal(self, deal_id: int) -> list:
        response = self.get(f"v2/deals/{deal_id}/products", { 'limit': self._PAGE_LIMIT })

        if (response.get('success', False) == True):
            has_more_data = response['additional_data']['next_cursor'] is not None
            if (has_more_data):
                raise NotImplementedError("Pagination is not implemented for this endpoint")
            data = response.get('data')
            return data if isinstance(data, list) else []

    def get_product_deal_attachments(self, product_id: int, deal_id: int) -> dict:
        products = self.get_products_from_deal(deal_id)

        def is_same_product_and_deal(product):
            return product['product_id'] == int(product_id) and product['deal_id'] == int(deal_id)

        filtered_products = list(filter(is_same_product_and_deal, products))

        return [att['id'] for att in filtered_products]
    
    def replace_product_deal_attachment(self, deal_id: int, attachment_id: int, new_product_id: int) -> dict:
        return self.patch(
            f"v2/deals/{deal_id}/products/{attachment_id}", 
            { 
                'product_id': new_product_id,
                'product_variation_id': None
            }
        )
    
    def get_all_products(self) -> dict:
        response = self.get("v2/products", { 'limit': self._PAGE_LIMIT })
        return {str(product.get("id")): product for product in response.get('data', [])}

    def delete_product(self, product_id: int) -> bool:
        response = self.delete(f"v2/products/{product_id}")
        return response.get('success', False)
    
    def update_product(self, product_id: int, body: dict) -> dict:
        response = self.patch(f"v2/products/{product_id}", body)
        if response.get('success', False):
            return response.get('data', {})
        else:
            raise Exception(f"Error updating product {product_id}: {response.get('message', 'Unknown error')}")
        
    def update_product_name(self, product_id: int, name: str) -> dict:
        if not name or not name.strip() or not isinstance(name, str):
            raise ValueError("Invalid product name")
        return self.update_product(product_id, { 'name': name })