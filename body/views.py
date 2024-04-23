from django.shortcuts import render


def index(request):
    context = {
        'title': 'Тело',
        'content': 'Тут будут информация о теле'
    }
    return render(request, "body/index.html", context)
