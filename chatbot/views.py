import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDELINES_PATH = os.path.join(os.path.dirname(__file__), 'data', 'guidelines.json')

with open(GUIDELINES_PATH, 'r', encoding='utf-8') as f:
    GUIDELINES = json.load(f)

@api_view(['POST'])
def chat_api(request):
    text = request.data.get('message', '') or request.data.get('text', '')
    if not text:
        return Response({"reply": "\n".join(GUIDELINES['default']['advice'])})

    m = text.lower()
    reply_list = []
    if 'fever' in m:
        reply_list = GUIDELINES['fever']['advice']
    elif 'cold' in m or 'cough' in m:
        reply_list = GUIDELINES['cold']['advice']
    elif 'vomit' in m:
        reply_list = GUIDELINES['vomiting']['advice']
    elif 'pain' in m or 'ache' in m:
        reply_list = GUIDELINES['pain']['advice']
    else:
        reply_list = GUIDELINES['default']['advice']

    reply = "\n".join(reply_list)
    return Response({"reply": reply})
