from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
import json

class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        response = kwargs.get('response', None)

        # Google 응답 출력
        print("Google Response:", response)

        # 응답이 문자열인 경우 JSON으로 변환
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", e)
                raise ValueError("Invalid JSON response from Google")

        return super().complete_login(request, app, token, response=response)
