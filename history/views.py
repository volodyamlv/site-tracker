from django.shortcuts import render

from history.models import WorkoutHistory

# Create your views here.
def history_list(request):
    history_data = WorkoutHistory.objects.filter(user=request.user).order_by('-date_created', 'template_name', 'exercise_name')
    grouped_data = {}
    
    for item in history_data:
        date_str = item.date_created.strftime("%Y-%m-%d")
        if date_str not in grouped_data:
            grouped_data[date_str] = {}
        if item.template_name not in grouped_data[date_str]:
            grouped_data[date_str][item.template_name] = {}
        if item.exercise_name not in grouped_data[date_str][item.template_name]:
            grouped_data[date_str][item.template_name][item.exercise_name] = 0
        grouped_data[date_str][item.template_name][item.exercise_name] += 1
    
    context = {
        'grouped_data': grouped_data,
    }
    return render(request, 'history/history.html', context)




def detail(request, template_name, date):
    workouts = WorkoutHistory.objects.filter(user=request.user, template_name=template_name, date_created=date).order_by('exercise_name')
    grouped_data = {}
    
    for workout in workouts:
        if workout.exercise_name not in grouped_data:
            grouped_data[workout.exercise_name] = []
        grouped_data[workout.exercise_name].append(workout)
    
    context = {
        'template_name': template_name,
        'date': date,
        'grouped_data': grouped_data,
    }
    return render(request, 'history/detail.html', context)