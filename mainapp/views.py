# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment,  TempRetForm, \
    PersistentSaveForm, AutForm, \
    InventorySaveForm, SpecInventorySaveForm, FromPStoTSForm, FromTStoPSForm,\
    WritingOffForm, SendOnPSForm,\
    PassportForm, XMLForm, recalc, ROOT
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import auth
from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse
from django.views.generic.edit import DeleteView
import lxml.etree as et


# Create your views here.
@csrf_protect
@login_required
def TempSave(request, id_number=0):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != 0:
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object(name='Новий')
    if request.method == 'POST':
        form = TempSaveForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), aim=project, type='Приймання на тимчасове зберігання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.reason = cd['reason']
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form})
    else:
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'author': project.author, 'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'condition': project.condition, 'condition_descr': project.condition_descr, 'description': project.description,
                'price': project.price, 'note': project.note}
        form = TempSaveForm(initial=data)
        return render(request, 'AddOnTs.html', {'form': form, 'label': 'Прийняти об’єкт на ТЗ'})

@csrf_protect
@login_required
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
            act = Activity(time_stamp=dt.now(), aim = project, type='Повернення з тимчасового зберiгання',
                           actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        reason = str(get_attrib_assigns('Приймання на тимчасове зберігання', project, 'reason'))
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'author': project.author, 'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description, 'condition': project.condition,
                'condition_descr': project.condition_descr, 'term_back': project.term_back,
                'reason': reason, 'side_1': project.side_1, 'side_2': project.side_2,
                'price': project.price, 'note': project.note
                }
        form = TempRetForm(initial=data)
        return render(request, 'AddOnTs.html', {'form': form, 'label': 'Повернути об’єкт з ТЗ'})

@permission_required('mainapp.only_personal_activity', login_url='/admin')
def GetProject(request):
    act_list = Activity.objects.filter(actor=request.user).order_by('time_stamp').reverse()
    if request.user.has_perm('mainapp.all_activity'):
        act_list = Activity.objects.all().order_by('time_stamp').reverse()
    return render(request, 'projects.html', {'acts': act_list})

@login_required
def ApproveProject(request, offset):
    if Activity.objects.get(id=int(offset)).approval == False:
        return HttpResponse('Вже відхилено раніше<br><a href="/activities">Назад</a>')
    elif Activity.objects.get(id=int(offset)).approval == True:
        return HttpResponse('Вже затверджено ранiше<br><a href="/activities">Назад</a>')
    else:
        Activity.objects.get(id=int(offset)).approve()
        return HttpResponse('Успішно затверджено<br><a href="/activities">Назад</a>')

@login_required
def RejectProject(request, offset):
    if Activity.objects.get(id=int(offset)).approval == False:
        return HttpResponse('Вже відхилено раніше<br><a href="/activities">Назад</a>')
    else:
        Activity.objects.get(id=int(offset)).reject()
        return HttpResponse('Успішно відхилено<br><a href="/activities">Назад</a>')


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

def get_all_attrib_assigns(act_type, project, attribute):
    act = Activity.objects.filter(type=act_type, approval=True)
    a = []
    for i in act:
            b = AttributeAssignment.objects.filter(event_initiator=i, aim=project, attr_name=attribute, actual=True)
            if not b:
                continue
            else:
                a.append(b)
    i = 0
    c = []
    while i < len(a):
        c.append(a[0][i].attr_value)
    try:
        return c
    except IndexError:
        return ''


def appendlists(list_from, list_to):
    for i in list_from:
        list_to.append(i)
    return list_to


def get_old_attributes(project, attribute):
    ps = get_all_attrib_assigns('Приймання на постійне зберігання', project, attribute)
    inv = get_all_attrib_assigns('Інвентарний облік', project, attribute)
    spec_inv = get_all_attrib_assigns('Спеціальний інвентарний облік', project, attribute)
    res = []
    appendlists(ps, res)
    appendlists(inv, res)
    appendlists(spec_inv, res)
    old_attributes = ''
    for i in res:
        old_attributes.join(',').join(str(i))
    return old_attributes

@login_required
@csrf_protect
def AddOnPS(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object(name='Новий')
    if request.method == 'POST':
        form = PersistentSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), aim = project, type='Приймання на постійне зберігання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        source = get_attrib_assigns('Приймання на тимчасове зберігання', project, 'source')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'author': project.author, 'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'source': source, 'note': project.note,
                'price': project.price,  'way_of_found': project.way_of_found,
                }
        form = PersistentSaveForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Прийняти об’єкт на ПЗ'})

@login_required 
def ActivityPage(request, id_number):
    if Activity.objects.filter(id=int(id_number)).exists():
        act = Activity.objects.get(id=int(id_number))
        if not (act.actor == request.user or request.user.has_perm('mainapp.all_activity')):
            return HttpResponse('Ви не маєте доступу до цiєi подii')
    else:
        return HttpResponse('Подія не існує.<br>Спробуйте інший id.')

    attrs = act.attributeassignment_set.all()
    for k in attrs:
        if k.attr_name == 'material':
            k.attr_value = k.attr_value.decode('unicode-escape')
    return render(request, 'attribute_assign.html', {'attrs': attrs,
                                                     'act': act})

