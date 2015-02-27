from django.shortcuts import render, HttpResponse
from models import MaterialForm, Object, Material
# Create your views here.
#test branch 2 attempt

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