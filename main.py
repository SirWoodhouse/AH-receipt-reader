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
    page_text_new = page_text.replace("V PAY", "")
    page_text_new_2 = page_text_new.replace("SPAARZEGELS",  "")
    page_text_new_3 = page_text_new_2.replace("PREMIUM", "")
    # Split lines for easier parsing
    lines = page_text_new_3.split('\n')

    # Search lines
    for line in lines:
        # Search for products bought, excluding non-relevant information
        groceries_search = re.search(
        r"^B[0-9]|BB[0-9]|^[0-9]\s|^[0-9]\.\d{2,3}", line)
        # Store found groceries in variable and print
        if groceries_search:
            groceries = line

            # Split line to only get the quantity of bought products
            # in int or float
            groceries_quantity = groceries.split()[0]
            # Remove the 'B' or 'BB' at the start of the 'quantity' string
            groceries_quantity_new = groceries_quantity.replace("B","")
            print(groceries_quantity_new)

            # First part of product line
            groceries_products = groceries.split()[1:2]
            for value in groceries_products:
                items = re.search("([A-Z]+)", value)
                if items:
                    first_part = items.group()
                    print(first_part)

            # Second part of products line
            groceries_products = groceries.split()[2:3]
            for value in groceries_products:
                items = re.search("([A-Z]+)", value)
                if items:
                    second_part = items.group()
                    print(second_part)

            # Third part of products line
            groceries_products = groceries.split()[3:4]
            for value in groceries_products:
                items = re.search("([A-Z]+)", value)
                if items:
                    third_part = items.group()
                    print(third_part)

            # Print first part of price
            groceries_prices = groceries.split()
            for value in groceries_prices:
                items = re.match(r"[0-9]+,[0-9]+", value)
                if items:
                    price_one = items.group()
                    print(price_one)


def data_to_csv(groceries_quantity_new):
    # Open and read csv file with write function
    df = pd.read_csv('assets/groceries.csv')

    # Print output groceries_quantity_new to first column

    pass


# Initializer
if __name__ == "__main__":
    pdf_file = "assets/AH_kassabon_2.pdf"
    # search_pdf(pdf_file)
    data_to_csv(search_pdf(pdf_file))

