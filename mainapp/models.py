    # -*- coding: utf-8 -*-
import datetime
import os
from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select, ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import xml.etree.ElementTree as et
from django.forms.extras.widgets import SelectDateWidget
# Create your models here. test

TECHNIQUE_CHOICES = (('', '--------'),)
WAY_OF_FOUND_CHOICES = (('', '--------'),)
COLLECTIONS = (('', '--------'),)
TOPOGRAPHY = (('', '--------'),)
CONDITIONS = (('', '--------'), ('Без пошкоджень', 'Без пошкоджень'), ('Задовільний', 'Задовільний'), ('Незадовільний', 'Незадовільний'))


def get_choice(*args):
    choice = (('', '--------'),)
    root = et.parse('museum/materials.xml').getroot()
    for table in args:
        root = root.find(table)
    for s in root:
        choice += ((s.text, s.text),)
    return choice

def get_image_path(self, filename):
    path = ''.join(["/", filename])
    return path

class Custom:
    class MaterialSelectWidget(MultiWidget):
        def __init__(self, choices, amount):
            widgets = [Select(choices=choices)]
            self.amo = amount
            for i in range(amount-1):
                widgets.append(Select(choices=choices, attrs={'style': 'display:none;'}))
            super(Custom.MaterialSelectWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(',')
            else:
                res = []
                for i in range(self.amo):
                    res.append(None)
                return res

        def format_output(self, rendered_widgets):
            res = u''.join(rendered_widgets)
            return res

    class MaterialSelectField(MultiValueField):
        def __init__(self, choices, amount, *args, **kwargs):
            list_fields = []
            for i in range(amount):
                list_fields.append(fields.ChoiceField(choices=choices))
            super(Custom.MaterialSelectField, self).__init__(list_fields,
                                                             widget=Custom.MaterialSelectWidget(choices, amount),
                                                             *args,
                                                             **kwargs)

        def compress(self, values):
            res = ''
            for value in values:
                if value:
                    res += value
            return res


    class MultiMaterialSelectWidget(MultiWidget):
        def __init__(self):
            widgets = [Custom.MaterialSelectWidget(choices=get_choice('materials', 'precious'), amount=100),
                       Custom.MaterialSelectWidget(choices=get_choice('materials', 'semi-precious'), amount=100),
                       Custom.MaterialSelectWidget(choices=get_choice('materials', 'non-precious'), amount=100)]
            super(Custom.MultiMaterialSelectWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(';')
            else:
                return []

        def format_output(self, rendered_widgets):
            return u'\n<p><label for="id_temp2_0_0">Дорогоцінні: </label><br>' + rendered_widgets[0] + \
                   u'\n<p><label for="id_temp2_1_0">Напів дорогоцінні: </label><br>' + rendered_widgets[1] + \
                   u'\n<p><label for="id_temp2_2_0">Не дорогоцінні: </label><br>' + rendered_widgets[2]

    class MultiMaterialSelectField(MultiValueField):
        def __init__(self, *args, **kwargs):
            list_fields = [Custom.MaterialSelectField(choices=get_choice('materials', 'precious'), amount=100, label='Precious'),
                           Custom.MaterialSelectField(choices=get_choice('materials', 'semi-precious'), amount=100, label='Semi-precious'),
                           Custom.MaterialSelectField(choices=get_choice('materials', 'non-precious'), amount=100, label='Non-precious')]
            super(Custom.MultiMaterialSelectField, self).__init__(list_fields,
                                                                  widget=Custom.MultiMaterialSelectWidget(),
                                                                  *args, **kwargs)

        def compress(self, values):
            result = ';'
            return result.join(values)

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
            list_fields = [Custom.MaterialField(required=True)]
            for i in range(number-1):
                list_fields.append(Custom.MaterialField())
            super(Custom.MultiMaterialField, self).__init__(list_fields, widget=Custom.MultiMaterialWidget(number=number, placeholder1=placeholder1, placeholder2=placeholder2),
                                                            *args, **kwargs)

        def compress(self, values):
            result = ';'
            return result.join(values)

    class TextChoiceWidget(MultiWidget):
        def __init__(self, choices, placeholder1='', size1=10):
            widgets = [TextInput(attrs={'size': size1, 'max_length': 30, 'placeholder': placeholder1}),
                       Select(choices=choices)]
            super(Custom.TextChoiceWidget, self).__init__(widgets)

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

    class TextChoiceField(MultiValueField):
        def __init__(self, choices, placeholder1, size1=10, *args, **kwargs):
            list_fields = [fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices)]
            super(Custom.TextChoiceField, self).__init__(list_fields,
                                                         widget=Custom.TextChoiceWidget(choices=choices, size1=size1, placeholder1=placeholder1),
                                                         *args,
                                                         **kwargs)

        def compress(self, values):
            if values:
                return values[0] + ':' + values[1]
            else:
                return ''

    class ChoiceTextChoiceField(MultiValueField):
        def __init__(self, choices1, choices2, placeholder1):
            list_fields = [fields.ChoiceField(choices=choices1),
                           fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices2)]
            super(Custom.ChoiceTextChoiceField, self).__init__(list_fields,
                                                               widget=Custom.ChoiceTextChoiceWidget(choices1=choices1,
                                                                                                    choices2=choices2,
                                                                                                    placeholder1=placeholder1))
        def compress(self, values):
            if values:
                return values[0] + ':' + values[1] + ':' + values[2]
            else:
                return ''

    class ChoiceTextChoiceWidget(MultiWidget):
        def __init__(self, choices1, choices2, placeholder1='', invisible=True, **kwargs):
            if invisible:
                attrs = {'max_length': 10, 'placeholder': placeholder1, 'style': 'display:none;'}
            else:
                attrs = {'max_length': 10, 'placeholder': placeholder1}
            widgets = [Select(choices=choices1, **kwargs),
                       TextInput(attrs),
                       Select(choices=choices2, **kwargs)]
            super(Custom.ChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(':')
                return res
            else:
                return [None, None, None]

        def format_output(self, rendered_widgets):
            return u''.join(rendered_widgets)

    class MultiChoiceTextChoiceWidget(MultiWidget):
        def __init__(self, number):
            widgets = [Custom.ChoiceTextChoiceWidget(placeholder1='0,2', choices1=get_choice('dimension', 'type'), choices2=get_choice('dimension', 'measurement_unit'), invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceTextChoiceWidget(placeholder1='', choices1=get_choice('dimension', 'type'), choices2=get_choice('dimension', 'measurement_unit'), attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(';')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceTextChoiceField(MultiValueField):
        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceTextChoiceField(choices1=get_choice('dimension', 'type'), choices2=get_choice('dimension', 'measurement_unit'), placeholder1='0.2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceTextChoiceField(choices1=get_choice('dimension', 'type'), choices2=get_choice('dimension', 'measurement_unit'), placeholder1=''))
            super(Custom.MultiChoiceTextChoiceField, self).__init__(list_fields,
                                                                    widget=Custom.MultiChoiceTextChoiceWidget(number),
                                                                    *args,
                                                                    **kwargs)

        def compress(self, values):
            res = ''
            for value in values:
                if value:
                    res += value
            return res


class Object(models.Model):
    collection = models.CharField(max_length=200, default='', null=True)  #
    is_fragment = models.BooleanField(default=False)
    name = models.CharField(max_length=200, default='', null=True)  #
    amount = models.IntegerField(default=0, null=True)  #
    size = models.CharField(max_length=40, default='', null=True)  #
    _class = models.CharField(max_length=200, default='', null=True)  ##
    type = models.CharField(max_length=200, default='', null=True)  ##
    material = models.CharField(max_length=200, default='', null=True)  #
    technique = models.CharField(max_length=200, default='', null=True)  #
    description = models.TextField(max_length=1000, default='', null=True)  #
    identifier = models.CharField(max_length=50, default='', null=True)
    image = models.ImageField(upload_to=get_image_path, default='default.jpg', null=True)
    #image_type = models.CharField(max_length=50, default='', null=True)
    author = models.CharField(max_length=100, default='', null=True)  #
    price = models.CharField(max_length=50, default='', null=True)  #
    mark_on_object = models.CharField(max_length=200, default='', null=True)  ##
    note = models.CharField(max_length=200, default='', null=True)  #
    condition = models.CharField(max_length=100, default='', null=True)  #
    condition_descr = models.CharField(max_length=2000, null=True)
    transport_possibility = models.BooleanField(default=False)  ##
    recomm_for_restauration = models.CharField(max_length=100, default='', null=True)  ##
    restauration_notes = models.CharField(max_length=200, default='', null=True)  ##
    storage = models.CharField(max_length=200, default='', null=True)  #
    place_appellation = models.CharField(max_length=200, default='', null=True)  ##
    is_there = models.CharField(max_length=200, default='', null=True)  ##
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200, default='', null=True)  #
    #link_on_doc = models.CharField(max_length=200)
    #doc_type = models.CharField(max_length=50)
    transferred_from = models.CharField(max_length=200, default='', null=True)  #
    transferred_to = models.CharField(max_length=200, default='', null=True)  #
    term_back = models.DateTimeField(max_length=200, default='2000-02-12 00:00', null=True)  #
    aim_of_receiving_gen = models.CharField(max_length=200, default='', null=True)  #
    #aim_of_receiving = models.ForeignKey(Activity)
    circumst_write_off = models.CharField(max_length=200, default='', null=True)  ##
    reason = models.CharField(max_length=200, default='default.txt', null=True)  #
    source = models.CharField(max_length=200, default='', null=True)  #

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
    attr_value = models.CharField(max_length=200, default='None', null=True)
    actual = models.BooleanField(default=False)
    aim = models.ForeignKey(Object)
    event_initiator = models.ForeignKey(Activity)
    approval = models.BooleanField(default=False)

    def __unicode__(self):
        if self.attr_value:
            return self.attr_name + ' : ' + self.attr_value
        else:
            return self.attr_name

    def approve(self):
        setattr(self.aim, self.attr_name, self.attr_value)
        self.aim.save()
        self.approval = True
        self.actual = True
        for query in self.aim.attributeassignment_set.filter(attr_name=self.attr_name):
            query.actual = False
        self.save()


class TempSaveForm(forms.Form):
    name = Custom.TextChoiceField(choices=get_choice('languages'), label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=1000, label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=get_choice('dimension', 'type'), label='Техніка', required=False)
    material = Custom.MultiMaterialSelectField(label='Матеріали')
    # size_type = forms.CharField(max_length=200, label='Type of size', required=True)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    #size_measurement_unit = forms.CharField(max_length=50, label='Measurement Unit')
    #measurement =
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт приймання на ТЗ)', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 (акт приймання на ТЗ)', required=True)
    #aim_of_receiving_gen = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Мета приймання на ТЗ', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=False)
    reason = forms.FileField(label='Підстава', required=False)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    term_back = forms.DateTimeField(widget=SelectDateWidget)
    code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    #date_write_TS = forms.DateTimeField(input_formats=['%Y-%m-%d'],label='Date of writing in the book of TS')

    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=False) #
    #ne nado, v activity est' #writing_person = forms.CharField(max_length=50, label='Person who writes is TS book')
    #return_mark = forms.BooleanField(label='Is it returned?')


class InitialTempSaveForm(forms.Form):
    obj = forms.ModelChoiceField(queryset=Object.objects.all())


class TempRetForm(forms.Form):
    choices = (
        ('returned', 'Повернутий з тимчасового збереження'),
        ('add on PS', 'Поставити об’єкт на постійне збереження ')
    )
    name = Custom.TextChoiceField(choices=get_choice('languages'), label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=None, label='Кількість', required=True)
    #date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    #place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True) #
    technique = forms.ChoiceField(choices=get_choice('dimension', 'type'), label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField(label='Матеріал')
    # size_type = forms.CharField(max_length=200, label='Type of size', required=True)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea)
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 450px;"}))
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': 'margin: 0px; height: 252px; width: 450px;'}))
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    term_back = forms.DateTimeField(widget=SelectDateWidget)
    reason = forms.FileField(label='Підстава', required=False)
    side_1 = forms.CharField(max_length=100, label='Сторона 1 (акт повернення з ТЗ)', required=True)
    side_2 = forms.CharField(max_length=100, label='Сторона 2 (акт повернення з ТЗ)', required=True)
    return_mark = forms.ChoiceField(choices=choices, required=True, label='Позначка про повернення предмета або переведення до музейного зібрання (ПЗ) у книзі ТЗ')
    save_place = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True) #


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
    name = Custom.TextChoiceField(choices=get_choice('languages'), label='Назва', placeholder1='') #
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False) #
    amount = forms.IntegerField(label='Кількість', required=True) #
    #date_creation = forms.CharField(label='Дата створення предмета', required=True)
    # place_of_creating = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True) #
    technique = forms.ChoiceField(choices=get_choice('dimension', 'type'), label='Техніка', required=True) #
    material = Custom.MultiMaterialSelectField(label='Матеріал') #
    size = Custom.MultiChoiceTextChoiceField(label='Розміри') #
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea) #
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True) #
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea) #
    can_transport = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True) #
    recommandation_rest = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації') #
    price = forms.CharField(max_length=40, label='Вартість', required=True) #
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea) #
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True) #
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=False) #
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True) #
    link_on_doc = forms.FileField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=False) #
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт ПЗ)', required=True) #
    side_2 = forms.CharField(max_length=209, label='Сторона 2 (акт ПЗ)', required=True) #
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа', required=False)
    save_place = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True) #
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)
    inventory_number = forms.CharField(max_length=200, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=200, label='Спеціальний інвентарний номер', required=True)


class PrepareInventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareInventoryForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Приймання на постійне зберігання':
                objlist.append(project)
        objects = []
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class InventorySaveForm(forms.Form):
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=get_choice('languages'), label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    #date_creation = forms.CharField(label='Дата створення предмета', required=True)
    # place_of_creating = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    #date_detection = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Дата знаходження', required=True)
    #place_detection = forms.CharField(max_length=200, label='Місце виявлення')
    #date_existence = forms.CharField(max_length=200, label='Дата побутування')
    #place_existence = forms.CharField(max_length=200, label='Місце побутування')
    technique = forms.CharField(max_length=200, label='Техніка', required=True)
    material = Custom.MultiMaterialField(label='Матеріал', placeholder1='Золото', placeholder2='10г')
    # size_type = forms.CharField(max_length=200, label='Type of size', required=True)
    size = Custom.MultiMaterialField(number=3, label='Розміри', placeholder1='Ширина', placeholder2='2м')
    mark_on_object = forms.CharField(max_length=200, label='Позначки на предметі ')
    #classification = forms.CharField(max_length=200, label='Класифікація')
    #typology = forms.CharField(max_length=200, label='Типологія')
    description = forms.CharField(max_length=200, label='Опис предмета', required=True)
    #bibliography = forms.CharField(max_length=200, label='Бібліографія')
    condition = forms.CharField(max_length=200, label='Стан збереженості(тип)', required=True)
    condition_descr = forms.CharField(max_length=200, label='Опис стану збереженості', required=True)
    can_transport = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recommandation_rest = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = forms.CharField(max_length=200, label='Примітка', required=True)
    inventory_number = forms.CharField(max_length=100, label='Інвентарний номер')
    #дата запису до інвентарної книги буде в Activity
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.CharField(max_length=200, label='Спосіб надходження ', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер')
    fond = forms.CharField(max_length=200, label='Фонд (колекція, відділ)', required=True)
    mat_person_in_charge = forms.CharField(max_length=50, label='Матеріально-відповідальна особа', required=True)
    save_place = forms.CharField(max_length=200, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)
    #особа яка здійснила запис також в Activity


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


class AutForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логiн:')
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Пароль:')

