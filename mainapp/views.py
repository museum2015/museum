# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelChoiceField
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm, TempRetForm, \
    PersistentSaveForm, ObjectEditForm, ObjectCreateForm, PrepareRetForm, PreparePSForm, AutForm, PrepareInventoryForm,\
    InventorySaveForm, PreparePStoTSForm, PrepareSpecInventoryForm, FromPStoTSForm, FromTStoPSForm, PrepareTStoPSForm,\
    PrepareWritingOffForm, PrepareSendOnPSForm, WritingOffForm, SendOnPSForm
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
from django.views.generic.edit import UpdateView, CreateView
import ast
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth


# Create your views here.

@csrf_protect
@login_required(login_url='/admin/')
def TempSave(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object()
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Приймання на тимчасове зберігання', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'condition': project.condition, 'condition_descr': project.condition_descr, 'description': project.description,
                'price': project.price}
        form = TempSaveForm(initial=data)

        return render(request, 'AddOnTs.html', {'form': form})

@csrf_protect
@login_required(login_url='/admin/')
def TempRet(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            return HttpResponseRedirect('prepare')
    if project.attributeassignment_set.filter(approval=False, aim=project).exists():
        return HttpResponse('У цього об’єкта є незатвердженi подiї.')
    if request.method == 'POST':
        form = TempRetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Повернення з тимчасового зберiгання', actor=request.user)
            act.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        reason = get_attrib_assigns('Приймання на тимчасове зберігання', project, 'reason')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'condition_descr': project.condition_descr, 'date_creation': project.date_creation,
                'place_of_creation': project.place_of_creation, 'term_back': project.term_back,
                'reason': reason, 'side_1': project.side_1, 'side_2': project.side_2,
                'price': project.price, 'note': project.note, 'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'collection': project.collection}
        form = TempRetForm(initial=data)
        return render(request, 'AddOnTs.html', {'form': form})

@permission_required('mainapp.only_personal_activity', login_url='/admin')
def GetProject(request):
    act_list = Activity.objects.filter(actor=request.user).order_by('time_stamp').reverse()
    if request.user.has_perm('mainapp.all_activity'):
        act_list = Activity.objects.all().order_by('time_stamp').reverse()
    return render(request, 'projects.html', {'acts': act_list})

@login_required(login_url='/admin/')
def ApproveProject(request, offset):
    if Activity.objects.get(id=int(offset)).approval == False:
        Activity.objects.get(id=int(offset)).approve()
        return HttpResponse('Успішно затверджено<br><a href="/">На головну</a>')
    else:
        return HttpResponse('Вже затверджено ранiше<br><a href="/">На головну</a>')

@login_required(login_url='/admin/')
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

def get_attrib_assigns(act_type, project, attribute):
    act = Activity.objects.filter(type=act_type, approval=True)
    a = []
    for i in act:
            b = AttributeAssignment.objects.filter(event_initiator=i, aim=project, attr_name=attribute, actual=True)
            if not b:
                continue
            else:
                a.append(b)
    try:
        return a[0][0].attr_value
    except IndexError:
        return ''

@login_required(login_url='/admin/')
@csrf_protect
def AddOnPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object()
    if request.method == 'POST':
        form = PersistentSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Приймання на постійне зберігання', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnPS.html', {'form': form, 'errors': form.errors})
    else:
        source = get_attrib_assigns('Приймання на тимчасове зберігання', project, 'source')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'can_transport': project.transport_possibility,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'recomm_for_restauration': project.recomm_for_restauration, 'date_creation': project.date_creation,
                'place_of_creation': project.place_of_creation, 'source': source,
                'price': project.price,  'way_of_found': project.way_of_found,
                'transport_possibility': project.transport_possibility, 'fond': project.collection}
        form = PersistentSaveForm(initial=data)
    return render(request, 'AddOnPS.html', {'form': form})

@login_required(login_url='/admin/')
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

@login_required(login_url='/admin/')
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

@login_required(login_url='/admin/')
def ActivityPage(request, id_number):
    if Activity.objects.filter(id=int(id_number)).exists():
        act = Activity.objects.get(id=int(id_number))
        if not (act.actor == request.user or request.user.has_perm('mainapp.all_activity')):
            return HttpResponse('Ви не маєте доступу до цiєi подii')
    else:
        return HttpResponse('Подія не існує.<br>Спробуйте інший id.')

    attrs = act.attributeassignment_set.all()

    return render(request, 'attribute_assign.html', {'attrs': attrs,
                                                     'act': act})

@permission_required('mainapp.see_all_obj', login_url='/admin')
def ObjectList(request):
    qs = Object.objects.all()
    return render(request, 'objects.html', {'objects': qs})

