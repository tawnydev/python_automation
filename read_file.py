import pandas as pd
import requests

########## functions ##########
def findCustomer(firstname, lastname, list):
    for c in list:
        if c["firstname"] == firstname and c["lastname"] == lastname:
            return True
    return False

########## script ##########
# GET DATA FROM API
print("1) Get Customers")
api_customers = requests.get("http://localhost:8080/customers")
customers_list = []

if api_customers:
    print("Get Customers => Success!")
    customers_list = api_customers.json()
else:
    raise Exception(f"Non-success status code: {api_customers.status_code}")

# READ FILE
print("2) Read file")
customers_file = pd.read_excel("customers.xlsx")
#print("nom colonnes="+str(customers_file.head(0)))
#print(customers_file["hotel"])
#print(customers_file["hotel"].shape)

for ind in customers_file.index:
    print(customers_file['customer firstname'][ind], customers_file['customer lastname'][ind])
    if findCustomer(customers_file['customer firstname'][ind],customers_file['customer lastname'][ind], customers_list):
        print(customers_file['customer firstname'][ind]+" trouve!")
    else:
        print(customers_file['customer firstname'][ind]+" non trouve!")

