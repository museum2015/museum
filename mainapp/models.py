#asdhgash
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
        list_fields = [fields.CharField(),
                       fields.CharField()]
        super(MaterialField, self).__init__(list_fields, widget=MaterialWidget(), *args, **kwargs)
    def compress(self, values):
        return values[0] + ':' + values[1] + ';'
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

class Test_Form(forms.Form):
    #material = MultiMaterialField()
    qwe = forms.CharField()


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
    identifier = models.CharField(max_length=50)
    image = models.ImageField()
    image_type = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    author_type = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    price_type = models.CharField(max_length=50)
    mark_on_object = models.CharField(max_length=200)
    mark_type = models.CharField(max_length=50)
    note = models.CharField(max_length=200)
    note_type = models.CharField(max_length=50)
    mark_note_lang=models.CharField(max_length=30)
    condition_descr=models.CharField(max_length=500)
    condition_saved=models.CharField(max_length=100)
    transport_possibility=models.BooleanField(default=False)
    recomm_for_restauration=models.CharField(max_length=100)
    restauration_notes = models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    place_appellation = models.CharField(max_length=200)
    is_there = models.CharField(max_length=200)
    #documented_in = models.CharField(max_length=200)
    #documented_type = models.CharField(max_length=50)
    way_of_found = models.CharField(max_length=200)
    #link_on_doc = models.CharField(max_length=200)
    #doc_type = models.CharField(max_length=50)
    transfered_from = models.CharField(max_length=200)
    transfered_to = models.CharField(max_length=200)
    term_back=models.DateTimeField(max_length=200)
    aim_of_receiving_gen = models.CharField(max_length=200)
    #aim_of_receiving = models.ForeignKey(Events)
    circumst_write_off = models.CharField(max_length=200)



    



