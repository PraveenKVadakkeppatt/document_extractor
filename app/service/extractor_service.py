import re


# Extract PO Number
def extract_po_number(text: str):

    # PO → exact text "PO", [-\s]? → optional - OR space, \d+ → one or more digits
    patterns = [r"PO[-\s]?\d+", r"#\s*(PO[-\d]+)"]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).replace("#", "").strip()
        
    return None



# Extract Date
def extract_order_date(text: str):
    pattern = r"Date\s*:\s*(.+)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip()
    
    return None


# Delivery Date
def extract_delivery_date(text: str):
    patterns = [
        r"Delivery Date\s*:\s*(.+)",
        r"Deliver By\s*:\s*(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()
        
    return None


# Vendor Details
def extract_vendor_details(text: str):
    pattern = r"Vendor Address(.*?)Deliver To"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        # Extract captured block
        block = match.group(1).strip()
        # Split into lines
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if lines:
            return{
                "name": lines[0],
                "address": ", ".join(lines[1:])
            }
        
    return {
        "name": None,
        "address": None
    }



# Deliver To
def extract_deliver_to(text: str):
    pattern = r"Deliver To(.*?)Item & Description"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        block = match.group(1).strip()
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        cleaned_lines = [ line for line in lines if line != "#"]
        return ", ".join(cleaned_lines)
    
    return None




# Line Item Extraction
def extract_line_items(text: str):
    lines = [ line.strip() for line in text.splitlines() if line.strip() ]

    items = []

    start_index = None

    for i, line in enumerate(lines):
        if line == "Item & Description":
            start_index = i + 5
            break

    if start_index is None:
        return items

    i = start_index

    while i < len(lines):
        if lines[i] == "Sub Total":
            break

        try:
            if lines[i].isdigit():
                item = {
                    "item_name": lines[i + 1],
                    "quantity": float(lines[i + 2]),
                    "rate": float(lines[i + 3]),
                    "tax_percent": float(lines[i + 4]),
                    "tax_amount": float(lines[i + 5]),
                    "total_amount": float(lines[i + 6]),
                }

                items.append(item)
                i += 7
            else:
                i += 1

        except (IndexError, ValueError):
            i += 1

    return items



# Master Extractor ( All in one )
def extract_purchase_order_data(raw_content):
    if isinstance(raw_content, dict):
        return extract_from_excel(raw_content)

    return{
        "po_number": extract_po_number(raw_content),
        "vendor_details": extract_vendor_details(raw_content),
        "date": extract_order_date(raw_content),
        "delivery_date": extract_delivery_date(raw_content),
        "deliver_to": extract_deliver_to(raw_content),
        "line_items": extract_line_items(raw_content)
    }



# Excel extraction
def extract_from_excel(excel_data):

    # Get all Sheet Names
    sheet_names = list(excel_data.keys())

    line_sheet = excel_data[sheet_names[0]]
    meta_sheet = excel_data[sheet_names[1]]

    metadata = {}

    for row in meta_sheet:
        metadata.update(row)

    return {
        "po_number": metadata.get("PO Number"),
        "vendor_details": {
            "name": metadata.get("Vendor"),
            "address": metadata.get("Vendor Address"),
        },
        "date": metadata.get("Date"),
        "delivery_date": metadata.get("Delivery Date"),
        "deliver_to": metadata.get("Deliver To"),
        "line_items": line_sheet,
    }
