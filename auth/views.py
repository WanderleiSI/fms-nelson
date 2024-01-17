from ast import Expression
from base64 import urlsafe_b64decode
from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages, auth

# from django.utils.encoding import force_text
# Create your views here.


class CadastroView(View):
    def get(self, request):
        return render(request, "auth/cadastro.html")

    def post(self, request):
        # Pegar os dados do usuário, validar e criar conta
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        # mantém os campos preenchidos antes da senha, para o caso de ser muito curta e disparar o alerta.
        context = {"fieldVal": request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(
                        request, "A senha deve possuir no mínimo 6 caracteres"
                    )
                    return render(request, "auth/cadastro.html", context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Usuário cadastrado com sucesso!")
                return render(request, "auth/cadastro.html")

        return render(request, "auth/cadastro.html")


class ValidacaoUsuarioView(View):
    def post(self, request):
        data = json.loads(request.body)  # pega os dados e transforma em dicionario json
        username = data["username"]  # pega o nome de usuário do dicionário
        # checa se o nome de usuário contém algum caractere especial
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "error": "O nome de usuário não pode conter caracteres especiais. Ex: (@,#,!... etc)"
                },
                status=400,
            )
        # checa se o usuário existe no banco de dados
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    "error": "O nome de usuário inserido já existe. Por favor escolha outro."
                },
                status=409,
            )
        # else
        return JsonResponse({"user_valido": True})


class ValidacaoEmailView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {
                    "error_email": "Insira um formato de email válido. Ex: username@email.com"
                },
                status=400,
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"error_email": "O email inserido já existe. Por favor escolha outro."},
                status=409,
            )
        # else
        return JsonResponse({"email_valido": True})


class VerificacaoView(View):
    def get(self, request):
        user = User.objects.get(pk=id)
        if user.is_active:
            return redirect("login")
        user.is_active = True
        user.save()

        messages.success(request, "Conta ativiada com sucesso")
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Bem-vindo(a), " + user.username)

                    return redirect("main")

                messages.error(request, "Conta inativa!")
                return render(request, "auth/login.html")

            messages.error(
                request, "Nome de usuário ou senha incorreta, por favor tente novamente"
            )
            return render(request, "auth/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "Você saiu da sua conta")
        return redirect("login")
