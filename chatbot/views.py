import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from .chatbot import chatbot_reply  # import chatbot_reply function from chatbot.py

# Optional: Just to check if template DIR is correct
print(settings.TEMPLATES[0]['DIRS'])

# View to render the chatbot HTML
def index(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
def get_bot_response(request):
    if request.method == "POST":
        print("[DEBUG] Received POST request")
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input') or data.get('message', '')
            user_input = user_input.strip()


            if user_input:
                print(f"[DEBUG] Normalized input: '{user_input}'")
                bot_raw = chatbot_reply(user_input)

                # 🧠 If bot_raw is a list of dicts (like HuggingFace pipeline), get the first 'generated_text'
                if isinstance(bot_raw, list) and 'generated_text' in bot_raw[0]:
                    bot_response = bot_raw[0]['generated_text']
                else:
                    bot_response = str(bot_raw)

                print(f"[DEBUG] Bot Reply: {bot_response}")
                return JsonResponse({"response": bot_response})
            else:
                return JsonResponse({"response": "Please enter a message."})
        except Exception as e:
            print(f"[ERROR] {e}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed."}, status=405)
