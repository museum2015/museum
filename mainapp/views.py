from django.shortcuts import render, HttpResponse
from models import Test_Form , Object,MultiMaterialField
# Create your views here.

def TestView(request):
    if request.method == 'POST':
        form = Test_Form(request.POST)
        return HttpResponse(form.qwe)
        #return render(request, 'form.html', {'form': form})
    else:
        form = Test_Form()
        return render(request, 'form.html', {'form': form})