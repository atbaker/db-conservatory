from django.http import HttpResponse
from django.shortcuts import render

import requests

def show_containers(req):
    r = requests.get('http://ec2-54-237-81-117.compute-1.amazonaws.com/containers')
    return HttpResponse(r)

def create_container(req):
    r = requests.post('http://ec2-54-237-81-117.compute-1.amazonaws.com/containers')
    return HttpResponse(r)
