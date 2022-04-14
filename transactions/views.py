from django.shortcuts import render
from .forms import ArquivoForm
from django.http import HttpResponseRedirect

def index(request):
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['arquivo']
            print(file.name)
            print(file.size)
            for line in file.readlines():
                print(line)
            return HttpResponseRedirect('.')
    else:
        form = ArquivoForm()
        return render(request, 'index.html', {'form': form})