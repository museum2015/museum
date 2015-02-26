from django.shortcuts import render, HttpResponse
from models import MaterialForm, Object, MultiMaterialField
# Create your views here.

def get_material(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MaterialForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse(cd['your_name'])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MaterialForm()

    return render(request, 'form.html', {'form': form})