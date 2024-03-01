from django.conf import settings

class LanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        code = request.session.get("lan_mode", "chi")
        lan_code = {"chi": 0, "en": 1, "jp": 2}
        settings.TRANS_DICT = {k: v[lan_code[code]] for k, v in settings.TRANS_REPO.items()}

        response = self.get_response(request)

        return response