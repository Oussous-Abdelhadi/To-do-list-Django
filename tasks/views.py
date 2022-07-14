from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.utils.text import slugify

from tasks.models import Collection, Task

# Create your views here.

def index(request):
    """ Contenu de la page index.html """
    context = {}
    collection_slug = request.GET.get("collection")
    collection = Collection.get_defaut_collection()

    if collection_slug:
        collection = get_object_or_404(Collection, slug=collection_slug)

    context["collections"] = Collection.objects.order_by("slug")
    context["collection"] = collection
    context["tasks"] = collection.task_set.order_by("description")

    return render (request, 'tasks/index.html', context=context)

def add_collection(request):
    """ Ajout d'une collection """
    collection_name = escape(request.POST.get("collection-name")) # escape pour faille XSS
    collection, created = Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))
    if not created :
        return HttpResponse("La collection existe déjà", status=409)
    return HttpResponse(f'<button>{collection_name}</button>')

def add_task(request):
    """ Return une description de la tâche """
    slug_url = request.POST.get("collection")
    collection = Collection.get_defaut_collection()
    if request.POST.get("collection"):
        collection = Collection.objects.get(slug=slug_url)
    task = request.POST.get("task-description")
    Task.objects.create(description=task, collection=collection)

    return HttpResponse(f"<p>{task}</p>")

def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    return HttpResponse("")

def delete_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    collection.delete()
    return redirect('home')

def get_task(request, collection_pk):
    """ Return une description de la tâche """
    collection = get_object_or_404(Collection, pk=collection_pk)
    tasks = collection.task_set.order_by("description")
    return render (request, 'tasks/tasks.html', context={'tasks':tasks, "collections": collection})