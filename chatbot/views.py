import json
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import LLM classifier
from .ai_client import classify_text

# Load guidelines JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDELINES_PATH = os.path.join(os.path.dirname(__file__), 'data', 'guidelines.json')

with open(GUIDELINES_PATH, 'r', encoding='utf-8') as f:
    GUIDELINES = json.load(f)


@api_view(['POST'])
def chat_api(request):
    """
    Main chatbot endpoint:
    - Takes user message
    - Sends to LLM classifier
    - Extracts symptoms_present and symptoms_absent
    - Gives WHO-based care instructions
    """

    # 1. Get message
    text = request.data.get('message', '') or request.data.get('text', '')
    if not text.strip():
        return Response({
            "reply": "\n".join(GUIDELINES['default']['advice']),
            "diagnosis": None
        })

    # 2. Run AI classifier
    result = classify_text(text)
    present = [s.lower() for s in result.get('symptoms_present', [])]
    absent = [s.lower() for s in result.get('symptoms_absent', [])]

    # 3. Find advice for symptoms PRESENT (ignore symptoms_absent)
    reply_items = []

    for s in present:
        if s in GUIDELINES:
            reply_items.extend(GUIDELINES[s]["advice"])

    # 4. If no known symptoms → use default safe advice
    if not reply_items:
        reply_items = GUIDELINES["default"]["advice"]

    # 5. Create final reply text
    reply = "\n".join(reply_items)

    # 6. Return response
    return Response({
        "reply": reply,
        "diagnosis": result  # shows symptoms_present/absent, language
    })
