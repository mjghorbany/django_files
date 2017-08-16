from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.template import loader
from .models import Node
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views import generic

from django.shortcuts import render

# Create your views here.
def index(request):
    template='KBMS/home2.html'
    context={
        'nodes_n': '20',
        'rels_n': '17',
        'rules_n': '0',
        'ontology_n': '1',
    }
    return render(request,template,context)

def ontology(request):
    return render(request,'KBMS/ontology.html')


def detail(request, node_id):
    try:
        node=Node.objects.get(pk=node_id)
    except Node.DoesNotExist:
        raise Http404('The Node you asked for doesn not exist!')

    template='KBMS/detail.html'
    context={
        'nodes':node,
        'id':id,
        'rels': '20',
    }
    return render(request,template,context)

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
    fields = ['ini_node','att1','att2','att3']
