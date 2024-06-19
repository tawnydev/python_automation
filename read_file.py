import pandas as pd
import requests

url = "http://localhost:8080"
customer_endpoint = "/customers"
hotel_endpoint = "/hotels"
reservation_endpoint = "/reservations"


########## functions ##########
def findCustomer(firstname, lastname, list):
    for c in list:
        if c["firstname"] == firstname and c["lastname"] == lastname:
            return c
    return None


def findHotel(name, list):
    for h in list:
        if h["name"] == name:
            return h
    return None


def findReservation(id_customer, id_hotel, chambre, list):
    for r in list:
        if r["customer"]["id"] == id_customer and r["hotel"]["id"] == id_hotel and r[
            "chambre"] == chambre:
            return r
    return None


########## script ##########
# GET DATA FROM API
print("1) Get Customers")
api_customers = requests.get(url + customer_endpoint)
customers_list = []

if api_customers:
    print("Get Customers => Success!")
    customers_list = api_customers.json()
else:
    raise Exception(f"Non-success status code: {api_customers.status_code}")
print("2) Get Hotels")
api_hotels = requests.get(url + hotel_endpoint)
hotels_list = []

if api_hotels:
    print("Get Hotels => Success!")
    hotels_list = api_hotels.json()
else:
    raise Exception(f"Non-success status code: {api_hotels.status_code}")
print("3) Get Reservations")
api_reservations = requests.get(url + reservation_endpoint)
reservations_list = []

if api_reservations:
    print("Get Reservations => Success!")
    reservations_list = api_reservations.json()
else:
    raise Exception(f"Non-success status code: {api_reservations.status_code}")

# READ FILE
print("4) Read file")
customers_file = pd.read_excel("customers.xlsx")

for ind in customers_file.index:
    # customer process
    firstname_index = customers_file['customer firstname'][ind]
    lastname_index = customers_file['customer lastname'][ind]
    current_customer = findCustomer(firstname_index, lastname_index, customers_list)
    if current_customer is not None:
        print(firstname_index + " trouve!")
    else:
        print(firstname_index + " non trouve!")
        print("creation du customer")
        create_customer = requests.post(url + customer_endpoint,
                                        json={"firstname": str(firstname_index), "lastname": str(lastname_index)})
        if create_customer:
            print("Create Customer => Success!")
            new_customer = create_customer.json()
            customers_list.append(new_customer)
        else:
            raise Exception(f"Non-success status code: {create_customer.status_code}")
    # hotel process
    hotel = customers_file['hotel'][ind]
    current_hotel = findHotel(hotel, hotels_list)
    if current_hotel is not None:
        print(hotel + " trouve!")
    else:
        print(hotel + " non trouve!")
        print("creation du hotel")
        create_hotel = requests.post(url + hotel_endpoint, json={"name": str(hotel)})
        if create_hotel:
            print("Create Hotel => Success!")
            new_hotel = create_hotel.json()
            hotels_list.append(new_hotel)
        else:
            raise Exception(f"Non-success status code: {create_hotel.status_code}")
    # reservation process
    chambre = customers_file['chambre'][ind]
    opt_spa = False
    if customers_file['option spa'][ind] == "ok":
        opt_spa = True
    opt_petit_dej = False
    if customers_file['petit dej'][ind] == "ok":
        opt_spa = True
    cout_restaurant = 0.0
    if str() != "nan" and isinstance(customers_file['cout restaurant'][ind],(int,float)):
        cout_restaurant = float(customers_file['cout restaurant'][ind])
    current_reservation = findReservation(current_customer["id"], current_hotel["id"], chambre, reservations_list)
    if current_reservation is not None:
        print("reservation " + str(chambre) + " dans " + hotel + " pour " + firstname_index + " trouve!")
    else:
        print(str(chambre) + " non trouve!")
        print("creation de la reservation")
        print({"chambre": int(chambre), "hotel": current_hotel,
                                                                      "customer": current_customer,
                                                                      "optionPetitDej": opt_petit_dej,
                                                                      "optionSpa": opt_spa,
                                                                      "coutRestaurant": cout_restaurant})
        create_resa = requests.post(url + reservation_endpoint, json={"chambre": int(chambre), "hotel": current_hotel,
                                                                      "customer": current_customer,
                                                                      "optionPetitDej": opt_petit_dej,
                                                                      "optionSpa": opt_spa,
                                                                      "coutRestaurant": cout_restaurant})
        if create_resa:
            print("Create Reservation => Success!")
            new_resa = create_resa.json()
            reservations_list.append(new_resa)
        else:
            raise Exception(f"Non-success status code: {create_resa.status_code}")
