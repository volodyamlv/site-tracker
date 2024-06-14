from django.shortcuts import render, redirect, get_object_or_404
from .models import Template, Exercise
from .forms import TemplateForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from history.models import WorkoutHistory
def index(request):
    context = {"title": "Тренировки", "content": "Тут будут тренировки"}
    return render(request, "training/index.html", context)


def template_list(request):
    templates = Template.objects.filter(user=request.user).order_by('-id').prefetch_related(
        "exercise_set"
    )
    return render(request, "training/templates_list.html", {"templates": templates})


def template_create(request):
    errors = []

    if request.method == "POST":
        template_form = TemplateForm(request.POST)
        exercise_names = request.POST.getlist("exercise_name")
        exercise_sets = request.POST.getlist("exercise_sets")

        # Проверка на наличие хотя бы одного упражнения
        if not any(exercise_names) or not all(exercise_names) or not all(exercise_sets):
            errors.append("Заполните все поля")

        if template_form.is_valid() and not errors:
            template = template_form.save(commit=False)
            template.user = request.user
            template.save()

            for name, sets in zip(exercise_names, exercise_sets):
                if name and sets:
                    exercise = Exercise(name=name, sets=sets, template=template)
                    exercise.save()

            return redirect("training:template_list")
        else:
            if not template_form.is_valid():
                errors.append("Введите название шаблона")

    else:
        template_form = TemplateForm()

    return render(
        request,
        "training/template_form.html",
        {"template_form": template_form, "errors": errors},
    )


@require_POST
def template_delete(request, pk):
    template = get_object_or_404(Template, pk=pk, user=request.user)
    template.delete()
    return JsonResponse({'status': 'success'})


# def template_detail(request, pk):
#     template = get_object_or_404(Template, pk=pk, user=request.user)
#     exercises = Exercise.objects.filter(template=template)
#     return render(
#         request,
#         "training/template_detail.html",
#         {"template": template, "exercises": exercises},
#     )


def exercise_form(request, pk):
    template = get_object_or_404(Template, pk=pk)
    exercises = template.exercise_set.all()  # Получаем все упражнения для данного шаблона

    exercises_with_sets = [(exercise, range(exercise.sets)) for exercise in exercises]

    if request.method == 'POST':
        for exercise in exercises:
            for i in range(exercise.sets):
                weight = request.POST.get(f'weight_{exercise.pk}_{i}')
                amount = request.POST.get(f'amount_{exercise.pk}_{i}')
                if weight and amount:
                    WorkoutHistory.objects.create(
                        user=request.user,
                        template_name=template.name,
                        exercise_name=exercise.name,
                        weight=weight,
                        amount=amount
                    )
        return redirect("training:template_list")  # Перенаправление на страницу успешного сохранения

    context = {
        'template': template,
        'exercises_with_sets': exercises_with_sets,  # Передаем список кортежей
    }

    return render(request, 'training/exercise_form.html', context)
