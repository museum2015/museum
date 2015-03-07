from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm ,TempRetForm , PersistentSaveForm
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_protect
@login_required
def TempSave(request):
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on temporary storage', actor=request.user)
            act.save()
            obj = Object()
            obj.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=obj)
                attr_assign.save()
            return HttpResponse('ok')
        return HttpResponse('ne ok')
    else:
        form = TempSaveForm()
    return render(request, 'AddOnTs.html', {'form': form})


@csrf_protect
def TempRet(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Object does not exist.<br>Try with another id_number.')
    if str(project.attributeassignment_set.filter(approval=False, aim=project)[0]):
        return HttpResponse('This object has not approved activity<br> Please, confirm they')
    act = Activity(time_stamp=dt.now(), type='Getting from temporary storage', actor=request.user)
    act.save()
    for temp in project.attributeassignment_set.filter(approval=True, aim=project):
        if str(temp.event_initiator) == 'Getting on temporary storage':
            attr_assign = AttributeAssignment(attr_name=temp.attr_name, event_initiator=act, aim=project)
            attr_assign.save()
    return redirect('/')


def GetProject(request):
    act_list = Activity.objects.filter(approval=False)
    return render(request, 'projects.html', {'acts': act_list})


def ApproveProject(request, offset):
    Activity.objects.get(id=int(offset)).approve()
    return HttpResponse('Succesfully approved')


@csrf_protect
def ProjectPage(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Object does not exist.<br>Try with another id_number.')
    return_from_tc = False
    getting_on_pc = False
    wire_off = False
    editing = False

    i = 0
    while project.attributeassignment_set.filter(approval=True)[i].event_initiator == 'Editing':
        i += 1
    status = str(project.attributeassignment_set.filter(approval=True)[i].event_initiator)

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
def AddOnPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Object does not exist.<br>Try with another id_number.')
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
        return HttpResponse('ne ok')
    else:
        form = PersistentSaveForm()
    return render(request, 'AddOnPS.html', {'form': form})
