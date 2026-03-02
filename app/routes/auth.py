from datetime import timedelta
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.repositories.repository import UserRepository
from app.services.auth_service import verify_password, create_access_token
from app.schemas.schemas import UserCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await UserRepository.get_user_by_username(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuario o contraseña incorrectos"},
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "register": True}
    )


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
):
    existing_user = await UserRepository.get_user_by_username(username)
    if existing_user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "register": True, "error": "El usuario ya existe"},
        )

    existing_email = await UserRepository.get_user_by_email(email)
    if existing_email:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "register": True,
                "error": "El email ya está registrado",
            },
        )

    user_data = UserCreate(
        username=username, email=email, full_name=full_name, password=password
    )

    await UserRepository.create_user(user_data)

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "success": "Usuario creado exitosamente. Por favor inicia sesión.",
        },
    )
