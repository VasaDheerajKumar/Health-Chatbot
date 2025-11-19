from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def chat_api(request):
    return Response({"reply": "Service not ready yet. Use next steps."})


