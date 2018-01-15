from django.shortcuts import render
from .forms import FlightSearchForm
from .wizz_request import request_data
from general.new_request_number import new_request_number
from general.models import Airport, priceType, priceTemplate, Price
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from ac_wizzair.dates_from_range import get_dates_range
from django.utils import timezone
import requests
import json

# Create your views here.
def flight_search_form(request):
    form = FlightSearchForm(request.POST)
    if request.method == 'POST':
        request_id = new_request_number()
        departureStation = request.POST.get('departureStation')
        arrivalStation = request.POST.get('arrivalStation')
        dateFrom = request.POST.get('date_from')
        dateTo = request.POST.get('date_to')
        priceType = request.POST.get('priceType')

        dates_range = get_dates_range(dateFrom, dateTo)
        request_index = 0
        while request_index < len(dates_range['dates_from']):
            date_from = dates_range['dates_from'][request_index]
            date_to = dates_range['dates_to'][request_index]

            request_1 = request_data(departureStation, arrivalStation, date_from, date_to, priceType)
            currency_now = requests.get('https://openexchangerates.org/api/latest.json?app_id=6cdf29a6391b479cb9d0a4fe9608fa04')
            currency_json = json.loads(currency_now.content)
            for j in request_1['outboundFlights']:
                new_price = Price()
                new_price.request_id = request_id
                new_price.departureStation_IATA = j['departureStation']
                new_price.arrivalStation_IATA = j['arrivalStation']
                new_price.date = j['departureDate'][0:10]
                if j['price'] is None:
                    print(j['price'])
                    new_price.price = 0.0
                    new_price.currency = 'NON'
                    new_price.price_USD = 0.0
                else:
                    new_price.price = j['price']['amount']
                    new_price.currency = j['price']['currencyCode']
                    new_price.price_USD = float(new_price.price)/currency_json['rates'][new_price.currency]
                new_price.price_type = priceType
                new_price.update_date = timezone.now()
                airport_d = Airport.objects.get(iata_code=j['departureStation'])
                airport_a = Airport.objects.get(iata_code=j['arrivalStation'])
                new_price.departureStation = airport_d.name #j['departureStation']
                new_price.arrivalStation = airport_a.name #j['arrivalStation']
                new_price.air_company = 'WiZZ Air'
                new_price.save()
            for j in request_1['returnFlights']:
                new_price_return = Price()
                new_price_return.request_id = request_id
                new_price_return.departureStation_IATA = j['departureStation']
                new_price_return.arrivalStation_IATA = j['arrivalStation']
                new_price_return.date = j['departureDate'][0:10]
                if j['price'] is None:
                    print(j['price'])
                    new_price_return.price = 0.0
                    new_price_return.currency = 'NON'
                    new_price_return.price_USD = 0.0
                else:
                    new_price_return.price = j['price']['amount']
                    new_price_return.currency = j['price']['currencyCode']
                    new_price_return.price_USD = float(new_price_return.price) / currency_json['rates'][new_price_return.currency]
                new_price_return.price_type = priceType
                new_price_return.update_date = timezone.now()
                airport_d_return = Airport.objects.get(iata_code=j['departureStation'])
                airport_a_return = Airport.objects.get(iata_code=j['arrivalStation'])
                new_price_return.departureStation = airport_d_return.name  # j['departureStation']
                new_price_return.arrivalStation = airport_a_return.name  # j['arrivalStation']
                new_price_return.air_company = 'WiZZ Air'
                new_price_return.save()

            request_index += 1
            sleep(5)
        # request_res.update(request_1)
        url = reverse('search-results', kwargs={'request_id': request_id})
        return HttpResponseRedirect(url)
    return render(request, 'lowcosts/search.html', {'form': form})


def get_wizzair_airports(request, city_code):
    ap_request = requests.get('https://be.wizzair.com/7.7.5/Api/asset/map?languageCode=uk-ua')
    req_json = json.loads(ap_request.content)
    kiev_connections = []
    for city in req_json['cities']:
        if city['iata'] == city_code:
            airport = Airport.objects.get_or_create(
                iata_code=city['iata'],
                name=city['shortName'] + " (" + city['iata'] + ")",
                counrty=city['countryName'],
                city=city['shortName'],
                longitude=city['longitude'],
                latitude=city['latitude'],
            )
            for connect in city['connections']:
                kiev_connections.append(connect['iata'])
    for city in req_json['cities']:
        for ap in kiev_connections:
            if ap == city['iata']:
                airport = Airport.objects.get_or_create(
                iata_code=city['iata'],
                name=city['shortName'] + " (" + city['iata'] + ")",
                counrty=city['countryName'],
                city=city['shortName'],
                longitude=city['longitude'],
                latitude=city['latitude'],
            )
    return HttpResponse("Done")