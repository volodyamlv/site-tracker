from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def search_food(request):
    if request.method == "POST":
        food_input = request.POST.get("food_input")
        print(food_input)
        if food_input:
            URL = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=" + os.getenv('API_KEY');

            response = requests.post(
                URL,
                json={"query": food_input, "dataType": ["Survey (FNDDS)"]},
            )
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Food input is empty"}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


def index(request):
    context = {"title": "Еда", "content": "Здесь еда"}
    return render(request, "food/index.html", context)
