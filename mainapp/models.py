# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select, ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your models here. test


def get_image_path(self, filename):
    path = ''.join(["/", filename])
    return path


class Custom:
    class MaterialWidget(MultiWidget):
        def __init__(self, placeholder1='', placeholder2='', size1=10, size2=10):
            widgets = [TextInput(attrs={'size': size1, 'max_length': 30, 'placeholder': placeholder1}),
                       TextInput(attrs={'size': size2, 'max_length': 10, 'placeholder': placeholder2})]
            super(Custom.MaterialWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(':')
                return res
            else:
                return [None, None]

        def format_output(self, rendered_widgets):
            dd = '<br>'
            res = u''.join(rendered_widgets)
            return dd+res

    class MaterialField(MultiValueField):
        def __init__(self, size1=10, size2=30, *args, **kwargs):
            list_fields = [fields.CharField(max_length=30),
                           fields.CharField(max_length=30)]
            super(Custom.MaterialField, self).__init__(list_fields, widget=Custom.MaterialWidget(size1, size2), *args,
                                                       **kwargs)

        def compress(self, values):
            if values:
                return values[0] + ':' + values[1]
            else:
                return ''


    class MultiMaterialWidget(MultiWidget):
        def __init__(self, placeholder1, placeholder2, number=5):
            widgets = [Custom.MaterialWidget(placeholder1=placeholder1, placeholder2=placeholder2)]
            for i in range(number-1):
                widgets.append(Custom.MaterialWidget())
            super(Custom.MultiMaterialWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(';')
            else:
                return []

        def format_output(self, rendered_widgets):
            res = u''.join(rendered_widgets)
            return res+'<br>'

    class MultiMaterialField(MultiValueField):
        def __init__(self, placeholder1='Золото', placeholder2='10г', number=5, *args, **kwargs):
            list_fields = []
            for i in range(number):
                list_fields.append(Custom.MaterialField())
            super(Custom.MultiMaterialField, self).__init__(list_fields, widget=Custom.MultiMaterialWidget(number=number, placeholder1=placeholder1, placeholder2=placeholder2),
                                                            *args, **kwargs)

        def compress(self, values):
            result = ';'
            return result.join(values)


class Object(models.Model):
    collection = models.CharField(max_length=200, default='')  #
    is_fragment = models.BooleanField(default=False)
    name = models.CharField(max_length=200, default='')  #
    #name_lang = models.CharField(max_length=200, default='')  ##
    #name_type = models.CharField(max_length=200, default='')
    amount = models.IntegerField(default=0)  #
    # size_type = models.CharField(max_length=200, default='') #
    size = models.CharField(max_length=40, default='')  #
    #size_measurement_unit = models.CharField(max_length=200, default='') #
    _class = models.CharField(max_length=200, default='')  ##
    type = models.CharField(max_length=200, default='')  ##
    material = models.CharField(max_length=200, default='')  #
    #measurement = models.CharField(max_length=400, default='')
    technique = models.CharField(max_length=200, default='')  #
    description = models.TextField(max_length=1000, default='')  #
    #description_lang = models.CharField(max_length=50, default='')  ##
    #description_type = models.CharField(max_length=200, default='')  ##
    identifier = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to=get_image_path, default='default.jpg')
    #image_type = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=100, default='')  #
    #author_type = models.CharField(max_length=50, default='')  ##
    price = models.CharField(max_length=50, default='')  #
    #price_type = models.CharField(max_length=50, default='')  ##
    mark_on_object = models.CharField(max_length=200, default='')  ##
    #mark_type = models.CharField(max_length=50, default='')  ##
    note = models.CharField(max_length=200, default='')  #
    #note_type = models.CharField(max_length=50, default='')  ##
    #mark_note_lang = models.CharField(max_length=30, default='')  ##
    #condition_descr=models.CharField(max_length=500, default='')#
    condition = models.CharField(max_length=100, default='')  #
    transport_possibility = models.BooleanField(default=False)  ##
    recomm_for_restauration = models.CharField(max_length=100, default='')  ##
    restauration_notes = models.CharField(max_length=200, default='')  ##
    storage = models.CharField(max_length=200, default='')  #
    place_appellation = models.CharField(max_length=200, default='')  ##
    is_there = models.CharField(max_length=200, default='')  ##
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200, default='')  #
    #link_on_doc = models.CharField(max_length=200)
    #doc_type = models.CharField(max_length=50)
    transferred_from = models.CharField(max_length=200, default='')  #
    transferred_to = models.CharField(max_length=200, default='')  #
    term_back = models.DateTimeField(max_length=200, default='2000-02-12 00:00')  #
    aim_of_receiving_gen = models.CharField(max_length=200, default='')  #
    #aim_of_receiving = models.ForeignKey(Activity)
    circumst_write_off = models.CharField(max_length=200, default='')  ##
    reason = models.CharField(max_length=200, default='')  #
    source = models.CharField(max_length=200, default='')  #

    def __unicode__(self):
        return self.name + ' (' + self.identifier + ')'

    def status(self):
        if not self.attributeassignment_set.filter(approval=True):
            status = 'Пустий об’єкт'
        else:
            i = self.attributeassignment_set.filter(approval=True).count()-1
            while str(self.attributeassignment_set.filter(approval=True)[i].event_initiator) == 'Editing':
                i -= 1
            status = str(self.attributeassignment_set.filter(approval=True)[i].event_initiator)
        return status

