from django.shortcuts import render


def index(request):
    context = {
        'title': 'Тренировки',
        'content': 'Тут будут тренировки'
    }
    return render(request, "training/index.html", context)
