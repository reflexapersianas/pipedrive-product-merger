import pandas as pd
import sys, json

from src.utils.truncate_string import truncate_string, MAX_NAME_LENGTH


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "output/2_deal_ids.json"

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        df = pd.DataFrame.from_dict(data, orient='index')

        df = df.rename(columns={
            'name': 'Nome',
            'id_replacement': 'ID Substituição',
            'name_replacement': 'Nome Substituição',
        })[['Nome', 'ID Substituição', 'Nome Substituição']]
        
        print(f"{'ID Or.':<9} {'Nome':<{MAX_NAME_LENGTH}} | {'ID Sub.':<9} {'Nome Substituição':<{MAX_NAME_LENGTH}}")
        print("-" * (MAX_NAME_LENGTH * 2 + 18))
        
        for index, row in df.iterrows():
            nome = truncate_string(row['Nome'])
            nome_substituicao = truncate_string(row['Nome Substituição'])

            print(f"{str(index):<9} {nome:<{MAX_NAME_LENGTH}} | {str(row['ID Substituição']):<9} {nome_substituicao:<{MAX_NAME_LENGTH}}")


if __name__ == "__main__":
    main()