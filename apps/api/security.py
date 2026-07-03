from ninja.security import HttpBearer
from ninja_jwt.tokens import AccessToken
from apps.models import User

class JWTAuth(HttpBearer):

    def authenticate(self, request, token):
        print("TOKEN:", token)

        try:
            access = AccessToken(token)
            print("PAYLOAD:", access.payload)

            user = User.objects.get(id=access["user_id"])
            print("USER:", user.username)

            return user

        except Exception as e:
            print("JWT ERROR:", e)
            return None