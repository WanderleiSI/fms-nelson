from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("cadastro", CadastroView.as_view(), name="cadastro"),
    path("validacao", csrf_exempt(ValidacaoUsuarioView.as_view()), name="validacao"),
    path(
        "valida_email", csrf_exempt(ValidacaoEmailView.as_view()), name="valida_email"
    ),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
