from django.shortcuts import render

# Create your views here.
import cv2
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from urine_strip_app.models import UrineStrip
from urllib.request import urlretrieve
from PIL import Image
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_http_methods(["POST"])
@csrf_exempt
@require_POST
def process_image(request):
    if request.method == 'POST':
        # Get the image from the request
        img_url = request.POST.get('img_url')
        if img_url:
            # Download the image and save it to a local file
            img_path, _ = urlretrieve(img_url)
            img = cv2.imread(img_path)

            # Define the colors to be detected on the urine strip
            colors = {
                'color_1': (255, 255, 255),
                'color_2': (240, 255, 0),
                'color_3': (31, 223, 0),
                'color_4': (0, 192, 0),
                'color_5': (0, 160, 0),
                'color_6': (0, 128, 0),
                'color_7': (0, 96, 0),
                'color_8': (0, 64, 0),
                'color_9': (0, 32, 0),
                'color_10': (0, 0, 0),
            }

            # Detect the colors on the urine strip
            results = {}
            for color_name, color_value in colors.items():
                mask = cv2.inRange(img, color_value, color_value)
                count = cv2.countNonZero(mask)
                results[color_name] = count

            # Save the results to the database
            urine_strip = UrineStrip(image=img_url, result=results)
            urine_strip.save()

            # Return the results as a JSON response
            return JsonResponse(results)

    return JsonResponse({'error': 'Invalid request method'})
