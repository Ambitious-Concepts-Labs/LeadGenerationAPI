import os

import googlemaps

# import win32.com.client as win32

API_KEY = open('API_KEY.txt').read()
map_client = googlemaps.Client(API_KEY)

import requests

# url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=mongolian&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + API_KEY


def get_place_info_test(business_type, location_name):
    try:
        query = "query=" + business_type
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?" + query + "%20in%20" + location_name + "&key=" + API_KEY

        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        res = response.json()
        results = res['results']
        print(len(results))
        return response.json()
    except Exception as e:
        print(e)
        return None

print(get_place_info_test("restaurants", "Dallas Texas"))
# print(dir(map_client)) # Map Keys from Google Maps API

def get_place_info(location_name):
    try:
        # location_name = 'Lanxess Arena Köln' #For Testing
        response = map_client.places(query=location_name)
        results = response.get('results')[0]
        print(len(response.get('results')))
        # print(results[0]['business_status'])
        # print(results[0]['formatted_address'])
        # print(results[0]['name'])
        # print(results[0]['place_id'])
        # print(results[0]['rating'])
        # print(results[0]['user_ratings_total'])
        return results
    except Exception as e:
        print(e)
        return None
# print(get_place_info('Business Dallas Texas'))

# xlApp = win32.Dispatch('Excel.Application')
# xlApp.Visible = True
# wb = xlApp.workbooks.open(os.path.join(os.getcwd(), 'Copy of output.xlsx'))
# wsList = wb.Worksheets('List')


# LastRow = wsList.Cells(wsList.Rows.Count, 'A').End(-4162).Row

# for i in range(2, LastRow+1):
#     place_info = get_place_info(wsList.Cells(i, 1).Value)
#     wsList.cells(i, 2).Value = place_info['name']
#     wsList.cells(i, 3).Value = place_info['formatted_address']
#     wsList.cells(i, 4).Value = place_info['place_id']
#     wsList.cells(i, 5).Value = place_info['rating']
#     wsList.cells(i, 6).Value = place_info['user_ratings_total']

# wb = None
# wsList = None
# xlApp = None