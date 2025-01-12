# Imports
# pypdf for parsing pdf
from pypdf import PdfReader
# regex for advanced string matching
import re
# pandas for csv
import pandas as pd


# Main program
def search_pdf(pdf_file):
    # Open PDF-file and read it
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    # Extract text from PDF for parsing
    page_text = page.extract_text()
    # Remove unwanted text not dismissed by regex in the following section
    ignored_text_lines = ["V PAY", "SPAARZEGELS", "PREMIUM", "SUBTOTAAL", "KOOPZEGELS"]
    for text in ignored_text_lines:
        page_text = page_text.replace(text, "")
    # Split into lines
    lines = page_text.split('\n')


    # Search lines
    products = []
    for line in lines:
        # Search for products bought, excluding non-relevant information
        regex = r"^(B?B?[0-9]+.?[0-9]*?K?G?) ([A-Z\.\,\']+[A-Z\.\,\' ]+) ([0-9 ]+\,[0-9]+)"
        groceries_search = re.search(regex, line)
        # Store found groceries in variable and print
        if groceries_search:
            # Split the match into amount, product and price
            matches = re.match(regex, line)
            amount = matches.group(1)
            product = matches.group(2)
            price = matches.group(3)
            # Remove the 'B' or 'BB' at the start of the 'quantity' string
            amount = re.search(r"[0-9,.]+([A-Z]{2})?", amount)[0]
            # Remove prices per piece from product if applicable
            product = re.search(r"[a-zA-Z_\'\,\.]+( [a-zA-Z_\'\,\.]+)*", product)[0]
            # Remove the empty space from price
            price = price.replace(" ","")
            print(f"{amount} x {product} {price}")
            products.append({"amount": amount,"product":product,"total": price})
    return products

def data_to_csv(new_groceries):
    # Open and read csv file with write function
    csv_file = 'assets/groceries.csv'
    df = pd.read_csv(csv_file, sep=';')
    # Print output groceries_quantity_new to first column
    for grocery in new_groceries:
        amount = re.search(r"^[0-9\,\.]+", grocery['amount'])[0]
        total = float(grocery['total'].replace(',','.'))
        price = round(total / float(amount), 2)
        new_entry = pd.DataFrame([{
            'Amount/quantity': grocery['amount'],
            'Product': grocery['product'],
            'Price': price,
            'Total': total
        }])
        df = pd.concat([df, new_entry], ignore_index=True, axis=0)

    df.to_csv(csv_file, index=False, sep=';')



# Initializer
if __name__ == "__main__":
    pdf_file = "assets/AH_kassabon_2.pdf"
    #search_pdf(pdf_file)
    data_to_csv(search_pdf(pdf_file))

