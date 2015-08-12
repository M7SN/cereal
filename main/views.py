from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from main.models import Cereal, Manufacturer
from main.forms import CerealSearch, CreateCereal, UserSignUp, UserLogin

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

print Manufacturer
# Create your views here.

def cereal_list_template(request):

    manufacturers = Manufacturer.objects.all()

    context = {}

    context['manufacturers'] = manufacturers

    return render(request, 'cereal_list.html', context)

def cereal_list_template2(request):

    manufacturers = Manufacturer.objects.all()

    context = {}

    manufacturer_cereal = {}

    for manufacturer in manufacturers:
        cereals = manufacturer.cereal_set.filter(name__contains="A")

        manufacturer.name = { manufacturer.name : cereals }

        manufacturer_cereal.update(manufacturer.name)

    context['manufacturer_cereal'] = manufacturer_cereal

    return render_to_response('cereal_list2.html', context, context_instance=RequestContext(request))

    #return render(request, 'cereal_list2.html', context)

    # cereal_string = ""

    # for manufacturer in manufacturers:

    #     cereal_string += "<h4>%s</h4>" % manufacturer

    #     for cereal in manufacturer.cereal_set.all():
    #         cereal_string += "%s </br>" % cereal.name

    # return HttpResponse(cereal_string)

def cereal_detail(request, pk):

    context = {}

    cereal = Cereal.objects.get(pk=pk)

    context['cereal'] = cereal

    return render_to_response('cereal_detail.html', context, context_instance=RequestContext(request))

def cereal_search(request, cereal):

    cereals = Cereal.objects.filter(name__istartswith=cereal)

    cereal_string = ""

    for cereal in cereals:
        cereal_string += "<b>Cereal:</b>%s, <b>Manufacturer:</b>%s" % (cereal.name, cereal.manufacturer)

        print cereal


    return HttpResponse(cereal_string)

def cereal_create(request):

    context = {}

    form = CreateCereal()
    context['form'] = form

    if request.method == 'POST':
        form = CreateCereal(request.POST)

        if form.is_valid():
            form.save()

            context['valid'] = "Cereal Saved"

    elif request.method == 'GET':
        context['valid'] = form.errors


    return render_to_response('cereal_create.html', context, context_instance=RequestContext(request))

def get_cereal_search(request):

    #print request.GET['cereal']

    cereal = request.GET.get('cereal', 'None')

    cereals = Cereal.objects.filter(name__istartswith=cereal)

    cereal_string = """
    <form action='/get_cereal_search/' method='GET'>
    
    Cereal:
    </br>
    <input type="text" name="cereal" >

    </br>
    <input type="submit" value="Submit" >

    </form>
    """

    for cereal in cereals:
        cereal_string += "<b>Cereal:</b>%s, </br><b>Manufacturer:</b>%s </br>" % (cereal.name, cereal.manufacturer)
        for nutrition in cereal.nutrition.nutrition_list():
            cereal_string += "%s </br>" % nutrition

    return HttpResponse(cereal_string)

def manufact_list_view(request):

    manufacturers = Manufacturer.objects.all()

    manufact_string = ""

    for manufacturer in manufacturers:

        manufact_string += "<h4>%s</h4>" % manufacturer

    return HttpResponse(manufact_string)

def manufact_search(request, manufacturer):

    manufacturers = Manufacturer.objects.filter(name__istartswith=manufacturer)

    manufact_string = ""

    for manufacturer in manufacturers:
        manufact_string += "<b>Manufacturer:</b>%s, </br>" % (manufacturer.name)

        print manufacturer


    return HttpResponse(manufact_string)

def get_manufact_search(request):

    manufacturer = request.GET.get('manufacturer', 'None')

    manufacturers = Manufacturer.objects.filter(name__istartswith=manufacturer)

    manufact_string = """
    <form action='/get_manufact_search/' method='GET'>

    Manufacturer:
    </br>
    <input type="text" name="manufacturer" >

    </br>
    <input type="submit" value="Submit">

    </form>
    </br>
    """

    for manufacturer in manufacturers:
        manufact_string += "<b><em>%s</em></b></br>" % manufacturer.name
        cereals = manufacturer.cereal_set.all()
        for cereal in cereals:
            manufact_string += "<b>Cereal:</b>%s</br>" % (cereal.name)


    return HttpResponse(manufact_string)


def form_view(request):

        context = {}

        get = request.GET
        post = request.POST

        context['get'] = get
        context['post'] = post

        if request.method == "POST":
            cereal = request.POST.get('cereal', None)

            cereals = Cereal.objects.filter(name__startswith=cereal)

            context['cereals'] = cereals

        elif request.method == "GET":
            context['method'] = 'The method was GET'


        return render_to_response('form_view.html', context, context_instance=RequestContext(request))

from main.forms import CerealSearch

def form_view2(request):

        context = {}

        get = request.GET
        post = request.POST

        context['get'] = get
        context['post'] = post

        form = CerealSearch()
        context['form'] = form

        if request.method == "POST":
            form = CerealSearch(request.POST)

            if form.is_valid():
                # cereal = request.POST.get('name', None)
                cereal = form.cleaned_data['name']
                cereals = Cereal.objects.filter(name__startswith=cereal)

                context['cereals'] = cereals
                context['valid'] = "The Form Was Valid"

            else:
                context['valid'] = form.errors

        elif request.method == "GET":
            context['method'] = 'The method was GET'


        return render_to_response('form_view2.html', context, context_instance=RequestContext(request))

def signup(request):

    context = {}

    form = UserSignUp()
    context['form'] = form

    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                User.objects.create_user(name, email, password)
                context['valid'] = "Thank You For Signing Up!"

                auth_user = authenticate(username=name, password=password)
                login(request, auth_user)
                return HttpResponseRedirect('/cereal_list_template/')

            except IntegrityError, e:
                context['valid'] = "A User With That Name Already Exists"

        else:
            context['valid'] = form.errors

    if request.method == 'GET':
        context['valid'] = "Please Sign Up!"

    return render_to_response('signup.html', context, context_instance=RequestContext(request))

def home(request):

    context = {}

    manus = Manufacturer.objects.all()
    context['manus'] = manus

    return render_to_response('home.html', context, context_instance=RequestContext(request))

def login_view(request):

    context = {}

    context['form'] = UserLogin()

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    auth_user = authenticate(username=username, password=password)

    if auth_user is not None:
        if auth_user.is_active:
            login(request, auth_user)
            context['valid'] = "Login Successful"

            return HttpResponseRedirect('/home/')
        else:
            context['valid'] = "Please Enter User Name"

    return render_to_response('login.html', context, context_instance=RequestContext(request))

def logout_view(request):

    logout(request)

    return HttpResponseRedirect('/login_view/')



