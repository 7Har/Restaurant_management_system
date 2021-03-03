# I have created this file - Darshan
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')
    # return HttpResponse("<h1 align='center'> <font color='#FF0000' size='9' > Welcome Our Restaurant </font> </h1>")


# def about(request):
#     return HttpResponse("We are at about")
#
#
# def contact(request):
#     return HttpResponse("We are at contact")
#
#
# def tracker(request):
#     return HttpResponse("We are at tracker")
#
#
# def search(request):
#     return HttpResponse("We are at search")
#
#
# def checkout(request):
#     return HttpResponse("We are at checkout")
#
