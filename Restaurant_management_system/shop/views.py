from django.shortcuts import render, HttpResponse, redirect

# I have created this file - Darshan
# from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
# from PayTm import Checksum


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    darshan = {'allProds': allProds}
    return render(request, 'shop/index1.html', darshan)
    # return HttpResponse("<h1 align='center'> <font color='#FF0000' size='9' > Welcome Our Restaurant </font> </h1>")


# def login(request):
#     return render(request, 'shop/login.html')


# def signup(request):
#     return render(request, 'shop/signup.html')


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html', {'thank': thank})


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
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.desc or query in item.product_name or query in item.category or query in item.desc.upper() or query in item.product_name.upper() or query in item.category.upper():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    darshan = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 3:
        darshan = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', darshan)


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        # name = request.POST['name']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email1']
        phone = request.POST['phone']
        password = request.POST['password']
        password1 = request.POST['password1']

        # check for errorneous input
        if (password1 != password):
            messages.error(request, " Passwords do not match")
            return redirect('/shop')

        # Create the user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        # myuser.name = name
        myuser.first_name = f_name
        myuser.last_name = l_name
        myuser.phone = phone
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return redirect('/shop')

    else:
        return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')
