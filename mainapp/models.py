# -*- coding: utf-8 -*-

from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User

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
    actor = models.ForeignKey(myUser)
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



