import requests
import csv
import json
from bs4 import BeautifulSoup

url = "https://www.baraasallout.com/test.html"
response = requests.get(url)

if response.status_code == 200:
    print("Page loaded successfully.")
else:
    print(f"Error: Unable to load the page (Status code: {response.status_code})")
    exit()

page = BeautifulSoup(response.text, "html.parser")
product_cards = page.find_all("div", class_="product-card")
products_data = []

for card in product_cards:
    product_name = card.find("span", class_="name")
    if product_name:
        product_name = product_name.text.strip()
    else:
        product_name = "N/A"

    price = card.find("span", class_="price")
    if price:
        price = price.text.strip()
    else:
        price = "N/A"

    stock = card.find("span", class_="stock")
    if stock:
        stock = stock.text.strip()
    else:
        stock = "N/A"

    add_to_basket = card.find("button", class_="add-to-basket")
    if add_to_basket:
        add_to_basket = add_to_basket.text.strip()
    else:
        add_to_basket = "N/A"
    
    products_data.append({
        "name": product_name,
        "price": price,
        "stock": stock,
        "add_to_basket": add_to_basket
    })

for product in products_data:
    print(product)

with open("Product_Information.json", "w", encoding="UTF-8") as json_file:
    json.dump(products_data, json_file, indent=4, ensure_ascii=False)

print("Data has been saved to 'Product_Information.json'.")

headers = page.find_all(["h1", "h2"])
print("Headers:")
header_text = [header.get_text() for header in headers]
for text in header_text:
    print(text)

paragraph = page.find("p")
if paragraph:
    print("Paragraph:")
    print(paragraph.get_text())
else:
    print("No paragraph found.")

lists = page.find_all("li")
print("List items:")
list_text = [item.get_text() for item in lists]
for item in list_text:
    print(item)

with open("Extract_Text_Data.CSV", mode="w", newline="", encoding="UTF-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Header", "Paragraph", "List Items"])
    writer.writerow([", ".join(header_text), paragraph.get_text() if paragraph else "", ", ".join(list_text)])

table = page.find("table")
if table:
    rows = table.find_all("tr")
    with open("Extract_Table_Data.CSV", mode="w", newline="", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Price", "Stock Status"])
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                product_name = cols[0].text.strip()
                price = cols[1].text.strip()
                stock_status = cols[2].text.strip()
                writer.writerow([product_name, price, stock_status])

    print("Data has been saved to 'Extract_Table_Data.CSV'.")
else:
    print("No table found on the page.")





