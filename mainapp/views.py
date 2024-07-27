from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def mappage(request):
    return render(request, 'mainapp/mappage.html')

@csrf_exempt  # Disable CSRF protection only if absolutely necessary
def store_distance_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            source_add = data.get('source')
            dest_add = data.get('destination')
            source_lat = data.get('source_lat')
            source_lon = data.get('source_lon')
            destination_lat = data.get('destination_lat')
            destination_lon = data.get('destination_lon')
            distance = data.get("distance")
            date = data.get('date')
            time_taken = data.get('time_taken')
            is_electric = data.get('is_Electric')
            mode_of_transport = data.get('mode_of_transport')

            print(source_add, source_lat, source_lon, dest_add, destination_lon, destination_lat, distance,
                  date, time_taken, is_electric, mode_of_transport, sep="\n")

            # You can save the data to the database here

            # Redirect to the same page to refresh
            return redirect('mappage')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
