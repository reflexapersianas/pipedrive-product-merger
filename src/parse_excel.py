import pandas as pd

class ColumnNames:
    ID = "ID"
    NAME = "Nome"
    ID_REPLACEMENT = "TRANSFORMAR NO ID"


def extract_data_from_excel(file_path: str) -> dict:
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()

    df[ColumnNames.ID_REPLACEMENT] = pd.to_numeric(
        df[ColumnNames.ID_REPLACEMENT], errors="coerce"
    )

    df = df.dropna(subset=[ColumnNames.ID_REPLACEMENT])
    print(df[[ColumnNames.ID, ColumnNames.NAME, ColumnNames.ID_REPLACEMENT]].to_string())

    data_dict = {
        int(row[ColumnNames.ID]): {
            "name": row[ColumnNames.NAME],
            "id_replacement": int(row[ColumnNames.ID_REPLACEMENT]),
        }
        for _, row in df.iterrows()
    }
    return data_dict


if __name__ == "__main__":
    import sys, json
    
    output_path = "output/1_excel_data.json"

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        data = extract_data_from_excel(file_path)
        print(json.dumps(data, ensure_ascii=False, indent=4))
        with open(output_path, "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"\n[i] Data written to {output_path} ({len(data)} records)")
    else:
        print("[x] Please provide the path to the Excel file as a command-line argument.")
