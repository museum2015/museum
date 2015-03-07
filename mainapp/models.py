import datetime
from django import forms
from django.db import models
from django.forms import fields, MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your models here. test


def get_image_path(self, filename):
    path = ''.join(["/", filename])
    return path


class Custom:
    class MaterialWidget(MultiWidget):
        def __init__(self, size1=10, size2=10):
            widgets = [TextInput(attrs={'size': size1, 'max_length': 30}),
                       TextInput(attrs={'size': size2, 'max_length': 10})]
            super(Custom.MaterialWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                res = value.split(':')
                return res
            else:
                return [None, None]

        def format_output(self, rendered_widgets):
            res = u''.join(rendered_widgets)
            res += '<br>'
            return res

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
        def __init__(self, number=5):
            widgets = []
            for i in range(number):
                widgets.append(Custom.MaterialWidget())
            super(Custom.MultiMaterialWidget, self).__init__(widgets)

        def decompress(self, value):
            if value:
                return value.split(';')
            else:
                return []
                # def format_output(self, rendered_widgets):


    class MultiMaterialField(MultiValueField):
        def __init__(self, number=5, *args, **kwargs):
            list_fields = []
            for i in range(number):
                list_fields.append(Custom.MaterialField())
            super(Custom.MultiMaterialField, self).__init__(list_fields, widget=Custom.MultiMaterialWidget(number),
                                                            *args, **kwargs)

        def compress(self, values):
            result = ';'
            return result.join(values)


class Object(models.Model):
    collection = models.CharField(max_length=200, default='')  #
    is_fragment = models.BooleanField(default=False)
    name = models.CharField(max_length=200, default='')  #
    name_lang = models.CharField(max_length=200, default='')  ##
    name_type = models.CharField(max_length=200, default='')
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
    description_lang = models.CharField(max_length=50, default='')  ##
    description_type = models.CharField(max_length=200, default='')  ##
    identifier = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to=get_image_path, default='default.jpg')
    image_type = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=100, default='')  #
    author_type = models.CharField(max_length=50, default='')  ##
    price = models.CharField(max_length=50, default='')  #
    price_type = models.CharField(max_length=50, default='')  ##
    mark_on_object = models.CharField(max_length=200, default='')  ##
    mark_type = models.CharField(max_length=50, default='')  ##
    note = models.CharField(max_length=200, default='')  #
    note_type = models.CharField(max_length=50, default='')  ##
    mark_note_lang = models.CharField(max_length=30, default='')  ##
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
    name = forms.CharField(max_length=200, label='Name', required=False)  #
    is_fragment = forms.BooleanField(label='Is it fragment?', required=False)  #
    amount = forms.IntegerField(max_value=1000, label='Amount', required=False)  #
    #date_creation = forms.CharField(max_length=20, label='Date of creation', required=False)
    #place_of_creation = forms.CharField(max_length=200, label='Place of creation', required=False)
    author = forms.CharField(max_length=200, label='Author', required=False)  #
    technique = forms.CharField(max_length=200, label='Technique', required=False)  #
    material = Custom.MultiMaterialField(required=False)  #
    # size_type = forms.CharField(max_length=200, label='Type of size', required=False)#
    size = Custom.MultiMaterialField(number=1, required=False)  #
    #size_measurement_unit = forms.CharField(max_length=50, label='Measurement Unit')
    #measurement =
    #condition_descr = forms.CharField(max_length=200, label='Description of condition', required=False)#
    condition = forms.CharField(max_length=200, label='Condition', required=False)  #
    description = forms.CharField(max_length=500, label='Description', required=False)  #
    price = forms.CharField(max_length=200, label='Price', required=False)  #
    note = forms.CharField(max_length=200, label='Note', required=False)  #
    side_1 = forms.CharField(max_length=200, label='Object transferred from', required=False)  #
    side_2 = forms.CharField(max_length=200, label='Object transferred to', required=False)  #
    aim_of_receiving_gen = forms.CharField(max_length=200, label='Aim of receiving', required=False)  #
    way_of_found = forms.CharField(max_length=200, label='Way of found', required=False)  #
    reason = forms.CharField(max_length=200, label='Reason', required=False)  #
    source = forms.CharField(max_length=200, label='Source', required=False)  #
    collection = forms.CharField(max_length=200, label='Collection', required=False)  #
    term_back = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Term of get back', required=False)  #
    code = forms.CharField(max_length=50, label='Code of TS', required=False)  #
    #date_write_TS = forms.DateTimeField(input_formats=['%Y-%m-%d'],label='Date of writing in the book of TS')

    mat_person_in_charge = forms.CharField(max_length=50, label='Person in charge', required=False)
    storage = forms.CharField(max_length=200, label='Storage', required=False)  #
    #ne nado, v activity est' #writing_person = forms.CharField(max_length=50, label='Person who writes is TS book')
    #return_mark = forms.BooleanField(label='Is it returned?')


