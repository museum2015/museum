# -*- coding: utf-8 -*-
import datetime
import os
from django import forms
from django.db import models
from django.db.models import Q
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select, ModelForm, SelectMultiple
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.html import mark_safe, escape, format_html
from django.core.exceptions import ValidationError
from django.views.generic.edit import DeleteView
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

PREC_ST_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'two')
MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
WEIGHT_CHOICES = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
MATERIAL_CHOICES = get_choice(ROOT, 0, 'materials')
LANGUAGE_CHOICES = get_choice(ROOT, 0, 'languages')
ASSAY_CHOICES = get_choice(ROOT, 0, 'assay')
PREC_MAT_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'one')
TYPE_CHOICES = get_choice(ROOT, 0, 'dimension', 'type')
MEAS_CHOICES = get_choice(ROOT, 0,'dimension', 'measurement_unit')

def recalc():
    global ROOT, PREC_ST_CHOICES, MES_UNIT_WEIGHT, WEIGHT_CHOICES, MATERIAL_CHOICES, LANGUAGE_CHOICES, ASSAY_CHOICES, PREC_MAT_CHOICES, TYPE_CHOICES, MEAS_CHOICES
    ROOT = et.parse('museum/materials.xml').getroot()
    PREC_ST_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'two')
    MES_UNIT_WEIGHT = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
    WEIGHT_CHOICES = get_choice(ROOT, 0, 'dimension', 'measurement_unit', 'weight')
    MATERIAL_CHOICES = get_choice(ROOT, 0, 'materials')
    LANGUAGE_CHOICES = get_choice(ROOT, 0, 'languages')
    ASSAY_CHOICES = get_choice(ROOT, 0, 'assay')
    PREC_MAT_CHOICES = get_choice(ROOT, 0, 'materials', 'precious', 'one')
    TYPE_CHOICES = get_choice(ROOT, 0, 'dimension', 'type')
    MEAS_CHOICES = get_choice(ROOT, 0,'dimension', 'measurement_unit')


TECHNIQUE_CHOICES = (('', ''), ('Техніка 1', 'Техніка 1'),)
WAY_OF_FOUND_CHOICES = (('', ''), ('Розкопки', 'Розкопки'),)
AIMS = get_choice(ROOT, 0, 'purpose')
PLACE = (('', ''), ('На місці', 'На місці'), ('За межами фондосховища', 'За межами фондосховища'),
         ('За межами музею', 'За межами музею'))
MARKS_ON_OBJECT = (('', ''), ('Написи', 'Написи'), ('Печатки', 'Печатки'), ('Клейма', 'Клейма'),)
COLLECTIONS = (('', ''), ('Байдуже', 'Байдуже'),)
TOPOGRAPHY = (('', ''), ('Шкаф', 'Шкаф'))
CONDITIONS = (('', ''), ('Без пошкоджень', 'Без пошкоджень'), ('Задовільний', 'Задовільний'),
              ('Незадовільний', 'Незадовільний'))


def get_image_path(filename):
    path = ''.join(["/", filename])
    return path


