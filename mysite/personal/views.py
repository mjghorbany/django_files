from django.shortcuts import render
from django.http import HttpResponse

import requests
from py2neo import Graph,authenticate
import json



def get_books():
    authenticate("localhost:7474", "neo4j", "mjgh2765")
    graph = Graph()
    query = """
    MATCH (n:Drink) RETURN n LIMIT 3
    """
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
    books=get_books()
    return render(request,'personal/graph1.html',{'books': books})


def contact(request):
    return render(request,'personal/contact.html',{'content':['If you are interested to know more about us, please email : ','info@dana.xyz']})