class InitialTempSaveForm(forms.Form):
    obj = forms.ModelChoiceField(queryset=Object.objects.all())


class TempRetForm(forms.Form):
    choices = (
        ('returned', 'returned from TS'),
        ('add on PS', 'Adding the object on a persistent storage')
    )
    name = forms.CharField(max_length=200, label='Name', required=False)  #
    is_fragment = forms.BooleanField(label='Is it fragment?', required=False)  #
    amount = forms.IntegerField(max_value=None, label='Amount', required=False)  #
    #date_creation = forms.CharField(max_length=20, label='Date of creation', required=False)
    #place_of_creation = forms.CharField(max_length=200, label='Place of creation', required=False)
    author = forms.CharField(max_length=200, label='Author', required=False)  #
    technique = forms.CharField(max_length=200, label='Technique', required=False)  #
    material = Custom.MultiMaterialField(required=False)  #
    size_type = forms.CharField(max_length=200, label='Type of size', required=False)  #
    size = Custom.MaterialField(size1=2, size2=3, required=False)  #
    condition = forms.CharField(max_length=200, label='Condition', required=False)  #
    condition_descr = forms.CharField(max_length=200, label='Description of condition', required=False)
    description = forms.CharField(max_length=500, label='Description', required=False)  #
    price = forms.CharField(max_length=200, label='Price', required=False)  #
    term_back = forms.DateTimeField(input_formats=['%Y-%m-%d'], label='Term of get back', required=False)
    note = forms.CharField(max_length=200, label='Note', required=False)  #
    side_1 = forms.CharField(max_length=100, label='First side', required=False)
    side_2 = forms.CharField(max_length=100, label='Second side', required=False)
    return_mark = forms.ChoiceField(choices=choices, required=False)
    save_place = forms.CharField(max_length=200, label='Place of saving', required=False)


class PersistentSaveForm(forms.Form):
    choices=(
        ('immediately', 'Immediately restoration'),
        ('conservation', 'Conservation'),
        ('preventive', 'Preventive view')
    )
    name = forms.CharField(max_length=200, label='Name', required=False)
    is_fragment = forms.BooleanField(label='Is it fragment?', required=False)
    amount = forms.IntegerField(label='Amount', required=False)
    #date_creation = forms.CharField(label='Date of creating', required=False)
   # place_of_creating = forms.CharField(max_length=200, label='Place of creating', required=False)
    author = forms.CharField(max_length=200, label='Author', required=False)
    technique = forms.CharField(max_length=200, label='Technique', required=False)
    material = Custom.MultiMaterialField(required=False)
    size = Custom.MaterialField(size1=2, size2=3, required=False)
    description = forms.CharField(max_length=200, label='Description', required=False)
    condition = forms.CharField(max_length=200, label='Condition', required=False)
    can_transport = forms.BooleanField(label='Can be transported?(y/n)', required=False)
    recommandation_rest = forms.ChoiceField(choices=choices, required=False)
    conservation_descr = forms.CharField(max_length=200,label='Description of conservation state', required=False)
    price = forms.CharField(max_length=40, label='Price', required=False)
    note = forms.CharField(max_length=200, label='Note', required=False)
    PS_code = forms.CharField(max_length=200, label='Persistent save code', required=False)
    way_of_found = forms.CharField(max_length=200, label='Way of found', required=False)
    link_on_doc = forms.CharField(max_length=200, label='Link on document', required=False)
    mat_person_in_charge = forms.CharField(max_length=50, label='Person in charge', required=False)
    side_1 = forms.CharField(max_length=200, label='Side 1', required=False)
    side_2 = forms.CharField(max_length=209, label='Side 2', required=False)
    fond = forms.CharField(max_length=200, label='Fond(collection, department)', required=False)
    save_place = forms.CharField(max_length=200, label='Place of saving', required=False)
    old_registered_marks = forms.CharField(max_length=200, label='Old registered marks', required=False)
    inventory_number = forms.CharField(max_length=200, label='Inventory number', required=False)
    spec_inventory_numb = forms.CharField(max_length=200, label='Special inventory number', required=False)



