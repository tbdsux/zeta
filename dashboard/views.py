from django.shortcuts import render

# dashboard index
def index(request):
    return render(request, 'main/index.html')

# dashboard collections
def collections(request):
    return render(request, 'main/collections.html')

# dashboard browse
def browse(request):
    return render(request, 'main/browse.html')