@permission_required('mainapp.see_all_obj', login_url='/admin')
def ObjectList(request):
    qs = list(Object.objects.all())
    add = request.user.has_perm('mainapp.add_new_obj')
    change = request.user.has_perm('mainapp.change_obj')
    remove = request.user.has_perm('mainapp.remove_oobj')
    return render(request, 'objects.html', {'objects': qs,
                                            'user': request.user,
                                            'add': add,
                                            'change': change,
                                            'remove': remove})


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


class ObjectDelete(DeleteView):
    model = Object
    template_name_suffix = '_delete_form'
    success_url = '/objects'


@login_required 
@csrf_protect
def AddOnInventorySave(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object(name='Новий')
    if request.method == 'POST':
        form = InventorySaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), aim = project, type='Інвентарний облік', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        source = get_attrib_assigns('Приймання на постійне зберігання', project, 'source')
        old_registered_marks = get_attrib_assigns('Приймання на постійне зберігання', project, 'old_registered_marks')
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'date_creation': project.date_creation,
                'place_of_creation': project.place_of_creation, 'technique': project.technique,
                'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description, 'transport_possibility': project.transport_possibility,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'recomm_for_restauration': project.recomm_for_restauration, 'note': project.note, 'source': source,
                'price': project.price,  'way_of_found': project.way_of_found, 'PS_code': ps_code,
                'link_on_doc': project.link_on_doc, 'old_registered_marks': old_registered_marks,
                'collection': project.collection}
        form = InventorySaveForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Взяти об’єкт на інвентарний облік'})


@login_required 
@csrf_protect
def AddOnSpecInventorySave(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object(name='Новий')
    if request.method == 'POST':
        form = SpecInventorySaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), aim = project, type='Спеціальний інвентарний облік', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:

        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        mat_person_in_charge = get_attrib_assigns('Інвентарний облік' or 'Приймання на постійне зберігання', project, 'mat_person_in_charge')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'author': project.author, 'date_creation': project.date_creation,
                'place_of_creation': project.place_of_creation,
                'size': project.size, 'description': project.description,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'recomm_for_restauration': project.recomm_for_restauration, 'note': project.note,
                'price': project.price, 'PS_code': ps_code, 'inventory_number': inventory_number,
                'link_on_doc': project.link_on_doc, 'mat_person_in_charge': mat_person_in_charge,
                'storage': project.storage}
        form = SpecInventorySaveForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Взяти об’єкт на спеціальний інвентарний облік'})


@login_required
@csrf_protect
def Passport(request, id_number):
    try:
        project = Object.objects.get(id=int(id_number))
    except ObjectDoesNotExist:
        if id_number != '0':
            return HttpResponse('Об’єкт не існує.<br>Спробуйте інший id.')
        else:
            project = Object(name='Новий')
    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project.save()
            act = Activity(time_stamp=dt.now(), aim = project, type='Науково-уніфікований паспорт', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        collection = get_attrib_assigns('Інвентарний облік', project, 'collection')
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        spec_inventory_numb = get_attrib_assigns('Спеціальний інвентарний облік', project, 'spec_inventory_numb')
        old_inventory_numbers = get_attrib_assigns('Інвентарний облік' or 'Приймання на постійне зберігання',project, 'old_registered_marks')
        date_place_creation = ' '.join([project.date_creation, project.place_of_creation])
        date_place_detection = ' '.join([project.date_detection, project.place_detection])
        date_place_existence = ' '.join([project.date_existence, project.place_existence])
        source = get_attrib_assigns('Приймання на постійне зберігання', project, 'source')
        classify = get_attrib_assigns('Інвентарний облік', project, 'classify')
        typology = get_attrib_assigns('Інвентарний облік', project, 'typology')
        metals = get_attrib_assigns('Спеціальний інвентарний облік', project, 'metals')
        stones = get_attrib_assigns('Спеціальний інвентарний облік', project, 'stones')
        bibliography = get_attrib_assigns('Інвентарний облік', project, 'bibliography')
        data = {'collection': collection, 'PS_code': ps_code, 'inventory_number': inventory_number,
                'spec_inventory_numb': spec_inventory_numb, 'old_inventory_numbers': old_inventory_numbers,
                'identifier': project.identifier, 'storage': project.storage,
                'name': project.name, 'author': project.author, 'date_place_creation': date_place_creation,
                'date_place_detection': date_place_detection, 'date_place_existence': date_place_existence,
                'source': source, 'way_of_found': project.way_of_found, 'link_on_doc': project.link_on_doc,
                'classify': classify, 'typology': typology, 'amount': project.amount,
                'size': project.size, 'material': project.material.decode('unicode-escape').split(', '), 'technique': project.technique,
                'metals': metals, 'stones': stones, 'description': project.description,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'recomm_for_restauration': project.recomm_for_restauration,
                'transport_possibility': project.transport_possibility, 'price': project.price,
                'bibliography': bibliography}
        form = PassportForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Створити науково-уніфікований паспорт об’єкта'})


@login_required
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
            act = Activity(time_stamp=dt.now(), aim = project, type='Видача предметів з Постійного зберігання на Тимчасове зберігання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
                attr_assign.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form, 'errors': form.errors})
    else:
        ps_code = get_attrib_assigns('Приймання на постійне зберігання', project, 'PS_code')
        inventory_number = get_attrib_assigns('Інвентарний облік', project, 'inventory_number')
        data = {'name': project.name, 'is_fragment': project.is_fragment, 'amount': project.amount,
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'author': project.author, 'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'PS_code': ps_code, 'inventory_number': inventory_number,
                }
        form = FromPStoTSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Видати об’єкт з ПЗ на ТЗ'})


