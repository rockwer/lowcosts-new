from django.shortcuts import render
from django.http import HttpResponseRedirect
from general.models import Airport, priceType, priceTemplate, Price
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    return HttpResponseRedirect('/landing/')
    
def landing(request):
    return render(request, 'lowcosts/landing.html', {})

def search_history(request):
    prices = Price.objects.all().order_by('price_USD', 'update_date')
    paginator = Paginator(prices, 20)
    page = request.GET.get('page')
    try:
        prices = paginator.page(page)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)
    # contacts = paginator.get_page(page)
    return render(request, 'lowcosts/history.html', { 'prices': prices })

def get_search_results(request, request_id):
    prices = Price.objects.filter(request_id=request_id).order_by('price_USD', 'update_date')
    return render(request, 'lowcosts/results.html', {'prices': prices})

def get_all_requests(request):
    requests = Price.objects.order_by().values('request_id').distinct()
    print(requests)
    return render(request, 'lowcosts/all_requests.html', {'requests': requests})