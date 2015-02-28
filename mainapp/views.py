from django.shortcuts import render, HttpResponse
from models import MaterialForm, Object, Material
from django.views.decorators.csrf import csrf_protect

# Create your views here.
#test branch 2 attempt

@csrf_protect
def get_material(request):
    form = MaterialForm()
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse(cd['your_name'])
        else:
            form = MaterialForm()
    return render(request, 'form.html', {'form': form})


