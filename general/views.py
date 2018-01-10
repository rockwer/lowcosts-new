from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'general/landing.html', {})

def search_history(request):
    prices = Price.objects.all().order_by('price_USD', 'update_date')
    paginator = Paginator(prices, 50)
    page = request.GET.get('page')
    try:
        prices = paginator.page(page)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)
    # contacts = paginator.get_page(page)
    return render(request, 'wizz/history.html', { 'prices': prices })

def get_search_results(request, request_id):
    prices = Price.objects.filter(request_id=request_id).order_by('price_USD', 'update_date')
    return render(request, 'wizz/results.html', {'prices': prices})

def get_all_requests(request):
    requests = Price.objects.order_by().values('request_id').distinct()
    print(requests)
    return render(request, 'wizz/all_requests.html', {'requests': requests})