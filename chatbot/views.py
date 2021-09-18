from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response

def index(request):
    return HttpResponse('<p>{"server": "UP"}</p>')