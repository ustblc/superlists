from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest):
    return HttpResponse('<html><title>To-Do lists</title></html>')
