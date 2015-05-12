# -*- coding: utf-8 -*-
import datetime
import os
from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select, ModelForm, SelectMultiple
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
import lxml.etree as et
from bootstrap3_datetime.widgets import DateTimePicker
# Create your models here. test

ROOT = et.parse('museum/materials.xml').getroot()


def validate_all_choices(value):
    pass


def get_choice(root, level=0, *args):
    choice = ()
    for a in args:
        root = root.find(a)
    for s in root:
        prefix = ''
        if s.getchildren():
            for i in range(level):
                prefix += '__'
            choice += ((prefix+s.attrib['label'], get_choice(s, level=level+1)), )
        else:
            for i in range(level):
                prefix += '&nbsp;&nbsp;'
            choice += ((s.text, mark_safe(prefix+s.text)),)
    if not level:
        return (('', ''),) + choice
    else:
        return choice

WEIGHT_CHOICES = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
MATERIAL_CHOICES = get_choice(ROOT, 0, 'materials')
LANGUAGE_CHOICES = get_choice(ROOT, 0, 'languages')

TECHNIQUE_CHOICES = (('', ''), ('Техніка 1', 'Техніка 1'),)
WAY_OF_FOUND_CHOICES = (('', ''), ('Розкопки', 'Розкопки'),)
AIMS = (('', ''),)
PLACE = (('', ''), ('На місці', 'На місці'), ('За межами фондосховища', 'За межами фондосховища'),
         ('За межами музею', 'За межами музею'))
MARKS_ON_OBJECT = (('', ''), ('Написи', 'Написи'), ('Печатки', 'Печатки'), ('Клейма', 'Клейма'),)
COLLECTIONS = (('', ''), ('Байдуже', 'Байдуже'),)
TOPOGRAPHY = (('', ''), ('Шкаф', 'Шкаф'))
CONDITIONS = (('', ''), ('Без пошкоджень', 'Без пошкоджень'), ('Задовільний', 'Задовільний'),
              ('Незадовільний', 'Незадовільний'))


def get_image_path(self, filename):
    path = ''.join(["/", filename])
    return path


