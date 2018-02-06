from django.http import JsonResponse
from django.shortcuts import render
import feedparser
import itertools
import requests
import json
# To cache the the data
from django.core.cache import cache
from django.views.decorators.cache import cache_page




def testdata(request):
    print("inside test")
    if request.GET:
        # getlist  is to get the arguments in Array form
        url,list_data=get_data(request.GET.getlist('Product'),request.GET.getlist('Metroregion'),request.GET.get('Tomorrow'))
        return JsonResponse(list_data, safe=False)
    return render(request,"test.html")

def mithrildata(request):
    print("inside dajngo")
    if request.GET:
        print(request.GET.getlist('Product'))
        print(request.GET.getlist('Region'))
        print(request.GET.get('Tomorrow'))

        # getlist  is to get the arguments in Array form
        list_data=get_data(request.GET.getlist('Product'),request.GET.getlist('Region'),request.GET.get('Tomorrow'))

        # print(list_data)
        return JsonResponse(list_data, safe=False)
    return render(request,"mithril.html")

# def getDistance(lat1,lng1,lat2,lng2):
#
#     latlng1 = f'{lat1},{lng1}|'
#     latlng2 = f'{lat2},{lng2}'
#
#     x = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?',
#                      params = {'origins':latlng1,
#                                'destinations':latlng2,
#                                'key':DIST_KEY})
#
#     #print(x.url)
#     data= json.loads(x.content)
#     status = [data['status']]
#
#     if status == ['OK']:
#         distance = data['rows'][0]['elements'][0]['distance']['value']
#         distancekm = distance/1000
#         print('distance',distance)
#         return distancekm

#@cache_page(None, key_prefix="Fuelwatchdata")
def get_data(Product,Metroregion,Tomorrow):
     # Declaring emply list to store feed data
     list_data =[]

     #Get the List of URL's to Parse
     url = generate_url([Product],[Metroregion],Tomorrow)

     # lat1 = -32.0555
     # lng1 = 115.8474

     #Parse the url's in list using feedparser
     for i in url:
        list_parse = feedparser.parse(i)

        # channel elements are available in fuel.feed
        title = list_parse.feed.title
        print('title')

        # item elements are available in x.entries
        for i in list_parse.entries:



            cache.set_many({'Price' : i.price,
                            'Location':i.location,
                            'Address':i.address,
                            'Phone':i.phone,
                            'Brand' :i.brand,
                            'Date' : i.date,
                            'Latitude':i.latitude,
                            'Longitude':i.longitude})

            x = cache.get_many({'Address','Latitude','Longitude'})
            # Call getDistance to send address and calculate the distance
            #distance= getDistance(lat1,lng1,i.latitude,i.longitude)

            dic_data = {
                        'Price' : i.price,
                        'Location':i.location,
                        'Address':i.address,
                        'Phone':i.phone,
                        'Brand' :i.brand,
                        'Date' : i.date,
                        'Latitude':i.latitude,
                        'Longitude':i.longitude
                       }

            list_data.append(dic_data)
            list_data = sorted(list_data, key=lambda k: k['Price'])

     return list_data

def generate_url(Product,Region,Tomorrow):
    # list to store the url's generated
     link = []
     for i  in itertools.product(*Product,*Region):
         print('GEnurl',Product,Region)
         gen_url = ("http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}".format(*i))
         link.append(gen_url)
         if Tomorrow:
             gen_url = ("http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}&Day=tomorrow".format(*i))
             link.append(gen_url)
             print('djangourl',link)
     return (link)
