import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# ✅ Your Groq API Key
GROQ_API_KEY = os.getenv("GROK_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"  # ✅ UPDATED MODEL

class ActionSmartFinanceAdvice(Action):
    def name(self):
        return "action_smart_finance_advice"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        user_message = tracker.latest_message.get("text", "")

        prompt = (
            "You are FinSense AI 💼 — a smart, friendly, and practical financial assistant.\n"
            "Provide clear, actionable, and motivational answers in 3–5 sentences.\n"
            "Use emojis where appropriate to keep it fun and human-like.\n\n"
            f"User: {user_message}\n"
            "FinSense AI:"
        )

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 250
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                res = response.json()
                text = res["choices"][0]["message"]["content"].strip()
                dispatcher.utter_message(text=text)
            else:
                dispatcher.utter_message(
                    text=f"⚠️ API Error {response.status_code}: {response.text[:200]}"
                )

        except Exception as e:
            dispatcher.utter_message(text=f"❌ Error connecting to AI: {str(e)}")

        return []