class Custom:

    class MultiMaterialSelectWidget(MultiWidget):
        def __init__(self, amount):
            widgets = [SelectMultiple(choices=MATERIAL_CHOICES)]
            super(Custom.MultiMaterialSelectWidget, self).__init__(widgets)

        def decompress(self, value):
            return [value]

        def format_output(self, rendered_widgets):
            return '<br/>'+rendered_widgets[0]+'<br/>'

    class MultiMaterialSelectField(MultiValueField):

        def __init__(self, amount=10, *args, **kwargs):
            self.attrs = kwargs.copy()
            list_fields = [forms.CharField()]
            super(Custom.MultiMaterialSelectField, self).__init__(list_fields,
                                                                  widget=Custom.MultiMaterialSelectWidget(amount=amount),
                                                                  *args, **kwargs)

        def compress(self, values):
            if values:
                return values[0]
            else:
                return None

    class TextChoiceWidget(MultiWidget):
        def __init__(self, choices, placeholder1='', size1=10):
            widgets = [TextInput(attrs={'size': size1, 'max_length': 30, 'placeholder': placeholder1}),
                       Select(choices=choices)]
            super(Custom.TextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(' ')
                return [x.strip("()") for x in res]
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
                return values[0] + ' (' + values[1] + ')'
            else:
                return ''

    class TextChoiceDateWidget(MultiWidget):
        def __init__(self, choices, placeholder1='', size1=40):
            widgets = [TextInput(attrs={'size': size1, 'max_length': 50, 'placeholder': placeholder1}),
                       Select(choices=choices),
                       DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}, attrs={'width': '300px'})]
            super(Custom.TextChoiceDateWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(' ')
                return [x.strip("()") for x in res]
            else:
                return [None, None, None]

        def format_output(self, rendered_widgets):
            dd = '<br>'
            res = u''.join(rendered_widgets)
            return dd+res

    class TextChoiceDateField(MultiValueField):
        def __init__(self, choices, placeholder1, size1=40, *args, **kwargs):
            list_fields = [fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices),
                           fields.DateTimeField(DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}, attrs={'width': '300px'}))]
            super(Custom.TextChoiceDateField, self).__init__(list_fields,
                                                             widget=Custom.TextChoiceDateWidget(choices=choices, size1=size1, placeholder1=placeholder1),
                                                             *args,
                                                             **kwargs)

        def compress(self, values):
            if values:
                return values[0] + ' (' + values[1] + ')'
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
                return values[0] + ': ' + values[1] + ': ' + values[2]
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

    class ChoiceTextTextChoiceField(MultiValueField):
        def __init__(self, choices1, choices2, placeholder1, placeholder2):
            list_fields = [fields.ChoiceField(choices=choices1),
                           fields.CharField(max_length=30),
                           fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices2)]
            super(Custom.ChoiceTextTextChoiceField, self).__init__(list_fields,
                                                                   widget=Custom.ChoiceTextTextChoiceWidget(choices1=choices1,
                                                                                                            choices2=choices2,
                                                                                                            placeholder1=placeholder1,
                                                                                                            placeholder2=placeholder2))

        def compress(self, values):
            if values:
                return values[0] + ': ' + values[1] + ': ' + values[2] + ': ' + values[3]
            else:
                return ''

    class ChoiceTextTextChoiceWidget(MultiWidget):
        def __init__(self, choices1, choices2, placeholder1='', placeholder2='', invisible=True, **kwargs):
            if invisible:
                attrs = {'max_length': 10, 'placeholder1': placeholder1, 'placeholder2': placeholder2, 'style': 'display:none;'}
            else:
                attrs = {'max_length': 10, 'placeholder1': placeholder1, 'placeholder2': placeholder2}
            widgets = [Select(choices=choices1, **kwargs),
                       TextInput(attrs),
                       TextInput(attrs),
                       Select(choices=choices2, **kwargs)]
            super(Custom.ChoiceTextTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(':')
                return res
            else:
                return [None, None, None, None]

        def format_output(self, rendered_widgets):
            return u''.join(rendered_widgets)

    class MultiChoiceTextTextChoiceWidget(MultiWidget):
        PREC_ST_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'two')
        MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')

        def __init__(self, number):
            widgets = [Custom.ChoiceTextTextChoiceWidget(placeholder1='', choices1=self.PREC_ST_CHOICES, choices2=self.MES_UNIT_WEIGHT, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceTextTextChoiceWidget(placeholder1='', choices1=self.PREC_ST_CHOICES, choices2=self.MES_UNIT_WEIGHT, attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceTextTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split('; ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceTextTextChoiceField(MultiValueField):
        PREC_ST_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'two')
        MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')

        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceTextTextChoiceField(choices1=self.PREC_ST_CHOICES, choices2=self.MES_UNIT_WEIGHT, placeholder1='Кількість', placeholder2='2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceTextTextChoiceField(choices1=self.PREC_ST_CHOICES, choices2=self.MES_UNIT_WEIGHT, placeholder1='', placeholder2=''))
            super(Custom.MultiChoiceTextTextChoiceField, self).__init__(list_fields,
                                                                        widget=Custom.MultiChoiceTextTextChoiceWidget(number),
                                                                        *args,
                                                                        **kwargs)

        def compress(self, values):
            values = [x for x in values if x]
            return '; '.join(values)

    class ChoiceChoiceTextChoiceField(MultiValueField):
        def __init__(self, choices1, choices2, choices3, placeholder1):
            list_fields = [fields.ChoiceField(choices=choices1),
                           fields.ChoiceField(choices=choices2),
                           fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices3)]
            super(Custom.ChoiceChoiceTextChoiceField, self).__init__(list_fields,
                                                                     widget=Custom.ChoiceChoiceTextChoiceWidget(choices1=choices1,
                                                                                                                choices2=choices2,
                                                                                                                placeholder1=placeholder1,
                                                                                                                choices3=choices3))

        def compress(self, values):
            if values:
                return values[0] + ': ' + values[1] + ': ' + values[2] + ': ' + values[3]
            else:
                return ''

    class ChoiceChoiceTextChoiceWidget(MultiWidget):
        def __init__(self, choices1, choices2, choices3, placeholder1='', invisible=True, **kwargs):
            if invisible:
                attrs = {'max_length': 10, 'placeholder': placeholder1, 'style': 'display:none;'}
            else:
                attrs = {'max_length': 10, 'placeholder': placeholder1}
            widgets = [Select(choices=choices1, **kwargs),
                       Select(choices=choices2, **kwargs),
                       TextInput(attrs),
                       Select(choices=choices3, **kwargs)]
            super(Custom.ChoiceChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(':')
                return res
            else:
                return [None, None, None, None]

        def format_output(self, rendered_widgets):
            return u''.join(rendered_widgets)

    class MultiChoiceChoiceTextChoiceWidget(MultiWidget):
        PREC_MAT_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'one')
        MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
        ASSAY_CHOICES = get_choice(ROOT, 0, 'assay')

        def __init__(self, number):
            widgets = [Custom.ChoiceChoiceTextChoiceWidget(placeholder1='0,2', choices1=self.PREC_MAT_CHOICES, choices2=self.ASSAY_CHOICES, choices3=self.MES_UNIT_WEIGHT, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceChoiceTextChoiceWidget(placeholder1='', choices1=self.PREC_MAT_CHOICES, choices2=self.ASSAY_CHOICES, choices3=self.MES_UNIT_WEIGHT, attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split('; ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceChoiceTextChoiceField(MultiValueField):
        PREC_MAT_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'one')
        MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
        ASSAY_CHOICES = get_choice(ROOT, 0, 'assay')

        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceChoiceTextChoiceField(choices1=self.PREC_MAT_CHOICES, choices2=self.ASSAY_CHOICES, choices3=self.MES_UNIT_WEIGHT, placeholder1='0.2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceChoiceTextChoiceField(choices1=self.PREC_MAT_CHOICES, choices2=self.ASSAY_CHOICES, choices3=self.MES_UNIT_WEIGHT, placeholder1=''))
            super(Custom.MultiChoiceChoiceTextChoiceField, self).__init__(list_fields,
                                                                          widget=Custom.MultiChoiceChoiceTextChoiceWidget(number),
                                                                          *args,
                                                                          **kwargs)

        def compress(self, values):
            values = [x for x in values if x]
            return '; '.join(values)

    class MultiChoiceTextChoiceWidget(MultiWidget):
        TYPE_CHOICES = get_choice(ROOT, 0, 'dimension', 'type')
        MEAS_CHOICES = get_choice(ROOT, 0,'dimension', 'measurement_unit')

        def __init__(self, number):
            widgets = [Custom.ChoiceTextChoiceWidget(placeholder1='0,2', choices1=self.TYPE_CHOICES, choices2 = self.MEAS_CHOICES, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceTextChoiceWidget(placeholder1='', choices1=self.TYPE_CHOICES, choices2 = self.MEAS_CHOICES, attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split('; ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceTextChoiceField(MultiValueField):
        TYPE_CHOICES = get_choice(ROOT, 0, 'dimension', 'type')
        MEAS_CHOICES = get_choice(ROOT, 0,'dimension', 'measurement_unit')

        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceTextChoiceField(choices1=self.TYPE_CHOICES, choices2 = self.MEAS_CHOICES, placeholder1='0.2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceTextChoiceField(choices1=self.TYPE_CHOICES, choices2=self.MEAS_CHOICES, placeholder1=''))
            super(Custom.MultiChoiceTextChoiceField, self).__init__(list_fields,
                                                                    widget=Custom.MultiChoiceTextChoiceWidget(number),
                                                                    *args,
                                                                    **kwargs)

        def compress(self, values):
            values = [x for x in values if x]
            return '; '.join(values)


class Object(models.Model):
    class Meta:
        permissions = (('see_all_obj', 'бачити всi'),
                       ('see_personal_obj', 'бачити своi'),
                       ('action_obj', 'облiковi процедури'),
                       ('add_new_obj', 'додавання'),
                       ('change_obj', 'редагування'),
                       ('remove_obj', 'видалення'),
        )
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
    date_creation = models.CharField(max_length=50, default='', null=True)
    place_of_creation = models.CharField(max_length=50, default='', null=True)
    date_detection = models.CharField(max_length=50, default='', null=True)
    place_detection = models.CharField(max_length=50, default='', null=True)
    date_existence = models.CharField(max_length=50, default='', null=True)
    place_existence = models.CharField(max_length=50, default='', null=True)
    mark_on_object = models.CharField(max_length=200, default='', null=True)  ##
    note = models.CharField(max_length=200, default='', null=True)  #
    condition = models.CharField(max_length=100, default='', null=True)  #
    condition_descr = models.CharField(max_length=2000, null=True)
    transport_possibility = models.BooleanField(default=False)  ##
    recomm_for_restauration = models.CharField(max_length=100, default='', null=True)  ##
    restauration_notes = models.CharField(max_length=200, default='', null=True)  ##
    memorial_subject = models.CharField(max_length=200, default='', null=True)
    storage = models.CharField(max_length=200, default='', null=True)  #
    place_appellation = models.CharField(max_length=200, default='', null=True)  ##
    is_there = models.CharField(max_length=200, default='', null=True)  ##
    bibliography = models.CharField(max_length=1000, default='', null=True)
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200, default='', null=True)  #
    link_on_doc = models.CharField(max_length=200, default='', null=True)
    #doc_type = models.CharField(max_length=50)
    side_1 = models.CharField(max_length=200, default='', null=True)  #
    side_2 = models.CharField(max_length=200, default='', null=True)  #
    term_back = models.DateField(default='2000-01-01', null=True)  #
    aim_of_receiving_gen = models.CharField(max_length=200, default='', null=True)  #
    #aim_of_receiving = models.CharField(max_length=1000, default='', null=True)
    circumst_write_off = models.CharField(max_length=200, default='', null=True)  ##
    #reason = models.FileField(default='default.txt', null=True, upload_to=get_image_path)  #
    #source = models.CharField(max_length=200, default='', null=True)  #

    def __unicode__(self):
        return self.name.split(' ')[0]

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
    class Meta:
        permissions = (('only_personal_activity', 'бачити тiльки своi'),
                       ('all_activity', 'бачити все'))
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

    def set(self):
        return self.attributeassignment_set.all()


class AttributeAssignment(models.Model):
    attr_name = models.CharField(max_length=40)
    attr_value = models.CharField(max_length=200, default='None', null=True)
    attr_label = models.CharField(max_length=200, default='default', null=True)
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
        for query in self.aim.attributeassignment_set.filter(attr_name=self.attr_name, aim=self.aim):
            query.actual = False
            query.save()
        self.save()


class TempSaveForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=1000, label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
    material = Custom.MultiMaterialSelectField(label='Матеріал', required=False)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт приймання на ТЗ)', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 (акт приймання на ТЗ)', required=True)
    #aim_of_receiving = forms.ChoiceField(choices=AIMS, label='Мета приймання на ТЗ', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=False)
    reason = forms.FileField(label='Підстава', required=False)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    TS_code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=False) #
    #return_mark = forms.BooleanField(label='Is it returned?')

    def clean_material(self):
        if not self.cleaned_data['material']:
            raise ValidationError('Обязательное поле')


class InitialTempSaveForm(forms.Form):
    obj = forms.ModelChoiceField(queryset=Object.objects.all())


class TempRetForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('returned', 'Повернутий з тимчасового збереження'),
        ('add on PS', 'Поставити об’єкт на постійне збереження ')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=None, label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(label='Автор', required=True) #
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField(label = 'Матеріал', required=False)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea)
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 450px;"}))
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': 'margin: 0px; height: 252px; width: 450px;'}))
    reason = forms.FileField(label='Підстава', required=False)
    side_1 = forms.CharField(max_length=100, label='Сторона 1 (акт повернення з ТЗ)', required=True)
    side_2 = forms.CharField(max_length=100, label='Сторона 2 (акт повернення з ТЗ)', required=True)
    return_mark = forms.ChoiceField(choices=choices, required=True, label='Позначка про повернення предмета або переведення до музейного зібрання (ПЗ) у книзі ТЗ')
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True) #


class PrepareRetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareRetForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Приймання на тимчасове зберігання'\
                    and project.status() != 'Списання (втрата тощо)'\
                    and project.status() != 'Пустий об’єкт':
                objlist.append(project)
        objects = [(o.id, o.__unicode__()) for o in objlist]
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class PreparePSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreparePSForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() != 'Пустий об’єкт' and project.status() != 'Приймання на постійне зберігання'\
                    and project.status() != 'Списання (втрата тощо)'\
                    and project.status() != 'Передача на постійне зберігання'\
                    and project.status() != 'Повернення творів з Тимчасового зберігання на Постійне зберігання'\
                    and project.status() != 'Видача предметів з Постійного зберігання на Тимчасове зберігання':
                objlist.append(project)
        objects = [(0, 'Новий об’єкт')]
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class PersistentSaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True) #
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField(label='Матеріали', required=False)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=False)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=False) #
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт ПЗ)', required=True)
    side_2 = forms.CharField(max_length=209, label='Сторона 2 (акт ПЗ)', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа',
                                                  required=True)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)
    inventory_number = forms.CharField(max_length=200, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=200, label='Спеціальний інвентарний номер', required=True)


class PrepareInventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareInventoryForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Приймання на постійне зберігання'\
                    or project.status() == 'Пустий об’єкт'\
                    and project.status() != 'Списання (втрата тощо)':
                objlist.append(project)
        objects = [(0, 'Новий об’єкт')]
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class InventorySaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    date_detection = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Дата знаходження', required=True)
    place_detection = forms.CharField(max_length=200, label='Місце виявлення')
    date_existence = forms.CharField(max_length=200, label='Дата побутування')
    place_existence = forms.CharField(max_length=200, label='Місце побутування')
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField(label='Матеріали', required=False)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    mark_on_object = Custom.TextChoiceField(choices=MARKS_ON_OBJECT, label='Позначки на предметі', placeholder1='')
    classification = forms.CharField(max_length=200, label='Класифікація')
    typology = forms.CharField(max_length=200, label='Типологія')
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    bibliography = forms.CharField(max_length=200, label='Бібліографія')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    inventory_number = forms.CharField(max_length=100, label='Інвентарний номер')
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=False)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=False)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер')
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)


class PrepareSpecInventoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareSpecInventoryForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Інвентарний облік' or project.status() == 'Приймання на постійне зберігання'\
                    or project.status() == 'Пустий об’єкт'\
                    and project.status() != 'Списання (втрата тощо)':
                objlist.append(project)
        objects = [(0, 'Новий об’єкт')]
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class SpecInventorySaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    date_creation = forms.CharField(label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    fully_precious = forms.BooleanField(label='Предмет повністю складається з дорогоцінних'
                                              ' металів/дорогоцінного каміння?', required=False)
    metals = Custom.MultiChoiceChoiceTextChoiceField(label='Дорогоцінні метали')
    stones = Custom.MultiChoiceTextTextChoiceField(label='Дорогоцінне каміння')
    #name_prec_metal = Custom.MaterialSelectField(choices=get_choice(et.parse('museum/materials.xml').getroot(),'materials', 'precious'),
    #                                             label='Назва дорогоцінного металу', amount=1)
    #assay = Custom.MaterialSelectField(choices=get_choice(et.parse('museum/materials.xml').getroot(),'assay'),
    #                                   label='Проба дорогоцінного металу', amount=1)
    #weight_prec_metal = Custom.TextChoiceField(choices=WEIGHT_CHOICES,
    #                                label='Маса дорогоцінного металу в чистоті', placeholder1='')
    #name_prec_stone = Custom.MaterialSelectField(choices=get_choice(et.parse('museum/materials.xml').getroot(),'materials', 'precious'),
    #                                             label='Назва дорогоцінного каміння', amount=1)
    #amount_prec_stone0 = forms.CharField(label='Кількість дорогоцінного каміння')
    #weight_prec_stone = Custom.TextChoiceField(choices=WEIGHT_CHOICES,
    #                                           label='Маса дорогоцінного металу в чистоті', placeholder1='')
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер')
    PS_code = forms.CharField(max_length=200, label='Шифр і номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою')
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=False)
    mat_person_in_charge = forms.ModelChoiceField(queryset=User.objects.all(), label='Матеріально-відповідальна особа', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)


