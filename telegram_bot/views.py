import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        message = data.get("message")
        if not message:
            return JsonResponse({"ok": True})

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text.startswith("/start"):
            parts = text.strip().split()
            if len(parts) == 2:
                token = parts[1]
                user = User.objects.filter(telegram_token=token).first()
                if user:
                    user.telegram_chat_id = chat_id
                    user.save()
            return JsonResponse({"ok": True, "message": "chat_id saved"})
        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False}, status=405)