class Custom:
    class myUser(User):
        class Meta:
            proxy = True
        def __unicode__(self):
            if self.get_full_name():
                try:
                    return self.get_full_name()+' ('+self.groups.values_list('name', flat=True)[0]+')'
                except IndexError:
                    return self.get_full_name()
            else:
                try:
                    return self.get_username()+' ('+self.groups.values_list('name', flat=True)[0]+')'
                except IndexError:
                    return self.get_username()

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
            return values

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

    class TextAreaChoiceWidget(MultiWidget):
        def __init__(self, choices, placeholder1='', size1=10):
            widgets = [forms.Textarea(attrs={'size': size1, 'max_length': 30, 'placeholder': placeholder1, 'style': "margin: 0px; height: 252px; width: 550px;"}),
                       Select(choices=choices)]
            super(Custom.TextAreaChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(' ')
                return [x.strip("()") for x in res]
            else:
                return [None, None]

        def format_output(self, rendered_widgets):
            dd = '<br>'
            res = u'<br>'.join(rendered_widgets)
            return dd+res

    class TextAreaChoiceField(MultiValueField):
            def __init__(self, choices, placeholder1, size1=10, *args, **kwargs):
                list_fields = [fields.CharField(max_length=3000),
                               fields.ChoiceField(choices=choices)]
                super(Custom.TextAreaChoiceField, self).__init__(list_fields,
                                                                 widget=Custom.TextAreaChoiceWidget(choices=choices, size1=size1, placeholder1=placeholder1),
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
                return values[0] + ' : ' + values[1] + ' ' + values[2]
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
                a = value.split(' : ')[0]
                b = value.split(' : ')[1]
                c = b.split(' ')[1]
                b = b.split(' ')[0]
                return [a, b, c]
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
                return values[0] + ':' + values[1] + ':' + values[2] + ':' + values[3]
            else:
                return ''

    class ChoiceTextTextChoiceWidget(MultiWidget):
        def __init__(self, choices1, choices2, placeholder1='', placeholder2='', invisible=True, **kwargs):
            self.choices1 = choices1
            self.choices2 = choices2
            if invisible:
                self.a = {'max_length': 10, 'placeholder': placeholder1, 'style': 'display:none;'}
                self.b = {'max_length': 10,'placeholder': placeholder2, 'style': 'display:none;'}
            else:
                self.a = {'max_length': 10, 'placeholder': placeholder1}
                self.b = {'max_length': 10, 'placeholder': placeholder2}
            widgets = [Select(choices=choices1, **kwargs),
                       TextInput(attrs=self.a),
                       TextInput(attrs=self.b),
                       Select(choices=choices2, **kwargs)]
            super(Custom.ChoiceTextTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(':')

            else:
                return [None, None, None, None]

        def format_output(self, rendered_widgets):
            return u''.join(rendered_widgets)

    class MultiChoiceTextTextChoiceWidget(MultiWidget):
        def __init__(self, number):
            widgets = [Custom.ChoiceTextTextChoiceWidget(placeholder1='Кількість', placeholder2='Загальна маса', choices1=PREC_ST_CHOICES, choices2=MES_UNIT_WEIGHT, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceTextTextChoiceWidget(placeholder1='', choices1=PREC_ST_CHOICES, choices2=MES_UNIT_WEIGHT, attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceTextTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(', ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceTextTextChoiceField(MultiValueField):
        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceTextTextChoiceField(choices1=PREC_ST_CHOICES, choices2=MES_UNIT_WEIGHT, placeholder1='Кількість', placeholder2='2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceTextTextChoiceField(choices1=PREC_ST_CHOICES, choices2=MES_UNIT_WEIGHT, placeholder1='', placeholder2=''))
            super(Custom.MultiChoiceTextTextChoiceField, self).__init__(list_fields,
                                                                        widget=Custom.MultiChoiceTextTextChoiceWidget(number),
                                                                        *args,
                                                                        **kwargs)

        def compress(self, values):
            values = [x for x in values if x]
            return ', '.join(values)

    class ChoiceChoiceTextChoiceField(MultiValueField):
        def __init__(self, choices1, choices3):
            list_fields = [fields.ChoiceField(choices=choices1),
                           fields.CharField(max_length=10),
                           fields.CharField(max_length=30),
                           fields.ChoiceField(choices=choices3)]
            super(Custom.ChoiceChoiceTextChoiceField, self).__init__(list_fields,
                                                                     widget=Custom.ChoiceChoiceTextChoiceWidget(choices1=choices1,
                                                                                                                choices3=choices3))

        def compress(self, values):
            if values:
                return values[0] + ':' + values[1] + ':' + values[2] + ':' + values[3]
            else:
                return ''

    class ChoiceChoiceTextChoiceWidget(MultiWidget):
        def __init__(self, choices1, choices3, invisible=True, **kwargs):
            if invisible:
                self.a = {'max_length': 10, 'placeholder': 'Проба', 'style': 'display:none;'}
                self.b = {'max_length': 10, 'placeholder': 'Загальна маса', 'style': 'display:none;'}
            else:
                self.a = {'max_length': 10, 'placeholder': 'Проба'}
                self.b = {'max_length': 10, 'placeholder': 'Загальна маса'}
            widgets = [Select(choices=choices1, attrs=self.a),
                       TextInput(attrs=self.a),
                       TextInput(attrs=self.b),
                       Select(choices=choices3, attrs=self.b)]
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
        def __init__(self, number):
            widgets = [Custom.ChoiceChoiceTextChoiceWidget(choices1=PREC_MAT_CHOICES,choices3=MES_UNIT_WEIGHT, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceChoiceTextChoiceWidget(choices1=PREC_MAT_CHOICES, choices3=MES_UNIT_WEIGHT, invisible=True))
            super(Custom.MultiChoiceChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(', ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceChoiceTextChoiceField(MultiValueField):
        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceChoiceTextChoiceField(choices1=PREC_MAT_CHOICES, choices3=MES_UNIT_WEIGHT)]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceChoiceTextChoiceField(choices1=PREC_MAT_CHOICES, choices3=MES_UNIT_WEIGHT))
            super(Custom.MultiChoiceChoiceTextChoiceField, self).__init__(list_fields,
                                                                          widget=Custom.MultiChoiceChoiceTextChoiceWidget(number),
                                                                          *args,
                                                                          **kwargs)

        def compress(self, values):
            values = [x for x in values if x]
            return ', '.join(values)

    class MultiChoiceTextChoiceWidget(MultiWidget):
        def __init__(self, number):
            widgets = [Custom.ChoiceTextChoiceWidget(placeholder1='0,2', choices1=TYPE_CHOICES, choices2 = MEAS_CHOICES, invisible=False)]
            for i in range(number-1):
                widgets.append(Custom.ChoiceTextChoiceWidget(placeholder1='', choices1=TYPE_CHOICES, choices2 = MEAS_CHOICES, attrs={'style': 'display:none;'}))
            super(Custom.MultiChoiceTextChoiceWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split('; ')
            else:
                return []

        def format_output(self, rendered_widgets):
            return '<br/>' + ''.join(rendered_widgets)

    class MultiChoiceTextChoiceField(MultiValueField):
        def __init__(self, number=10, *args, **kwargs):
            list_fields = [Custom.ChoiceTextChoiceField(choices1=TYPE_CHOICES, choices2 = MEAS_CHOICES, placeholder1='0.2')]
            for i in range(number-1):
                list_fields.append(Custom.ChoiceTextChoiceField(choices1=TYPE_CHOICES, choices2=MEAS_CHOICES, placeholder1=''))
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
    is_fragment = models.BooleanField(default=False, blank=True)
    name = models.CharField(max_length=200, default='', null=True, blank=True)  #
    amount = models.IntegerField(default=0, null=True, blank=True)  #
    size = models.CharField(max_length=40, default='', null=True, blank=True)  #
    classify = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    type = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    material = models.CharField(max_length=200, default='', null=True, blank=True)  #
    technique = models.CharField(max_length=200, default='', null=True, blank=True)  #
    description = models.TextField(max_length=1000, default='', null=True, blank=True)  #
    identifier = models.CharField(max_length=50, default='', null=True, blank=True)
    image = models.ImageField(default='default.jpg', null=True, upload_to='images/')
    #image_type = models.CharField(max_length=50, default='', null=True, blank=True)
    author = models.CharField(max_length=100, default='', null=True, blank=True)  #
    price = models.CharField(max_length=50, default='', null=True, blank=True)  #
    date_creation = models.CharField(max_length=50, default='', null=True, blank=True)
    place_of_creation = models.CharField(max_length=50, default='', null=True, blank=True)
    date_detection = models.CharField(max_length=50, default='', null=True, blank=True)
    place_detection = models.CharField(max_length=50, default='', null=True, blank=True)
    date_existence = models.CharField(max_length=50, default='', null=True, blank=True)
    place_existence = models.CharField(max_length=50, default='', null=True, blank=True)
    mark_on_object = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    note = models.CharField(max_length=200, default='', null=True, blank=True)  #
    condition = models.CharField(max_length=100, default='', null=True, blank=True)  #
    condition_descr = models.CharField(max_length=2000, null=True, blank=True)
    transport_possibility = models.BooleanField(default=False, blank=True)  ##
    recomm_for_restauration = models.CharField(max_length=100, default='', null=True, blank=True)  ##
    restauration_notes = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    memorial_subject = models.CharField(max_length=200, default='', null=True, blank=True)
    storage = models.CharField(max_length=200, default='', null=True, blank=True)  #
    place_appellation = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    is_there = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    bibliography = models.CharField(max_length=1000, default='', null=True, blank=True)
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200, default='', null=True, blank=True)  #
    link_on_doc = models.CharField(max_length=200, default='', null=True, blank=True)
    #doc_type = models.CharField(max_length=50)
    side_1 = models.CharField(max_length=200, default='', null=True, blank=True)  #
    side_2 = models.CharField(max_length=200, default='', null=True, blank=True)  #
    term_back = models.DateField(default='2000-01-01', null=True, blank=True)  #
    aim_of_receiving_gen = models.CharField(max_length=200, default='', null=True, blank=True)  #
    #aim_of_receiving = models.CharField(max_length=1000, default='', null=True, blank=True)
    circumst_write_off = models.CharField(max_length=200, default='', null=True, blank=True)  ##
    reason = models.FileField(default='default.txt', null=True, upload_to='docs/')  #
    #source = models.CharField(max_length=200, default='', null=True, blank=True)  #
    stat = models.CharField(max_length=200, default='Пустий об’єкт', null=False, blank=True)


    def __unicode__(self):
        try:
            return self.name.split(' ')[0]
        except:
            return self.name

    def activity_set(self):
        return Activity.objects.filter(aim=self)

    @property
    def empty(self):
        return 'Пустий'.decode('utf-8') in self.stat

    @property
    def passport(self):
        if self.activity_set.filter(approval=True, type='Науково-уніфікований паспорт'): return True
        else: return False

    @property
    def io(self):
        if self.activity_set.filter(approval=True, type='Інвентарний облік'): return True
        else: return False

    @property
    def scio(self):
        if self.activity_set.filter(approval=True, type='Спеціальний інвентарний облік'): return True
        else: return False

    @property
    def ts(self):
        if 'тимчасовому зберіганні'.decode('utf-8') in self.stat: return True
        return False

    @property
    def ps(self):
        return 'постійне зберігання'.decode('utf-8') in self.stat

    @property
    def wo(self):
        return 'Cписаний'.decode('utf-8') in self.stat

    @property
    def ret(self):
        return 'Повернений'.decode('utf-8') in self.stat


class Activity(models.Model):
    class Meta:
        permissions = (('only_personal_activity', 'бачити тiльки своi'),
                       ('all_activity', 'бачити все'))
    time_stamp = models.DateTimeField(default='2000-02-12 00:00')
    type = models.CharField(max_length=150)
    actor = models.ForeignKey(Custom.myUser)
    approval = models.NullBooleanField(default=None, null=True)
    aim = models.ForeignKey(Object, null=True)

    def __unicode__(self):
        try:
            return self.type
        except IndexError:
            return 'UndefinedActivity'

    def approve(self):
        for attrib in self.attributeassignment_set.all():
            attrib.approve()
        self.approval = True
        if self.type == 'Приймання на тимчасове зберігання'.decode('utf-8') or \
           self.type == 'Видача предметів з Постійного зберігання на Тимчасове зберігання'.decode('utf-8'):
            self.aim.stat = format_html('На тимчасовому зберіганні (<a href="/activity/{0}">подія</a>)', self.pk)
        if self.type == 'Приймання на постійне зберігання'.decode('utf-8') or \
           self.type == 'Повернення творів з Тимчасового зберігання на Постійне зберігання'.decode('utf-8') or \
           self.type == 'Передача на постійне зберігання'.decode('utf-8'):
            self.aim.stat = format_html('На постійному зберіганні (<a href="/activity/{0}">подія</a>)', self.pk)
        if self.type == 'Списання'.decode('utf-8'):
            self.aim.stat = format_html('Cписаний (<a href="/activity/{0}">подія</a>)', self.pk)
        if self.type == 'Повернення з тимчасового зберiгання'.decode('utf-8'):
            self.aim.stat = format_html('Повернений з тимчасового зберiгання (<a href="/activity/{0}">подія</a>)', self.pk)
        if self.type == 'Науково-уніфікований паспорт'.decode('utf-8') or self.type == 'Інвентарний облік'.decode('utf-8'):
            if self.aim.empty:
                self.aim.stat = 'Щойно заповнений'
        self.save()
        self.aim.save()

    def reject(self):
        self.approval = False
        self.save()

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
        self.event_initiator.aim = self.aim
        for query in self.aim.attributeassignment_set.filter(attr_name=self.attr_name, aim=self.aim):
            query.actual = False
            query.save()
        self.save()


class TempSaveForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=1000, label='Кількість', required=True, min_value=0)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
    material = forms.CharField(label = 'Матеріали', required=False, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт приймання на ТЗ)', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 (акт приймання на ТЗ)', required=True)
    aim_of_receiving_gen = forms.ChoiceField(choices=AIMS, label='Мета приймання на ТЗ', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
    reason = forms.FileField(label='Підстава', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    TS_code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Матеріально-відповідальна особа', required=True)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True) #
    #return_mark = forms.BooleanField(label='Is it returned?')

    def clean_material(self):
        if self.cleaned_data['material'] == '[u\'\']':
            raise ValidationError('Обязательное поле')
        return self.cleaned_data['material']

    def __init__(self, *args, **kwargs):
        super(TempSaveForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
        self.fields['aim_of_receiving_gen'] = forms.ChoiceField(choices=AIMS, label='Мета приймання на ТЗ', required=True)
        self.fields['way_of_found'] = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
        self.fields['collection'] = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=False, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)

class InitialTempSaveForm(forms.Form):
    obj = forms.ModelChoiceField(queryset=Object.objects.all())


class TempRetForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('returned', 'Повернутий з тимчасового збереження'),
        ('add on PS', 'Поставити об’єкт на постійне збереження ')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(max_value=None, label='Кількість', required=True, min_value=0)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(label='Автор', required=True) #
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label='Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    price = forms.CharField(max_length=200, label='Вартість', required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    reason = forms.CharField(label='Підстава', required=True)
    side_1 = forms.CharField(max_length=100, label='Сторона 1 (акт повернення з ТЗ)', required=True)
    side_2 = forms.CharField(max_length=100, label='Сторона 2 (акт повернення з ТЗ)', required=True)
    return_mark = forms.ChoiceField(choices=choices, required=True, label='Позначка про повернення предмета або переведення до музейного зібрання (ПЗ) у книзі ТЗ')
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True) #

    def __init__(self, *args, **kwargs):
        super(TempRetForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
        self.fields['aim_of_receiving_gen'] = forms.ChoiceField(choices=AIMS, label='Мета приймання на ТЗ', required=True)
        self.fields['way_of_found'] = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
        self.fields['collection'] = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=False, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)

class PersistentSaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True) #
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=False) #
    side_1 = forms.CharField(max_length=200, label='Сторона 1 (акт ПЗ)', required=True)
    side_2 = forms.CharField(max_length=209, label='Сторона 2 (акт ПЗ)', required=True)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Матеріально-відповідальна особа',
                                                  required=True)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)
    inventory_number = forms.CharField(max_length=200, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=200, label='Спеціальний інвентарний номер', required=True)

    def __init__(self, *args, **kwargs):
        super(PersistentSaveForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
        self.fields['way_of_found'] = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
        self.fields['collection'] = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
        self.fields['storage'] = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)


class InventorySaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    date_detection = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Дата виявлення', required=True)
    place_detection = forms.CharField(max_length=200, label='Місце виявлення', required=True)
    date_existence = forms.CharField(max_length=200, label='Дата побутування', required=True)
    place_existence = forms.CharField(max_length=200, label='Місце побутування', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    mark_on_object = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Позначки на предметі', placeholder1='')
    classify = forms.ChoiceField(choices=get_choice(ROOT, 0, 'classify'), label='Класифікація', required=True)
    typology = forms.ChoiceField(choices=get_choice(ROOT, 0, 'typology'), label='Типологія', required=True)
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    bibliography = forms.CharField(max_length=1000, label='Бібліографія', required=True,
                                   widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    inventory_number = forms.CharField(max_length=100, label='Інвентарний номер', required=True)
    PS_code = forms.CharField(max_length=200, label='Шифр ПЗ (номер за книгою ПЗ)', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=False)
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Матеріально-відповідальна особа', required=True)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)
    old_registered_marks = forms.CharField(max_length=200, label='Старі облікові позначення', required=True)

    def __init__(self, *args, **kwargs):
        super(InventorySaveForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['mark_on_object'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Позначки на предметі', placeholder1='')
        self.fields['typology'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'typology'), label='Типологія', required=True)
        self.fields['classify'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'classify'), label='Класифікація', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
        self.fields['way_of_found'] = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
        self.fields['collection'] = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
        self.fields['storage'] = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)

class SpecInventorySaveForm(forms.Form):
    error_css_class = 'error'
    choices = (
        ('immediately', 'Термінова реставрація'),
        ('conservation', 'Консервація'),
        ('preventive', 'Профілактичний огляд')
    )
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
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
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    price = forms.CharField(max_length=40, label='Вартість', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    PS_code = forms.CharField(max_length=200, label='Шифр і номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи (акт приймання, протокол ФЗК, договір тощо)', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Матеріально-відповідальна особа', required=True)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Фізичне місце збереження (топографія)', required=True)

    def __init__(self, *args, **kwargs):
        super(SpecInventorySaveForm, self).__init__(*args, **kwargs)
        self.fields['storage'] = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['metals'] = Custom.MultiChoiceChoiceTextChoiceField(label='Дорогоцінні метали')
        self.fields['stones'] = Custom.MultiChoiceTextTextChoiceField(label='Дорогоцінне каміння')
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)


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
    collection = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
    PS_code = forms.CharField(label='Книга надходжень (номер)', max_length=50, required=True)
    inventory_number = forms.CharField(max_length=100, label='Інвентарний номер', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    old_inventory_numbers = forms.CharField(max_length=500, label='Старі інвентарні номери', required=True)
    collection_descr = forms.CharField(max_length=50, label='Колекційний опис (номер)', required=True)
    identifier = forms.CharField(label='Унікальний номер в інформаційній системі', max_length=50, required=True)
    negative = forms.CharField(label='Негатив (номер)', max_length=50, required=True)
    image = forms.ImageField(label='Фото', required=False)
    storage = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    author = forms.CharField(max_length=200, label='Автор або виробник', required=True)
    date_place_creation = forms.CharField(max_length=200, label='Час і місце створення (виготовлення)', required=True)
    date_place_detection = forms.CharField(max_length=200, label='Час і місце виявлення', required=True)
    date_place_existence = forms.CharField(max_length=200, label='Час і місце побутування', required=True)
    source = forms.CharField(max_length=200, label='Джерело надходження', required=True)
    way_of_found = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження (закупка, замовлення, дарунок, передача)', required=True)
    link_on_doc = forms.CharField(max_length=200, label='Документи', required=True)
    classify = forms.ChoiceField(choices=get_choice(ROOT, 0, 'classify'), label='Класифікація', required=True)
    typology = forms.ChoiceField(choices=get_choice(ROOT, 0, 'typology'), label='Типологія', required=True)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    size = Custom.MultiChoiceTextChoiceField(label='Виміри (см/мм)', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    metals = Custom.MultiChoiceChoiceTextChoiceField(label='Дорогоцінні метали')
    stones = Custom.MultiChoiceTextTextChoiceField(label='Дорогоцінне каміння')
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    person_or_actions = forms.CharField(max_length=2000, label='Особи чи події, пов’язані з предметом', required=True,
                                        widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    memorial_subject = forms.CharField(max_length=200, label='Зв’язок з іншими пам’ятками (історичний, мистецтвознавчий, культурологічний аспект)', required=True)
    extra_list = forms.CharField(max_length=2000, label='Додаткові відомості', required=True,
                                 widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    recomm_for_restauration = forms.ChoiceField(choices=choices, required=True, label='Рекомендації щодо реставрації')
    restoration = forms.CharField(max_length=2000, label='Реставрація (історія реставрації, зв’язок із журналом реставрації)', required=True,
                                  widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    transport_possibility = forms.BooleanField(label='Можливість транспортування (так, ні)', required=True)
    image_amount = forms.IntegerField(label='Кількість фотографій', min_value=0)
    price = forms.CharField(max_length=40, label='Оціночна вартість', required=True)
    attachment_amount = forms.IntegerField(label='Кількість додатків', min_value=0)
    exposition = forms.CharField(max_length=100, label='Експонування', required=True)
    existence_check = forms.CharField(max_length=100, label='Звіряння наявності (документ, дата)', required=True)
    bibliography = forms.CharField(max_length=1000, label='Бібліографія', required=True,
                                   widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    archive_materials = forms.CharField(max_length=200, label='Архівні матеріали', required=True)
    mat_person_in_charge = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Відповідальна особа')

    def __init__(self, *args, **kwargs):
        super(PassportForm, self).__init__(*args, **kwargs)
        self.fields['department'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'department'), label='Відомство', required=True)
        self.fields['adm_submission'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'department'), label='Адміністративне підпорядкування', required=True)
        self.fields['museum'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'museum'), label='Музей', required=True)
        self.fields['section'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'section'), label='Відділ', required=True)
        self.fields['collection'] = forms.ChoiceField(choices=COLLECTIONS, label='Фонд (колекція, відділ)', required=True)
        self.fields['storage'] = forms.ChoiceField(choices=TOPOGRAPHY, label='Топографічний шифр', required=True)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['way_of_found'] = forms.ChoiceField(choices=WAY_OF_FOUND_CHOICES, label='Спосіб надходження', required=True)
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['metals'] = Custom.MultiChoiceChoiceTextChoiceField(label='Дорогоцінні метали')
        self.fields['stones'] = Custom.MultiChoiceTextTextChoiceField(label='Дорогоцінне каміння')
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
        self.fields['typology'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'typology'), label='Типологія', required=True)
        self.fields['classify'] = forms.ChoiceField(choices=get_choice(ROOT, 0, 'classify'), label='Класифікація', required=True)


class FromPStoTSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    insurable_value = forms.CharField(max_length=30, label='Страхова вартість', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    side_1 = forms.CharField(max_length=200, label='Сторона 1 юридична особа', required=True)
    side_1_person_in_charge = forms.CharField(max_length=200, label='Сторона 1 головний зберігач (матеріально-відповідальна особа)', required=True)
    side_1_fond_saver = forms.CharField(max_length=200, label='Сторона 1 зберігач фонду', required=True)
    side_2 = forms.CharField(max_length=200, label='Сторона 2 юридична особа', required=True)
    side_2_person_in_charge = forms.CharField(max_length=200, label='Сторона 2 відповідальна особа/приватна особа', required=True)
    aim_of_receiving_gen = forms.CharField(max_length=500, label='Мета передачі на ТЗ', required=True)
    #                                   widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 520px;"}))
    reason = forms.CharField(label='Підстава (посилання на документи: договір, наказ директора, наказ вищої інстанції тощо)', max_length=400, required=True)
    term_back = forms.DateField(label='Дата повернення', widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                                        "pickTime": False},
                                                                               attrs={'width': '300px'}))
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    TS_code = forms.CharField(max_length=100, label='Шифр та номер ТЗ (актуальний)', required=True)
    is_there = forms.ChoiceField(choices=PLACE[2:4], label='Фізичне місце збереження (топографія) – позначка про відсутність (за межами фондосховища, за межами музею)', required=True)

    def __init__(self, *args, **kwargs):
        super(FromPStoTSForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)


class FromTStoPSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    date_creation = forms.CharField(max_length=20, label='Дата створення предмета', required=True)
    place_of_creation = forms.CharField(max_length=200, label='Місце створення предмета', required=True)
    author = forms.CharField(max_length=200, label='Автор', required=True)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    insurable_value = forms.CharField(max_length=30, label='Страхова вартість', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
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

    def __init__(self, *args, **kwargs):
        super(FromTStoPSForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)


class SendOnPSForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    technique = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=True)
    material = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
    size = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
    condition = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
    condition_descr = forms.CharField(max_length=2000, label='Опис стану збереженості', required=True,
                                      widget=forms.widgets.Textarea(attrs={'style': "margin: 0px; height: 252px; width: 550px;"}))
    description = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
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

    def __init__(self, *args, **kwargs):
        super(SendOnPSForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['technique'] = forms.ChoiceField(choices=TECHNIQUE_CHOICES, label='Техніка', required=False)
        self.fields['material'] = forms.CharField(label = 'Матеріали', required=True, widget=SelectMultiple(choices=MATERIAL_CHOICES))
        self.fields['size'] = Custom.MultiChoiceTextChoiceField(label='Виміри', required=True)
        self.fields['condition'] = forms.ChoiceField(choices=CONDITIONS, label='Стан збереженості (тип)', required=True)
        self.fields['description'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', size1=2000, label='Опис предмета', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)


class WritingOffForm(forms.Form):
    error_css_class = 'error'
    name = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
    is_fragment = forms.BooleanField(label='Фрагмент(не повний)?', required=False)
    amount = forms.IntegerField(label='Кількість', required=True, min_value=0)
    note = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)
    main_saver = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Головний зберігач', required=True)
    fond_saver = forms.ModelChoiceField(queryset=Custom.myUser.objects.all(), label='Зберігач фонду', required=True)
    reason = forms.CharField(label='Причина', max_length=400, required=True)
    circumstance = forms.CharField(label='Обставини ', max_length=400, required=True)
    link_on_doc = forms.CharField(max_length=200, label='Посилання на документи: акти звірення, погодження Міністерства культури тощо', required=False)
    PS_code = forms.CharField(max_length=200, label='Шифр та номер за книгою надходжень (ПЗ)', required=True)
    inventory_number = forms.CharField(max_length=100, label='Шифр і номер за Інвентарної книгою', required=True)
    spec_inventory_numb = forms.CharField(max_length=100, label='Спеціальний інвентарний номер', required=True)
    TS_code = forms.CharField(max_length=50, label='Шифр ТЗ (номер за книгою ТЗ)', required=True)
    is_there = forms.ChoiceField(choices=PLACE[2:4], label='Фізичне місце збереження (топографія) – позначка про відсутність (за межами фондосховища, за межами музею)', required=True)

    def __init__(self, *args, **kwargs):
        super(WritingOffForm, self).__init__(*args, **kwargs)
        self.fields['name'] = Custom.TextChoiceField(choices=LANGUAGE_CHOICES, label='Назва', placeholder1='', required=True)
        self.fields['note'] = Custom.TextAreaChoiceField(choices=LANGUAGE_CHOICES, placeholder1='', label='Примітка', required=True)


class ObjectEditForm(ModelForm):
    class Meta:
        model = Object
        fields = '__all__'

class AutForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логiн:')
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label='Пароль:')

def get_xml(root, prefix, value, level=0):
    choice = ()
    for s in root:
        if s.getchildren():
            choice += get_xml(s, prefix+s.attrib['label']+', ', value+s.tag+',', level+1)
        else:
            choice = ((value[:-1], prefix[:-2]),)
            break
    if not level:
        return (('', ''),) + choice
    else:
        return choice

class XMLForm(forms.Form):
    choicefield = forms.CharField(label='Куда добавить', required=True, widget=Select(choices=get_xml(ROOT, '', '', 0)))
    charfield = forms.CharField(label='Что добавить', required=True)