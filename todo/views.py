from django.shortcuts import render, render_to_response, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import shareTodoForm
from .models import Todo, Shared
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from pprint import pprint

# Create your views here.
def index(request):

    if request.user.is_authenticated:

        todos = Todo.objects.filter(author_id=request.user.id).order_by('-id')[:10]

        #isledi +
        #get_todo_with_relation = Todo.objects.filter(id=1).get().shared_set.all().values()


        
        try:
            get_shared = Shared.objects.filter(shared_with=request.user)
            #get_shared_todos = get_shared.todos.all().values()
            #return HttpResponse(get_shared)
        except Shared.DoesNotExist:
            get_shared = None

        #get_shared_todos = get_shared.todo.all().values()
        #return HttpResponse(get_shared_todos)
        return render(request,"user_example/profile.html",
            {"todos":todos, 
            "get_shared":get_shared })
    else:
        return redirect("/")

def welcome(request):
	if request.user.is_authenticated:
		return redirect("profile")
	else:
		return render(request,"welcome.html")

def addTodo(request):
	if request.method == "GET":

		return redirect("/")

	else:

		if request.user.is_authenticated:

			title = request.POST.get("title")
			newTodo = Todo(title = title, completed = False, author_id = request.user.id)
			newTodo.save()
			return redirect("profile")
			return HttpResponse(request.user.id)

		else:	
		    return redirect("/")

def update(request, id):
	#need to check current user can update
	#todo = Todo.objects.filter(id = id).first()
	todo = get_object_or_404(Todo, id = id)

	todo.completed = not todo.completed
	todo.save()
	return redirect("profile")

def delete(request, id):
	#need to check current user can update
	#todo = Todo.objects.filter(id = id).first()
	todo = get_object_or_404(Todo, id = id)
	todo.delete()
	return redirect("profile")

def detail(request, id):
    todo = Todo.objects.filter(id=id).first()

    #return HttpResponse(todo.shared_set.all().values())

    #return HttpResponse(todo.shared_set.all())

    try:
        shared = Shared.objects.filter(shared_with=request.user, todo=id)
        #get_shared_todos = get_shared.todos.all().values()
        #return HttpResponse(shared)
    except Shared.DoesNotExist:
        shared = None

    
    if not todo:
        return HttpResponse('404 not found - todo not found')

    if (todo.author.id == request.user.id) or (shared):
  
        return render(request,"detail.html",{"todo":todo})
        
    else:
        return HttpResponse('permission denied.')
        
    

def share_todo(request):

    if request.method == "GET":

        return HttpResponse('404 not found')

    else:
        form = shareTodoForm(request.POST, request.FILES)
        if not form.is_valid():
            #return HttpResponse('is not valid')
            return render_to_response("errors.html",{"form":form})
            #return HttpResponseRedirect(reverse('detailTodo', args=[23]))
        else:
           
            #1. find user by email or name
            nameoremail = request.POST.get('nameoremail')
            todo_id = request.POST.get('todo_id')
            #nameoremail = 'root'
            #return HttpResponse(todo_id)
            #return HttpResponse(nameoremail)
            user = User.objects.filter(username = nameoremail).first()
            #return HttpResponse(user.id)
            todo = Todo.objects.filter(id = todo_id).first()
            
            if not todo.author.id == request.user.id:
                return HttpResponse('you dont have permission')

            if user:
                auth_user = request.user

                theTodoShares = Shared.objects.filter(
                    todo = todo_id,
                    shared_with = user.id
                ).first()
                
                #return pprint(theTodoShares)
                #return HttpResponse(dir(theTodoShares))
                if auth_user.id == user.id:
                    return HttpResponse('you can not share with yourself')
                elif theTodoShares:
                    return HttpResponse('This Todo already shared with the user')
                else:
                    #store sharing params
                    store = Shared.objects.create(
                        owner=auth_user,
                        shared_with = user)
                    #newTodo.save()
                    store.todo.add(todo)
                    return HttpResponse('you can share with this user')

            else:
                return HttpResponse('user not found')