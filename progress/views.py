from django.shortcuts import render


def index(request):
    context = {
        'title': 'Прогресс',
        'content': 'Здесь будет статистика'
    }
    return render(request, "progress/index.html", context)
