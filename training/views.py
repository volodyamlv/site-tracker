from django.shortcuts import render, redirect, get_object_or_404
from .models import Template, Exercise
from .forms import TemplateForm, ExerciseForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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


def template_detail(request, pk):
    template = get_object_or_404(Template, pk=pk, user=request.user)
    exercises = Exercise.objects.filter(template=template)
    return render(
        request,
        "training/template_detail.html",
        {"template": template, "exercises": exercises},
    )


def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == "POST":
        form = UserExerciseDataForm(request.POST)
        if form.is_valid():
            exercise_data = form.save(commit=False)
            exercise_data.user = request.user
            exercise_data.exercise = exercise
            exercise_data.save()
            return redirect("workout_detail", pk=exercise.workout_template.pk)

    return render(
        request, "exercises/exercise_detail.html", {"exercise": exercise, "form": form}
    )
