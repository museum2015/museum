from django.shortcuts import render, HttpResponse
from models import MaterialForm, TempSaveForm, Object, Material
from django.views.decorators.csrf import csrf_protect

# Create your views here.
#test branch 2 attempt

@csrf_protect
def TempSave(request):
    form = TempSaveForm()
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = Object()
            obj.name_title=cd['name']
            obj.collection=cd['collection']
            #...and so on...
            obj.save()
        else:
            form = MaterialForm()
    return render(request, 'form.html', {'form': form})


