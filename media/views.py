from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic, Message
from .forms import CreateRoomForm, RegisterForm, TopicForm
from django.contrib.auth.hashers import make_password


# Create your views here.
def home_view(request):
    q = request.GET.get("q") if request.GET.get("q") else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(description__icontains=q)
        | Q(host__username__icontains=q)
        | Q(name__icontains=q)
    )
    topics = Topic.objects.all()
    # return HttpResponse("<h1>Hello world</h1>")
    context = {
        "rooms": rooms,
        "topics": topics,
    }
    return render(request, "home.html", context)


@login_required(login_url="media:login")
def my_rooms_view(request):
    rooms = Room.objects.filter(host=request.user)
    topics = Topic.objects.all()
    # return HttpResponse("<h1>Hello world</h1>")
    context = {
        "rooms": rooms,
        "topics": topics,
    }
    return render(request, "home.html", context)


def room_view(request, pk):
    # return HttpResponse("<h1>ROOM</h1>")
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    if request.method == "POST":
        Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("message")
        )
        room.participants.add(request.user)
        return redirect("media:room", pk=room.id)
    context = {
        "room": room,
        "room_messages": messages,
    }
    return render(request, "room.html", context)


@login_required(login_url="media:login")
def create_room(request):
    form = CreateRoomForm()
    if request.method == "POST":
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("media:home")
    context = {
        "form": form,
        "page": "create",
    }
    return render(request, "login.html", context)


@login_required(login_url="media:login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = CreateRoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("YOU ARE NOT ALLOWED HERE !")

    if request.method == "POST":
        form = CreateRoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.info(request, "Room info been updated !!!")
            return redirect("media:home")
    context = {
        "page": "update",
        "form": form,
    }
    return render(request, "login.html", context)


@login_required(login_url="media:login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("YOU ARE NOT ALLOWED HERE !")

    if request.method == "POST":
        room.delete()
        return redirect("media:home")
    return render(
        request,
        "login.html",
        {
            "page": "delete",
            "obj": room,
        },
    )


def login_view(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("media:home")
            else:
                messages.error(request, "Username or Password was Incorrect")
                return redirect("media:login")

        return render(
            request,
            "login.html",
            {
                "page": "login",
            },
        )
    else:
        return redirect("media:home")


def logout_view(request):
    logout(request)
    return redirect("media:home")


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if password == confirm_password:
                not_user = form.save(commit=False)
                not_user.password = make_password(password)
                not_user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect("media:home")

            else:
                messages.error(request, "Password and Confirm Password don't match !!!")
                return redirect("media:register")
        else:
            messages.error(request, "username already been used !!!")
            return redirect("media:register")

    return render(
        request,
        "login.html",
        {
            "page": "register",
            "form": form,
        },
    )


@login_required(login_url="media:login")
def add_topic_view(request):
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if Topic.objects.filter(name=name).exists():
                # print("This Topic already exists !!!")
                messages.info(request, "This Topic already exists !!!")
                return redirect("media:add_topic")
            form.save()
            return redirect("media:create_room")
    context = {
        "page": "topic",
        "form": form,
    }
    return render(request, "login.html", context)
