from django.shortcuts import render, redirect, get_object_or_404
from .models import Template, Exercise
from .forms import TemplateForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from history.forms import WorkoutHistoryForm
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
                errors.append("Template name is required.")

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
    
    if request.method == 'POST':
        forms = []
        for exercise in exercises:
            form = WorkoutHistoryForm(request.POST, prefix=f'exercise_{exercise.pk}')
            forms.append(form)
        
        if all(form.is_valid() for form in forms):
            for form in forms:
                workout_history = form.save(commit=False)
                workout_history.user = request.user
                workout_history.template_name = template.name
                workout_history.exercise_name = exercises.get(pk=int(form.prefix.split('_')[1])).name
                workout_history.save()
            return redirect("training:template_list")  # Перенаправление на страницу успешного сохранения
    else:
        forms = [WorkoutHistoryForm(prefix=f'exercise_{exercise.pk}') for exercise in exercises]
    
    exercise_forms = zip(exercises, forms)  # Связываем упражнения с соответствующими формами
    
    context = {
        'template': template,
        'exercise_forms': exercise_forms,
    }
    
    return render(request, 'training/exercise_form.html', context)