def aut(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = AutForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                username=cd['username']
                password=cd['password']
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("")
            else:
                return render(request, 'index.html', {'form': form})
        else:
            form = AutForm()
            return render(request, 'index.html', {'form': form})
    else:
        return render(request, 'index.html', {'user': request.user.username})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

class ObjectUpdate(UpdateView):
    model = Object
    form_class = ObjectEditForm
    template_name_suffix = '_update_form'

class ObjectCreate(CreateView):
    model = Object
    form_class = ObjectCreateForm
    template_name_suffix = '_create_form'

@login_required(login_url='/admin/')
def PrepareInventory(request):
    if request.method == 'POST':
        form = PrepareInventoryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PrepareInventoryForm()
        return render(request, 'AddOnInventoryBook.html', {'form': form})

@login_required(login_url='/admin/')
@csrf_protect
def AddOnInventorySave(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object()
    if request.method == 'POST':
        form = InventorySaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Інвентарний облік', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnInventoryBook.html', {'form': form, 'errors': form.errors})
    else:
        source = get_attrib_assigns('Приймання на постійне зберігання', project, 'source')
        old_registered_marks = get_attrib_assigns('Приймання на постійне зберігання', project, 'old_registered_marks')
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'recomm_for_restauration': project.recomm_for_restauration, 'date_creation': project.date_creation,
                'place_of_creation': project.place_of_creation, 'note': project.note, 'source': source,
                'price': project.price,  'way_of_found': project.way_of_found, 'PS_code': ps_code,
                'link_on_doc': project.link_on_doc, 'old_registered_marks': old_registered_marks,
                'transport_possibility': project.transport_possibility, 'fond': project.collection}
        form = InventorySaveForm(initial=data)
    return render(request, 'AddOnInventoryBook.html', {'form': form})

@login_required(login_url='/admin/')
def PreparePSToTS(request):
    if request.method == 'POST':
        form = PreparePStoTSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PreparePStoTSForm()
        return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
@csrf_protect
def FromPSToTS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')

    if request.method == 'POST':
        form = FromPStoTSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Видача предметів з Постійного зберігання на Тимчасове зберігання', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'PS_code': ps_code, 'inventory_number': inventory_number,
                }
        form = FromPStoTSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
def PrepareTSToPS(request):
    if request.method == 'POST':
        form = PrepareTStoPSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PrepareTStoPSForm()
        return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
@csrf_protect
def FromTSToPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')

    if request.method == 'POST':
        form = FromTStoPSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Повернення творів з Тимчасового зберігання на Постійне зберігання', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        insurable_value = get_attrib_assigns('Видача предметів з Постійного зберігання на Тимчасове зберігання', project, 'insurable_value')
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        side_1_person_in_charge = get_attrib_assigns('Видача предметів з Постійного зберігання на Тимчасове зберігання', project, 'side_1_person_in_charge')
        side_1_fond_saver = get_attrib_assigns('Видача предметів з Постійного зберігання на Тимчасове зберігання', project, 'side_1_fond_saver')
        side_2_person_in_charge = get_attrib_assigns('Видача предметів з Постійного зберігання на Тимчасове зберігання', project, 'side_2_person_in_charge')
        reason = get_attrib_assigns('Видача предметів з Постійного зберігання на Тимчасове зберігання', project, 'reason')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr, 'side_1': project.side_1,
                'side_2': project.side_2, 'side_1_person_in_charge': side_1_person_in_charge,
                'side_1_fond_saver': side_1_fond_saver, 'side_2_person_in_charge':side_2_person_in_charge,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'PS_code': ps_code, 'inventory_number': inventory_number, 'reason': reason,
                'term_back': project.term_back, 'insurable_value': insurable_value,
                }
        form = FromTStoPSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
def PrepareSendOnPS(request):
    if request.method == 'POST':
        form = PrepareSendOnPSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PrepareSendOnPSForm()
        return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
@csrf_protect
def SendOnPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')

    if request.method == 'POST':
        form = SendOnPSForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Передача на постійне зберігання', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        spec_inventory_numb = get_attrib_assigns('Спеціальний інвентарний облік', project, 'spec_inventory_numb')
        ts_code = get_attrib_assigns('Приймання на тимчасове зберігання', project, 'TS_code')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'technique': project.technique, 'material': project.material,
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'PS_code': ps_code, 'inventory_number': inventory_number, 'spec_inventory_numb': spec_inventory_numb,
                'TS_code': ts_code,
                }
        form = SendOnPSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
def PrepareWritingOff(request):
    if request.method == 'POST':
        form = PrepareWritingOffForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(cd['obj'])
        else:
            return HttpResponseRedirect('/')
    else:
        form = PrepareWritingOffForm()
        return render(request, 'AddOnTs.html', {'form': form})

@login_required(login_url='/admin/')
@csrf_protect
def WritingOff(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')

    if request.method == 'POST':
        form = WritingOffForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Списання (втрата тощо)', actor=request.user)
            act.save()
            project.save()
            for (k, v) in cd.items():
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        spec_inventory_numb = get_attrib_assigns('Спеціальний інвентарний облік', project, 'spec_inventory_numb')
        ts_code = get_attrib_assigns('Приймання на тимчасове зберігання', project, 'TS_code')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'note': project.note, 'PS_code': ps_code, 'inventory_number': inventory_number,
                'spec_inventory_numb': spec_inventory_numb, 'TS_code': ts_code,
                }
        form = WritingOffForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form})
