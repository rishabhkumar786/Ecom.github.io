from django.shortcuts import render
from django.http import HttpResponse
from .models import product, Contact, Orders, OrderUpdate
from math import ceil
from Paytm import checksum
import json
from django.views.decorators.csrf import csrf_exempt
MERCHANT_KEY = 'kbzk1DSBJiV_03p5'

def index(request):
    #products = product.objects.all()
    #n = len(products)
    #nSlides = n//4 + ceil(n/4 - n//4)
    #params = {'no_of_slides': nSlides, 'product': products, 'range': range(1, nSlides)}
    #allprods = [[products, range(1, nSlides), nSlides], [products, range(1, nSlides), nSlides]]

    allProds = []
    catProds = product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil(n / 4 - n // 4)
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allProds}
    return render(request, 'shop/index.html', params)




def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        # print(name, email, phone, desc)
        contact = Contact(name=name, email=email,phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def searchMatch(query, item):
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = '11'
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        print(n)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def history(request):
    return render(request, 'shop/history.html')

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status" : "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status" : "NoItem"}')
        except Exception as e:
            return HttpResponse('{"status" : "Error"}')

    return render(request, 'shop/tracker.html')
    return render(request, 'shop/tracker.html')

def productView(request, myid):
    # fetching the product by id
    p_product = product.objects.filter(id=myid)

    return render(request, 'shop/productView.html', {'product_sample': p_product[0]})



def checkout(request):
    dup_id = 0
    dup_email = ""
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json= items_json,name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        dup_id = order.order_id
        dup_email = email

        # request paytm to transfer amount to your account by the taking payment from user
        param_dict = {
            'MID': 'SqEmpN40297461727019', #this is staging MID to get order placed type your merchant id
            'ORDER_ID': str(dup_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': dup_email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    else:
        thank = False
        id = 0
    #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Checksum = form[i]


    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, Checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