class Activity(models.Model):
    time_stamp = models.DateTimeField(default='2000-02-12 00:00')
    type = models.CharField(max_length=30)
    actor = models.ForeignKey(User)
    approval = models.BooleanField(default=False)

    def __unicode__(self):
        try:
            return self.type
        except IndexError:
            return 'UndefinedActivity'

    def approve(self):
        for attrib in self.attributeassignment_set.all():
            attrib.approve()
        self.approval = True
        self.save()

    def aim(self):
        return self.attributeassignment_set.all()[:1].get().aim

class AttributeAssignment(models.Model):
    attr_name = models.CharField(max_length=40)
    attr_value = models.CharField(max_length=200)
    aim = models.ForeignKey(Object)
    event_initiator = models.ForeignKey(Activity)
    approval = models.BooleanField(default=False)

    def __unicode__(self):
        return self.attr_name + ' : ' + self.attr_value

    def approve(self):
        setattr(self.aim, self.attr_name, self.attr_value)
        self.aim.save()
        self.approval = True
        self.save()


class TempSaveForm(forms.Form):
    name = forms.CharField(max_length=200, label='Назва предмета', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=True)
    amount = forms.IntegerField(max_value=1000, label='Кількість', required=True)
    #date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    #place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.CharField(max_length=200, label='Техніка', required=True)
    material = Custom.MultiMaterialField(required=True, label='Матеріал', placeholder1='Золото', placeholder2='10г')
    # size_type = forms.CharField(max_length=200, label='Type of size', required=True)
    size = Custom.MultiMaterialField(number=3, required=True, label='Розміри', placeholder1='Ширина', placeholder2='2м')
    #size_measurement_unit = forms.CharField(max_length=50, label='Measurement Unit')
    #measurement =
    condition = forms.CharField(max_length=200, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=200, label='Опис стану збереженості', required=True)
    description = forms.CharField(max_length=500, label='Опис предмета', required=True)
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    note = forms.CharField(max_length=200, label='Примітка', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт приймання на ТЗ)', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 (акт приймання на ТЗ)', required=True)
    aim_of_receiving_gen = forms.CharField(max_length=200, label='Мета приймання на ТЗ', required=True)
    way_of_found = forms.CharField(max_length=200, label='Спосіб надходження', required=True)
    reason = forms.CharField(max_length=200, label='Підстава', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    collection = forms.CharField(max_length=200, label='Фонд (колекція, відділ)', required=True)
    term_back = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Термін повернення(до якої дати)', required=True)
    code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    #date_write_TS = forms.DateTimeField(input_formats=['%Y-%m-%d'],label='Date of writing in the book of TS')

    mat_person_in_charge = forms.CharField(max_length=50, label='Матеріально-відповідальна особа', required=True)
    storage = forms.CharField(max_length=200, label='Фізичне місце збереження (топографія)', required=True) #
    #ne nado, v activity est' #writing_person = forms.CharField(max_length=50, label='Person who writes is TS book')
    #return_mark = forms.BooleanField(label='Is it returned?')


class InitialTempSaveForm(forms.Form):
    obj = forms.ModelChoiceField(queryset=Object.objects.all())


class TempRetForm(forms.Form):
    choices = (
        ('returned', 'Повернутий з тимчасового збереження'),
        ('add on PS', 'Поставити об’єкт на постійне збереження ')
    )
    name = forms.CharField(max_length=200, label='Назва предмета', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=True)
    amount = forms.IntegerField(max_value=None, label='Кількість', required=True)
    #date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    #place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True) #
    technique = forms.CharField(max_length=200, label='Техніка', required=True)
    material = Custom.MultiMaterialField(required=True, label='Матеріал') #
#   size_type = forms.CharField(max_length=200, label='Type of size', required=True) #
    size = Custom.MultiMaterialField(number=3, required=True, label='Розміри')
    condition = forms.CharField(max_length=200, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=200, label='Опис стану збереженості', required=True)
    description = forms.CharField(max_length=500, label='Опис предмета', required=True)
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    term_back = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Термін повернення(до якої дати)', required=True)
    note = forms.CharField(max_length=200, label='Примітка', required=True)
    reason = forms.CharField(max_length=200, label='Підстава', required=True)
    side_1 = forms.CharField(max_length=100, label='Сторона 1 (акт повернення з ТЗ)', required=True)
    side_2 = forms.CharField(max_length=100, label='Сторона 2 (акт повернення з ТЗ)', required=True)
    return_mark = forms.ChoiceField(choices=choices, required=True, label='Позначка про повернення предмета або переведення до музейного зібрання (ПЗ) у книзі ТЗ')
    save_place = forms.CharField(max_length=200, label='Фізичне місце збереження (топографія)', required=True)

class PrepareRetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareRetForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Приймання на тимчасове зберігання':
                objlist.append(project)
        objects = [(o.id, o.__unicode__()) for o in objlist]
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')

class PreparePSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreparePSForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() != 'Пустий об’єкт':
                objlist.append(project)
        objects = [(0, 'Новий об’єкт')]
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')

class PersistentSaveForm(forms.Form):
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = forms.CharField(max_length=200, label='Назва предмета', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=True)
    amount = forms.IntegerField(label='Кількість', required=True)
    #date_creation = forms.CharField(label='Дата створення предмета', required=True)
    # place_of_creating = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.CharField(max_length=200, label='Техніка', required=True)
    material = Custom.MultiMaterialField(required=True, label='Матеріал')
    size = Custom.MultiMaterialField(number=3, required=True, label='Розміри')
    description = forms.CharField(max_length=200, label='Опис предмета', required=True)
    condition = forms.CharField(max_length=200, label='Стан збереженості(тип)', required=True)
    can_transport = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recommandation_rest = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    conservation_descr = forms.CharField(max_length=200, label='Опис стану збереженості', required=True)
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = forms.CharField(max_length=200, label='Примітка', required=True)
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.CharField(max_length=200, label='Спосіб надходження ', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт ПЗ)', required=True)
    side_2 = forms.CharField(max_length=209, label='Сторона 2 (акт ПЗ)', required=True)
    fond = forms.CharField(max_length=200, label='Фонд (колекція, відділ)', required=True)
    mat_person_in_charge = forms.CharField(max_length=50, label='Матеріально-відповідальна особа', required=True)
    save_place = forms.CharField(max_length=200, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)
    inventory_number = forms.CharField(max_length=200, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=200, label='Спеціальний інвентарний номер', required=True)


class ObjectEditForm(ModelForm):
    class Meta:
        model = Object
    material = Custom.MultiMaterialField()
    size = Custom.MultiMaterialField(number=3)


class ObjectCreateForm(ModelForm):
    class Meta:
        model = Object
    material = Custom.MultiMaterialField()
    size = Custom.MultiMaterialField(number=3)