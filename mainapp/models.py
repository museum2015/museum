from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select
# Create your models here.


class MaterialWidget(MultiWidget):
    def __init__(self):
        widgets = [TextInput(attrs={'size': 30, 'maxlength': 30}),
                   TextInput(attrs={'size': 10, 'maxlength': 10})]
        super(MaterialWidget, self).__init__(widgets)
    def decompress(self, value):
        if value:
            return value.split(':')
        return [None, None]


class MaterialField(MultiValueField):
    def __init__(self, *args, **kwargs):
        list_fields = [forms.CharField(max_length=30),
                       forms.CharField(max_length=10)]
        super(MaterialField, self).__init__(list_fields, widget=MaterialWidget(), *args, **kwargs)
    def compress(self, values):
        if values:
            return values[0] + ':' + values[1] + ';'
        else:
            return ''
        #return values

class MultiMaterialWidget(MultiWidget):
    def __init__(self, number=5):
        widgets = []
        for i in range(number):
            widgets.append(MaterialWidget())
        super(MultiMaterialWidget, self).__init__(widgets)
    def decompress(self, value):
        res=[]
        if value:
            return value.split(';')
        else:
            return []

class MultiMaterialField(MultiValueField):
    def __init__(self, number=5, *args, **kwargs):
        list_fields = []
        for i in range(number):
            list_fields.append(MaterialField())
        super(MultiMaterialField, self).__init__(list_fields, widget=MultiMaterialWidget(number), *args, **kwargs)

    def compress(self, values):
        result = ''
        for value in values:
            result += value
        return result


class MaterialForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    your_name = MultiMaterialField()

class Object(models.Model):
    collection = models.CharField(max_length=200)
    name_title = models.CharField(max_length=200)
    name_lang = models.CharField(max_length=200)
    name_type = models.CharField(max_length=200)
    is_fragment = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    size_type = models.CharField(max_length=200)
    size_number = models.IntegerField(default=0)
    size_measurement_unit = models.CharField(max_length=200)
    _class = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    material = models.CharField(max_length=200)
    #measurement = models.CharField(default=False)
    technique = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    description_lang = models.CharField(max_length=50)
    description_type = models.CharField(max_length=200)




