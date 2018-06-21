from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.template import loader
from .models import Node,Rel
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import NodeSerializer
from django.http import Http404

from django.views import generic
from django.shortcuts import render

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from neo4jrestclient import client
from neo4j.v1 import GraphDatabase

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import OntologyForm
from .models import Ontology
from .graph import extract_qa, extract_utterances

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_ontology(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = OntologyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            ontology = form.save(commit=False)
            ontology.user = request.user
            ontology.ontology_logo = request.FILES['ontology_logo']
            file_type = ontology.ontology_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': ontology,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'KBMS/create_ontology.html', context)
            ontology.save()
            return render(request, 'KBMS/detail.html', {'album': ontology})
        context = {
            "form": form,
        }
        return render(request, 'KBMS/create_ontology.html', context)


# Create your views here.
def index(request):
    template='KBMS/index.html'

    #querying the graph to get the info
    uri = "bolt://35.161.86.89:7687"
    driver = GraphDatabase.driver(uri, auth=("admin", "AIRocks@17"))
    with driver.session() as session:
        node_object = session.run('MATCH (n) RETURN count(*)')
        rel_object = session.run('MATCH ()-[r]->() RETURN count(*)')

    node_count = node_object.values()[0][0]
    rel_count = rel_object.values()[0][0]

    print('Hereeeee',node_count,rel_count)
    context={
        'nodes_n': node_count,
        'rels_n': rel_count,
        'rules_n': '0',
        'ontology_n': '5',
    }
    return render(request,template,context)

def ontology(request):
    # if not request.user.is_authenticated():
    #     return render(request, 'music/login.html')
    # else:
    #     ontologies = Ontology.objects.filter(user=request.user)
    #     query = request.GET.get("q")
    #     if query:
    #         ontologies = ontologies.filter(
    #             Q(album_title__icontains=query) |
    #             Q(artist__icontains=query)
    #         ).distinct()
    #         return render(request, 'KBMS/ontology.html', {
    #             'ontologies': ontologies,
    #         })
    #     else:
    return render(request, 'KBMS/ontology.html')

def cy2neo(request):

    return render(request, 'KBMS/cy2neo.html')


def rule_engine(request):
    res=do_graph_query(request)
    context={
        'res1' : res[0][0],
        'res2' : res[1][0],
    }
    return render(request,'KBMS/rule.html',context)


def detail(request, ontology_id):
    if not request.user.is_authenticated():
        return render(request, 'KBMS/login.html')
    else:
        user = request.user
        album = get_object_or_404(Ontology, pk=ontology_id)
        return render(request, 'KBMS/detail.html', {'ontology': ontology, 'user': user})



def favorite(request, node_id):
    node=get_object_or_404(Node,pk=node_id)
    template = 'KBMS/detail.html'

    try:
        selected_node=Node.objects.get(pk=request.POST['node'])
    except (KeyError, Node.DoesNotExist):
        raise Http404('The Node you asked for doesn not exist!')

        return render(request,template,{
            'node':node,
            'error_message':'No Valid Node',
        })
    else:
        selected_node.is_favorite=True
        selected_node.save()
        return render(request, template, {'node':node})


class IndexView(generic.ListView):
    template_name = "KBMS/index.html"
    context_object_name = 'all_nodes'

    def get_queryset(self):
        return Node.objects.all()


class DetailView(generic.DetailView):
	model=Node
	template_name='KBMS/detail.html'

class NodeCreate(CreateView):
    model = Node
    fields = ['name','att1','att2','att3']




# Lists all stocks or creates a new one
# stocks/
class NodeList(APIView):

    def get(self, request):
        stocks = Node.objects.all()
        serializer = NodeSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodeDetail(APIView):
    def get_object(self, pk):
        try:
            return Node.objects.get(pk=pk)
        except Node.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = NodeSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = NodeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def do_graph_query(request):
    """Make query to Neo4j, return names of associated nodes."""


    url = "http://35.161.86.89:7474/db/data"
    gdb = GraphDatabase(url, username="admin", password="AIRocks@17")

    q = "MATCH (n:Drink) RETURN n LIMIT 25"
    results = gdb.query(q=q, data_contents=True)

    result=results.rows

    return result
    # result.rows[0][0]['calories']


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "KBMS/cy2neo.html", data)

    try:
        graph_name = request.POST["graph_name"]
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.xlsx'):
            return HttpResponse('<h1>File is not excel type</h1>')
        # if file is too large, return
        if csv_file.multiple_chunks():
            return HttpResponse('<h1>Uploaded file is too big (%.2f MB).</h1>')

        a=extract_qa(csv_file)
        b=extract_utterances(csv_file)
        data['graph_res']=a
        data['graph_name'] = graph_name

    except Exception as e:
        response_data = {}
        response_data['message'] = "This is an exception"
        response_data['res']=str(e)
        return JsonResponse(response_data, status=201)

    data['query']="MATCH(n: HR1)-[r]->(m:HR1) RETURN n, r, m LIMIT 50"
    return render(request, 'KBMS/cy2neo.html', data)