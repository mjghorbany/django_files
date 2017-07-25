from django.shortcuts import render
from django.http import HttpResponse

import requests
from py2neo import Graph,authenticate
import json
from .models import Triple


def get_books(claim):
    authenticate("localhost:7474", "neo4j", "mjgh2765")
    graph = Graph()

    #query="""MATCH (p:Person { name: 'Sally' }) RETURN p LIMIT 25"""
    query_before = """MATCH (record:"""
    query_after = """) RETURN record LIMIT 6"""
    query = query_before + claim + query_after
    data = graph.cypher.execute(query)


    # url = 'http://api.example.com/books'
    # params = {'year': year, 'author': author}
    # r = requests.get('http://api.example.com/books', params=params)

    books = data
    #books_list = {'books':books['results']}
    print(books)
    return books

# Create your views here.
def index(request):
    return render(request,'personal/graph1.html')


def search(request):
    if request.method == 'POST':
        print('in here')
        claim = request.POST.get('claim_field', None)
        print('claim_id: ',claim)
        try:
            #claim = Triple.objects.get(node1 = search_id)
            #do something with user
            books = get_books(claim)
            print(books)
            return render(request,'personal/graph1.html',{'books': books})
        except Triple.DoesNotExist:
            print('no match')
            return HttpResponse("Error")

    else:
        return render(request, 'graph1.html')


def contact(request):
    return render(request,'personal/contact.html',{'content':['If you are interested to know more about us, please email : ','info@dana.xyz']})