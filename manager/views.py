from django.http import HttpResponse

import requests

def show_containers(req):
    r = requests.get('http://ec2-54-205-233-235.compute-1.amazonaws.com/containers')
    return HttpResponse(r)

def create_container(req):
    r = requests.post('http://ec2-54-205-233-235.compute-1.amazonaws.com/containers')
    return HttpResponse(r)