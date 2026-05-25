import pandas as pd

def extract_excel_data(file_path: str):
    extracted_data = {}

    with pd.ExcelFile(file_path) as excel_file:
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            extracted_data[sheet_name] = df.to_dict(orient="records")

    return extracted_data

