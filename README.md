# Pipedrive Product Merger
Python scripts collection for merging duplicate Pipedrive products by replacing them in every deal they appear.

## ❓ Usage

You'll need to install the basic packages with pip.
```
py -m pip install -r requirements.txt
```

Export the products table from Pipedrive to an Excel file and create a replacement column, for example:
| ID | Name      | Replacement ID |
-----|-----------|----------------|
| 4  | Product Y |                |
| .. | ...       | ...            |
| 21 | Product X | 4              |
| .. | ...       | ...            |
* This will replace every appearance of Product X (ID 21) with Product Y (ID 4)

Set the environment variables `PIPE_SUBDOMAIN` (the name that appears before the .pipedrive.com in the URL) and `PIPE_TOKEN` (the API token) in your operational system, or you'll be asked for them in every script.

Then, run the script as needed to read the table, create the necessary objects and replace the products. The main scripts are indicated in the file structure below as (1) to (5). But, others were created for better analysis and personal use.

For the extra scripts, you'll need to run them as a package. For example,
```
py -m src.extra.verify_empty
```

## 📂 Scripts

```
src/
├── parse_excel.py                 # (1) Parses Excel file to extract the product replac.
├── product_deals.py               # (2) Fetches IDs from deals where products are assigned to.
├── product_deal_attachments.py    # (3) Fetches IDs of the deal-product attachments.
├── replace_deal_products.py       # (4) Replaces products attached to deals in Pipedrive.
├── delete_products.py             # (5) Deletes the now-empty products in Pipedrive.
├── pipedrive.py                   # PipedriveAPI class for interacting with the API
│
├── extra/
│   ├── rename_pipedrive_products.py       # Renames the products in Pipedrive with the read data.
│   ├── update_product_names.py            # Fetches the current product names (for better logging).
│   ├── verify_circular_substitution.py    # Checks for circular substitutions in product mappings
│   ├── verify_empty.py                    # Verifies for empty fields or missing data
│   └── visualize_datagrid.py              # Visualizes data in a grid format for analysis
│
└── utils/
    └── truncate_string.py                 # Utility for truncating strings
```