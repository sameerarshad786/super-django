import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Get the request body
        request_data = json.loads(request.body)
        print(json.dumps(request_data))
        
        # Process the request and prepare the response
        # ...
        
        # Send the response back to Dialogflow
        response = {
            'fulfillmentText': 'Hello from Django webhook!'
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request method'})
