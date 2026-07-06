from ninja import Router
from django.contrib.auth.hashers import make_password
from django.http import Http404
from apps.models import User
from .schemas import RegisterSchema, UserOut, RefreshSchema, AccessTokenOut, TokenOut, LoginSchema, UpdateProfileSchema
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken, TokenError
from .security import JWTAuth
from apps.mongodb.logger import log_activity

router = Router(tags=["Authentication"])

@router.post("/register", response={201: UserOut, 400: dict})
def register(request, data: RegisterSchema):

    if User.objects.filter(username=data.username).exists():
        return 400, {
            "message": "Username sudah digunakan."
        }

    if User.objects.filter(email=data.email).exists():
        return 400, {
            "message": "Email sudah digunakan."
        }

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password
    )
    log_activity(
        user=user,
        action="REGISTER",
        detail={}
    )

    return 201, user

@router.post("/login", response=TokenOut)
def login(request, data: LoginSchema):

    user = authenticate(
        username=data.username,
        password=data.password
    )

    if user is None:
        raise HttpError(
            401,
            "Username atau password salah."
        )

    refresh = RefreshToken.for_user(user)

    log_activity(
        user=user,
        action="LOGIN",
        detail={}
    )

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

@router.post("/refresh", response={200: AccessTokenOut, 401: dict})
def refresh_token(request, data: RefreshSchema):

    try:
        refresh = RefreshToken(data.refresh)

        return {
            "access": str(refresh.access_token)
        }

    except TokenError:
        return 401, {
            "message": "Refresh token tidak valid."
        }
    
@router.get("/me", auth=JWTAuth(), response=UserOut)
def me(request):
    return request.auth

@router.put("/me", auth=JWTAuth(), response=UserOut)
def update_profile(request, data: UpdateProfileSchema):

    user = request.auth

    user.username = data.username
    user.email = data.email
    user.save()

    return user

print("AUTH ROUTER LOADED")