import os
import json

# Example using OpenAI's python client (replace if using another)
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

CLASSIFY_PROMPT = """
You are a classifier that extracts medical symptoms a user HAS and DOES NOT HAVE.
Return JSON only in this exact schema:
{"language": "<iso>", "symptoms_present": ["fever","headache"], "symptoms_absent": ["cold"]}
Understand negations like 'no cold', 'not coughing', 'fever but no cold'.
User message: """


def classify_text(message: str) -> dict:
    prompt = CLASSIFY_PROMPT + json.dumps(message)
    # Use completion or responses API depending on your client; this is minimal example
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0
    )
    text = resp.choices[0].text.strip()
    try:
        return json.loads(text)
    except Exception:
        # If parsing fails, return fallback (assume english and simple present detection)
        lower = message.lower()
        present = []
        absent = []
        for k in ['fever','cold','cough','vomit','vomiting','pain','headache']:
            if f'no {k}' in lower or f'not {k}' in lower:
                absent.append(k)
            elif k in lower:
                present.append(k)
        return {"language": "en", "symptoms_present": present, "symptoms_absent": absent}
