from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm, TempRetForm, \
    PersistentSaveForm, ObjectEditForm, ObjectCreateForm
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
from django.views.generic.edit import UpdateView, CreateView
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_protect
def TempSave(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Object does not exist.<br>Try with another id_number.')
        else:
            project = Object()
            project.save()
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on temporary storage', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponse('ok')
        return HttpResponse('ne ok')
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'condition': project.condition, 'description': project.description,
                'price': project.price}
        form = TempSaveForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form})


@csrf_protect
def TempRet(request, id_number=0):
    if Object.objects.get(id=int(id_number)).exists():
        project = Object.objects.get(id=int(id_number))
    else:
        if id_number != 0:
            return HttpResponse('Object does not exist.<br>Try with another id_number.')
        else:
            project = Object()
            project.save()

    if project.attributeassignment_set.filter(approval=False, aim=project).exists():
             return HttpResponse('This object has not approved activity<br> Please, confirm they')
    if request.method == 'POST':
        form = TempRetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting from temporary storage', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponse('ok')
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'price': project.price, 'note': project.note, 'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'collection': project.collection}
        form = TempSaveForm(initial=data)
    return render(request, 'AddOnTS.html', {'form': form})


def GetProject(request):
    act_list = Activity.objects.filter(approval=False)
    return render(request, 'projects.html', {'acts': act_list})


def ApproveProject(request, offset):
    Activity.objects.get(id=int(offset)).approve()
    return HttpResponse('Succesfully approved<br><a href="/projects/'+
                        str(Activity.objects.get(id=int(offset)).attributeassignment_set.all()[0].aim.id)+
                        '/">Personal page</a>')


@csrf_protect
def ProjectPage(request, id_number):
    if Object.objects.filter(id=int(id_number)).exists():
        project = Object.objects.get(id=int(id_number))
    else:
        return HttpResponse('Object does not exist.<br>Try with another id_number.')

    if not project.attributeassignment_set.filter(approval=True).exists():
        return HttpResponse('This object is not approved')

    return_from_tc = False
    getting_on_pc = False
    wire_off = False
    editing = False

    i = project.attributeassignment_set.filter(approval=True).count()-1

    while str(project.attributeassignment_set.filter(approval=True)[i].event_initiator) == 'Editing':
        i -= 1

    status = str(project.attributeassignment_set.filter(approval=True)[i].event_initiator)
    print status
    if status == 'Getting on temporary storage':
        return_from_tc = True
        getting_on_pc = True
        editing = True

    if status == 'Getting on persistent storage':
        wire_off = True
        editing = True

    return render(request, 'ProjectPage.html', {'project': project,
                                                'return_from_tc': return_from_tc,
                                                'getting_on_pc': getting_on_pc,
                                                'wire_off': wire_off,
                                                'editing': editing})

@csrf_protect
def AddOnPS(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Object does not exist.<br>Try with another id_number.')
        else:
            project = Object()
            project.save()
    if request.method == 'POST':
        form = PersistentSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on persistent storage', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponse('ok')
        return HttpResponse(form.errors)
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'price': project.price, 'note': project.note, 'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'collection': project.collection}
        form = PersistentSaveForm(initial=data)
    return render(request, 'AddOnPS.html', {'form': form})


class ObjectUpdate(UpdateView):
    model = Object
    form_class = ObjectEditForm
    template_name_suffix = '_update_form'


class ObjectCreate(CreateView):
    model = Object
    form_class = ObjectCreateForm
    template_name_suffix = '_create_form'


def MainPage(request):
    return render(request, 'index.html', {})


def ShowAllActivities(request):
    return render(request, 'activities.html', {})


