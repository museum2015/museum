
import datetime
from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select
# Create your models here. test


def get_image_path(self, filename):
        path = ''.join(["/",filename])
        return path


class Material:
    class MaterialWidget(MultiWidget):
        def __init__(self):
            widgets = [TextInput(attrs={'size': 30, 'maxlength': 30}),
                       TextInput(attrs={'size': 10, 'maxlength': 10})]
            super(Material.MaterialWidget, self).__init__(widgets)
        def decompress(self, value):
            if value:
                return value.split(':')
            return [None, None]

    class MaterialField(MultiValueField):
        def __init__(self, *args, **kwargs):
            list_fields = [fields.CharField(max_length=30),
                           fields.CharField(max_length=30)]
            super(Material.MaterialField, self).__init__(list_fields, widget=Material.MaterialWidget(), *args, **kwargs)
        def compress(self, values):
            if values:
                return values[0] + ':' + values[1] + ';'
            else:
                return ''

    class MultiMaterialWidget(MultiWidget):
        def __init__(self, number=5):
            widgets = []
            for i in range(number):
                widgets.append(Material.MaterialWidget())
            super(Material.MultiMaterialWidget, self).__init__(widgets)
        def decompress(self, value):
            if value:
                return value.split(';')
            else:
                return []

    class MultiMaterialField(MultiValueField):
        def __init__(self, number=5, *args, **kwargs):
            list_fields = []
            for i in range(number):
                list_fields.append(Material.MaterialField())
            super(Material.MultiMaterialField, self).__init__(list_fields, widget=Material.MultiMaterialWidget(number), *args, **kwargs)

        def compress(self, values):
            result = ''
            for value in values:
                result += value
            return result


class MaterialForm(forms.Form):
    your_name = Material.MultiMaterialField()

class Object(models.Model):
    collection = models.CharField(max_length=200, default='')
    name_title = models.CharField(max_length=200, default='')
    name_lang = models.CharField(max_length=200, default='')
    name_type = models.CharField(max_length=200, default='')
    is_fragment = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    size_type = models.CharField(max_length=200, default='')
    size_number = models.IntegerField(default=0)
    size_measurement_unit = models.CharField(max_length=200, default='')
    _class = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=200, default='')
    material = models.CharField(max_length=200, default='')
    #measurement = models.CharField(default=False)
    technique = models.CharField(max_length=200, default='')
    description = models.TextField(max_length=1000, default='')
    description_lang = models.CharField(max_length=50, default='')
    description_type = models.CharField(max_length=200, default='')
    identifier = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to=get_image_path)
    image_type = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=100, default='')
    author_type = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    price_type = models.CharField(max_length=50, default='')
    mark_on_object = models.CharField(max_length=200, default='')
    mark_type = models.CharField(max_length=50, default='')
    note = models.CharField(max_length=200, default='')
    note_type = models.CharField(max_length=50, default='')
    mark_note_lang=models.CharField(max_length=30, default='')
    condition_descr=models.CharField(max_length=500, default='')
    condition_saved=models.CharField(max_length=100, default='')
    transport_possibility=models.BooleanField(default=False)
    recomm_for_restauration=models.CharField(max_length=100, default='')
    restauration_notes = models.CharField(max_length=200, default='')
    place=models.CharField(max_length=200, default='')
    place_appellation = models.CharField(max_length=200, default='')
    is_there = models.CharField(max_length=200, default='')
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200, default='')
    #link_on_doc = models.CharField(max_length=200)
    #doc_type = models.CharField(max_length=50)
    transfered_from = models.CharField(max_length=200, default='')
    transfered_to = models.CharField(max_length=200, default='')
    term_back=models.DateTimeField(max_length=200, default='2000-02-12 00:00')
    aim_of_receiving_gen = models.CharField(max_length=200, default='')
    #aim_of_receiving = models.ForeignKey(Events)
    circumst_write_off = models.CharField(max_length=200, default='')



    