class PreparePassportForm(forms.Form):
    error_css_class = 'error'
    def __init__(self, *args, **kwargs):
        super(PreparePassportForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() != 'Пустий об’єкт'\
                    or project.status() != 'Списання (втрата тощо)':
                objlist.append(project)
        objects = [(0, 'Новий об’єкт')]
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class PassportForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    department = forms.ChoiceField(choices=get_choice(ROOT, 0, 'department'), label='Відомство', required=True)
    adm_submission = forms.ChoiceField(choices=get_choice(ROOT, 0, 'department'), label='Адміністративне підпорядкування', required=True)
    museum = forms.ChoiceField(choices=get_choice(ROOT, 0, 'museum'), label='Музей', required=True)
    address = forms.CharField(label='Адреса', required=True, max_length=50 )
    section = forms.ChoiceField(choices=get_choice(ROOT, 0, 'section'), label='Відділ', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=False)
    PS_code = forms.CharField(label='Книга надходжень (номер)', max_length=50, required=True)
    inventory_number = forms.CharField(max_length=100, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    old_inventory_numbers = forms.CharField(max_length=500, label='Старі інвентарні номери', required=True)
    collection_descr = forms.CharField(max_length=50, label='Колекційний опис (номер)', required=True)
    identifier = forms.CharField(label='Унікальний номер в інформаційній системі', max_length=50, required=True)
    negative = forms.CharField(label='Негатив (номер)', max_length=50, required=True)
    image = forms.ImageField(label='Фото', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    author = forms.CharField(max_length=200, label='Автор або виробник', required=True)
    date_place_creation = forms.CharField(max_length=200, label='Час і місце створення (виготовлення)', required=True)
    date_place_detection = forms.CharField(max_length=200, label='Час і місце виявлення', required=True)
    date_place_existence = forms.CharField(max_length=200, label='Час і місце побутування', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження (закупка, замовлення, дарунок, передача)', required=False)
    link_on_doc = forms.CharField(max_length=50, label='Документи', required=False)
    classification = forms.CharField(max_length=200, label='Класифікація')
    typology = forms.CharField(max_length=200, label='Типологія')
    amount = forms.IntegerField(label='Кількість', required=True)
    size = Custom.MultiChoiceTextChoiceField(label='Розміри (см/мм)')
    material = Custom.MultiMaterialSelectField(label='Матеріали', required=False)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    metals = Custom.MultiChoiceChoiceTextChoiceField(label='Дорогоцінні метали')
    stones = Custom.MultiChoiceTextTextChoiceField(label='Дорогоцінне каміння')
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    person_or_actions = forms.CharField(max_length=2000, label='Особи чи події, пов’язані з предметом', required=True,
                                        widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    memorial_subject = forms.CharField(max_length=200, label='Зв’язок з іншими пам’ятками (історичний, мистецтвознавчий, культурологічний аспект)', required=True)
    extra_list = forms.CharField(max_length=2000, label='Додаткові відомості', required=True,
                                 widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    restoration = forms.CharField(max_length=2000, label='Реставрація (історія реставрації, зв’язок із журналом реставрації)', required=True,
                                  widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    image_amount = forms.IntegerField(label='Кількість фотографій', min_value=0)
    price = forms.CharField(max_length=40, label='Оціночна вартість', required=True)
    attachment_amount = forms.IntegerField(label='Кількість додатків', min_value=0)
    exposition = forms.CharField(max_length=100, label='Експонування', required=False)
    existence_check = forms.CharField(max_length=100, label='Звіряння наявності (документ, дата)', required=False)
    bibliography = forms.CharField(max_length=200, label='Бібліографія')
    archive_materials = forms.CharField(max_length=200, label='Архівні матеріали')
    person_in_charge = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=SelectMultiple(), label='Відповідальні особи')


class PreparePStoTSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreparePStoTSForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Приймання на постійне зберігання'\
                    and project.status() != 'Списання (втрата тощо)'\
                    and project.status() != 'Передача на постійне зберігання'\
                    and project.status() != 'Видача предметів з Постійного зберігання на Тимчасове зберігання':
                objlist.append(project)
        objects = []
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class FromPStoTSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField()
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    insurable_value = forms.CharField(max_length=30, label='Страхова вартість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    side_1 = forms.CharField(max_length=200, label='Сторона 1 юридична особа', required=True)
    side_1_person_in_charge = forms.CharField(max_length=200, label='Сторона 1 головний зберігач (матеріально-відповідальна особа)', required=True)
    side_1_fond_saver = forms.CharField(max_length=200, label='Сторона 1 зберігач фонду', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 юридична особа', required=True)
    side_2_person_in_charge = forms.CharField(max_length=200, label='Сторона 2 відповідальна особа/приватна особа', required=True)
    #aim_of_receiving = forms.CharField(max_length=2000, label='Мета передачі на ТЗ', required=True,
    #                                   widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    reason = forms.CharField(label='Підстава (посилання на документи: договір, наказ директора, наказ вищої інстанції тощо)', max_length=400, required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    TS_code = forms.CharField(max_length=100, label='Шифр та номер ТЗ (актуальний)', required=True)
    is_there = forms.ChoiceField(choices=PLACE[2:4], label='Фізичне місце збереження (топографія) – позначка про відсутність (за межами фондосховища, за межами музею)', required=True)


class PrepareTStoPSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareTStoPSForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() == 'Видача предметів з Постійного зберігання на Тимчасове зберігання'\
                    and project.status() != 'Списання (втрата тощо)':
                objlist.append(project)
        objects = []
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class FromTStoPSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField()
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    insurable_value = forms.CharField(max_length=30, label='Страхова вартість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    side_1 = forms.CharField(max_length=200, label='Сторона 1 юридична особа', required=True)
    side_1_person_in_charge = forms.CharField(max_length=200, label='Сторона 1 головний зберігач (матеріально-відповідальна особа)', required=True)
    side_1_fond_saver = forms.CharField(max_length=200, label='Сторона 1 зберігач фонду', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 юридична особа', required=True)
    side_2_person_in_charge = forms.CharField(max_length=200, label='Сторона 2 відповідальна особа/приватна особа', required=True)
    #aim_of_receiving = forms.CharField(max_length=2000, label='Мета передачі на ТЗ', required=True,
    #                                   widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    reason = forms.CharField(label='Посилання на документи: акт видачі на ТЗ, договір, наказ директора, наказ вищої інстанції тощо', max_length=400, required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    is_there = forms.ChoiceField(choices=PLACE[1:2], label='Фізичне місце збереження (топографія) – позначка про повернення у фонди', required=True)


class PrepareSendOnPSForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareSendOnPSForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() != 'Приймання на постійне зберігання' \
                    and project.status() != 'Повернення творів з Тимчасового зберігання на Постійне зберігання'\
                    and project.status() != 'Пустий об’єкт'\
                    and project.status() != 'Передача на постійне зберігання'\
                    and project.status() != 'Списання (втрата тощо)':
                objlist.append(project)
        objects = []
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class SendOnPSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = Custom.MultiMaterialSelectField()
    size = Custom.MultiChoiceTextChoiceField(label='Розміри')
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    description = forms.CharField(max_length=2000, label='Опис предмета', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    side_1 = forms.CharField(max_length=200, label='Сторона 1 юридична особа', required=True)
    side_1_person_in_charge = forms.CharField(max_length=200, label='Сторона 1 головний зберігач', required=True)
    side_1_fond_saver = forms.CharField(max_length=200, label='Сторона 1 зберігач фонду', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 юридична особа', required=True)
    side_2_person_in_charge = forms.CharField(max_length=200, label='Сторона 2 відповідальна особа/приватна особа', required=True)
    reason = forms.CharField(label='Підстава (посилання на документи: договір, наказ Міністерства культури тощо, наказ директора музею)', max_length=400, required=True)
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    TS_code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    is_there = forms.ChoiceField(choices=PLACE[2:4], label='Фізичне місце збереження (топографія) – позначка про відсутність (за межами фондосховища, за межами музею)', required=True)


class PrepareWritingOffForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrepareWritingOffForm, self).__init__(*args, **kwargs)
        objlist = []
        for project in Object.objects.all():
            if project.status() != 'Пустий об’єкт' and project.status() != 'Списання (втрата тощо)' :
                objlist.append(project)
        objects = []
        for o in objlist:
            objects.append((o.id, o.__unicode__()))
        self.fields['obj'] = forms.ChoiceField(choices=objects, label='Виберiть об’єкт')


class WritingOffForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='')
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True)
    note = forms.CharField(max_length=1000, label='Примітка', required=True, widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    main_saver = forms.ModelChoiceField(queryset=User.objects.all(), label='Головний зберігач', required=True)
    fond_saver = forms.ModelChoiceField(queryset=User.objects.all(), label='Зберігач фонду', required=True)
    reason = forms.CharField(label='Причина', max_length=400, required=True)
    circumstance = forms.CharField(label='Обставини ', max_length=400, required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи: акти звірення, погодження Міністерства культури тощо', required=False)
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    TS_code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    is_there = forms.ChoiceField(choices=PLACE[2:4], label='Фізичне місце збереження (топографія) – позначка про відсутність (за межами фондосховища, за межами музею)', required=True)


class ObjectEditForm(ModelForm):
    class Meta:
        model = Object
    #material = Custom.MultiMaterialField()
    #size = Custom.MultiMaterialField(number=3)


class ObjectCreateForm(ModelForm):
    class Meta:
        model = Object
    #material = Custom.MultiMaterialField()
    #size = Custom.MultiMaterialField(number=3)


class AutForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логiн:')
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Пароль:')