@login_required
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
            act = Activity(time_stamp=dt.now(), aim = project, type='Повернення творів з Тимчасового зберігання на Постійне зберігання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
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
                'date_creation': project.date_creation, 'place_of_creation': project.place_of_creation,
                'author': project.author, 'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr, 'side_1': project.side_1,
                'side_2': project.side_2, 'side_1_person_in_charge': side_1_person_in_charge,
                'side_1_fond_saver': side_1_fond_saver, 'side_2_person_in_charge': side_2_person_in_charge,
                'PS_code': ps_code, 'inventory_number': inventory_number, 'reason': reason,
                'term_back': project.term_back, 'insurable_value': insurable_value,
                }
        form = FromTStoPSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Видати об’єкт з ТЗ на ПЗ'})


@login_required
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
            act = Activity(time_stamp=dt.now(), aim = project, type='Передача на постійне зберігання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
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
                'technique': project.technique, 'material': project.material.decode('unicode-escape').split(', '),
                'size': project.size, 'description': project.description, 'note': project.note,
                'condition': project.condition, 'condition_descr': project.condition_descr,
                'PS_code': ps_code, 'inventory_number': inventory_number, 'spec_inventory_numb': spec_inventory_numb,
                'TS_code': ts_code,
                }
        form = SendOnPSForm(initial=data)
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Передати об’єкт на ПЗ'})


@login_required
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
            act = Activity(time_stamp=dt.now(), aim = project, type='Списання', actor=Custom.myUser.objects.get(username=request.user.username))
            act.save()
            project.save()
            for (k, v) in cd.items():
                if k=='material':
                    v = unicode(v[1:-1].replace('u\'', '').replace('\'', ''))
                attr_assign = AttributeAssignment(attr_name=k, attr_value=v, attr_label=form.fields[k].label,
                                                  event_initiator=act, aim=project)
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
    return render(request, 'AddOnTs.html', {'form': form, 'label': 'Списати об’єкт'})

class MyPDFView(View):
    template = 'asshole.html'

    def get(self, request, id_number):
        try:
            project = Object.objects.get(pk=id_number)
        except:
            return HttpResponse('Не існує об\'єкта с таким номером')
        act = Activity.objects.filter(type='Науково-уніфікований паспорт', approval=True).order_by('-time_stamp')
        act = [a for a in act if a.aim == project]
        if not act:
            return HttpResponse('У даного об\'єкта паспорт не заповнений')
        else:
            act = act[0]
        queryset = act.attributeassignment_set.all()
        a = Activity.objects.all().order_by('time_stamp')[0]
        context = {}
        for query in queryset:
            context[query.attr_name] = query.attr_value
        context['date_appear'] = a.time_stamp
        q = context['material']
        try:
            context['create_person'] = act.actor.get_full_name()
            context['create_group'] = act.actor.groups.values_list('name', flat=True)[0]
            context['charge_person'] = context['mat_person_in_charge'][:-1].split(' (')[0]
            context['charge_group'] = context['mat_person_in_charge'][:-1].split(' (')[1]
        except:
            pass
        context['date'] = dt.now()
        context['material'] = q[1:].replace('u\'', '').replace('\'', '').decode('unicode-escape')
        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="passport.pdf",
                                       show_content_in_browser=True,
                                       context=context,
                                       )
        return response

def EditXML(request):
    global ROOT
    if request.method == 'POST':
        form = XMLForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            root = ROOT
            for a in data['choicefield'].split(','):
                root = root.find(a)
            temp = et.SubElement(root, 'choice')
            temp.text = unicode(data['charfield'])
            f = open('museum/materials.xml', 'w')
            temp = et.tostring(ROOT, pretty_print=True, encoding='utf-8', xml_declaration=True)
            f.write(temp)
            f.close()
            recalc()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'AddOnTs.html', {'form': form})
    else:
        form = XMLForm()
    return render(request, "AddOnTs.html", {'form': form})