# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelChoiceField
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm, TempRetForm, \
    PersistentSaveForm, ObjectEditForm, ObjectCreateForm, PrepareRetForm, PreparePSForm
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
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object()
            project.save()
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Приймання на тимчасове зберігання', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'condition': project.condition, 'description': project.description,
                'price': project.price}
        form = TempSaveForm(initial=data)
        return render(request, 'AddOnTs.html', {'form': form})


@csrf_protect
def TempRet(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            return HttpResponseRedirect('prepare')
    if project.attributeassignment_set.filter(approval=False, aim=project).exists():
        return HttpResponse('У цього об’єкта є незатвердженi подii.')
    if request.method == 'POST':
        form = TempRetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Повернення з тимчасового зберiгання', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/activities')
        else:
            return render(request, 'ReturnFromTS.html', {'form': form, 'errors': form.errors})
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'price': project.price, 'note': project.note, 'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'collection': project.collection}
        form = TempSaveForm(initial=data)
        return render(request, 'ReturnFromTS.html', {'form': form})


def GetProject(request):
    act_list = Activity.objects.all()
    return render(request, 'activities.html', {'acts': act_list})


def ApproveProject(request, offset):
    if Activity.objects.get(id=int(offset)).approval == False:
        Activity.objects.get(id=int(offset)).approve()
        return HttpResponse('Успішно затверджено<br><a href="/">На головну</a>')
    else:
        return HttpResponse('Вже затверджено ранiше<br><a href="/">На головну</a>')


@csrf_protect
def ProjectPage(request, id_number):
    if Object.objects.filter(id=int(id_number)).exists():
        project = Object.objects.get(id=int(id_number))
    else:
        return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')

    if not project.attributeassignment_set.filter(approval=True).exists():
        return HttpResponse('Об’єкт не затверджений')

    return_from_tc = False
    getting_on_pc = False
    wire_off = False
    editing = False

    i = project.attributeassignment_set.filter(approval=True).count()-1

    while str(project.attributeassignment_set.filter(approval=True)[i].event_initiator) == 'Editing':
        i -= 1

    status = str(project.attributeassignment_set.filter(approval=True)[i].event_initiator)
    print status
    if status == 'Приймання на тимчасове зберігання':
        return_from_tc = True
        getting_on_pc = True
        editing = True

    if status == 'Приймання на постійне зберігання':
        wire_off = True
        editing = True

    return render(request, 'ProjectPage.html', {'project': project,
                                                'return_from_tc': return_from_tc,
                                                'getting_on_pc': getting_on_pc,
                                                'wire_off': wire_off,
                                                'editing': editing})

@csrf_protect
def AddOnPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object()
            project.save()
    if request.method == 'POST':
        form = PersistentSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Приймання на постійне зберігання', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('')
        else:
            return render(request, 'AddOnPS.html', {'form': form, 'errors': form.errors})
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'price': project.price, 'note': project.note, 'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'collection': project.collection}
        form = PersistentSaveForm(initial=data)
    return render(request, 'AddOnPS.html', {'form': form})


def PrepareRet(request):
    if request.method == 'POST':
        form = PrepareRetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/staff/return/' + cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PrepareRetForm()
        return render(request, 'AddOnTs.html', {'form': form})


def PreparePS(request):
    if request.method == 'POST':
        form = PreparePSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PreparePSForm()
        return render(request, 'AddOnPS.html', {'form': form})

def ActivityPage(request, id_number):
    if Activity.objects.filter(id=int(id_number)).exists():
        act = Activity.objects.get(id=int(id_number))
    else:
        return HttpResponse('Подія не існує.<br>Спробуйте інший id.')

    attrs = act.attributeassignment_set.all()

    return render(request, 'attribute_assign.html', {'attrs': attrs,
                                                     'act': act})



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


