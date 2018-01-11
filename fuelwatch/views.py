from django.http import JsonResponse
from django.shortcuts import render
import feedparser
import itertools


def mithrildata(request):
    print("inside dajngo")
    if request.GET:
        # print(request.GET.getlist('Product'))
        # print(request.GET.getlist('Metroregion'))
        # print(request.GET.get('Tomorrow'))
        # getlist  is to get the arguments in Array form
        url,list_data=get_data(request.GET.getlist('Product'),request.GET.getlist('Metroregion'),request.GET.get('Tomorrow'))
        return JsonResponse(list_data, safe=False)
    return render(request,"mithril.html")

def get_data(Product,Metroregion,Tomorrow):
     # Declaring emply list to store feed data
     list_data =[]

     #Get the List of URL's to Parse
     url = generate_url([Product],[Metroregion],Tomorrow)

     #Parse the url's in list using feedparser
     for i in url:
        list_parse = feedparser.parse(i)

        # channel elements are available in fuel.feed
        title = list_parse.feed.title

        # item elements are available in x.entries
        for i in list_parse.entries:
            dic_data = {
                        'Price' : i.price,
                        'Location':i.location,
                        'Address':i.address,
                        'Phone':i.phone,
                        'Brand' :i.brand,
                        'Date' : i.date
                       }

            list_data.append(dic_data)
            list_data = sorted(list_data, key=lambda k: k['Price'])
     return url,list_data

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
