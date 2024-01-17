import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import CategoriaForm, DespesasForm, GanhoForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum
import xlwt
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator

# Create your views here.
@login_required(login_url="/auth/login")
def index(request):
    despesas = Despesas.objects.filter(user=request.user)
    ganhos = Ganho.objects.filter(user=request.user)
    total_despesas = 0
    total_ganhos = 0
    saldo = 0

    for despesa in despesas:
        total_despesas += despesa.valor
    for ganho in ganhos:
        total_ganhos += ganho.valor

    saldo = total_ganhos - total_despesas

    context = {
        "despesas": despesas,
        "ganhos": ganhos,
        "total_despesas": total_despesas,
        "total_ganhos": total_ganhos,
        "saldo": saldo,
    }
    return render(request, "despesas/index.html", context)

@method_decorator(login_required, name="dispatch")
class CreateDespesaView(CreateView):
    model = Despesas
    form_class = DespesasForm
    template_name = "despesas/criar_despesa.html"

    def get_form_kwargs(self):
        kwargs = super(CreateDespesaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("minhas_despesas")


@login_required(login_url="/auth/login")
def minhas_despesas(request):
    despesas = Despesas.objects.filter(user=request.user)
    ganhos = Ganho.objects.filter(user=request.user)
    total_despesas = 0
    total_ganhos = 0
    saldo = 0

    for despesa in despesas:
        total_despesas += despesa.valor
    for ganho in ganhos:
        total_ganhos += ganho.valor

    saldo = total_ganhos - total_despesas
    paginator = Paginator(despesas, 5)
    pagina_num = request.GET.get("page")
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    context = {
        "despesas": despesas,
        "ganhos": ganhos,
        "total_despesas": total_despesas,
        "total_ganhos": total_ganhos,
        "saldo": saldo,
        "obj_pagina": obj_pagina,
    }
    return render(request, "despesas/minhas_despesas.html", context)


@login_required(login_url="/auth/login")
def edit_despesa(request, id):
    despesa = Despesas.objects.get(pk=id)
    categorias = Categoria.objects.filter(user=request.user)
    context = {
        "despesa": despesa,
        "val": despesa,
        "categorias": categorias,
    }
    if request.method == "GET":
        return render(request, "despesas/editar_despesa.html", context)
    if request.method == "POST":
        descricao = request.POST["descricao"]
        categoria = request.POST["categoria"]
        valor = request.POST["valor"]
        data = request.POST["data"]

        despesa.user = request.user
        despesa.descricao = descricao
        despesa.categoria = Categoria.objects.get(nome=categoria)
        despesa.valor = valor
        despesa.data = data
        despesa.save()
        messages.success(request, "Despesa atualizada com sucesso!")

        return redirect("minhas_despesas")


@login_required(login_url="/auth/login")
def remove_despesa(request, id):
    despesa = Despesas.objects.get(pk=id)
    despesa.delete()
    messages.success(request, "Despesa removida com sucesso!")

    return redirect("minhas_despesas")


@login_required(login_url="/auth/login")
def listar_categoria(request):
    categorias = Categoria.objects.filter(user=request.user)
    paginator = Paginator(categorias, 10)
    pagina_num = request.GET.get("page")
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    context = {"categorias": categorias, "obj_pagina": obj_pagina}
    return render(request, "despesas/listagem_categorias.html", context)


@login_required(login_url="/auth/login")
def add_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = request.user
            categoria.save()

            messages.success(request, "Categoria criada com sucesso!")
            return redirect("listagem_categorias")
        return render(request, "despesas/add_categoria.html", {"form": form})
    form = CategoriaForm()
    return render(request, "despesas/add_categoria.html", {"form": form})


@login_required(login_url="/auth/login")
def remove_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    try:
        categoria.delete()
    except:
        pass
    return redirect("listagem_categorias")


@login_required(login_url="/auth/login")
def listagem_ganhos(request):
    rendas = Ganho.objects.filter(user=request.user)
    paginator = Paginator(rendas, 5)
    pagina_num = request.GET.get("page")
    obj_pagina = Paginator.get_page(paginator, pagina_num)
    rendas = Ganho.objects.filter(user=request.user)
    total_ganho = 0

    for renda in rendas:
        total_ganho += renda.valor

    context = {
        "rendas": rendas,
        "obj_pagina": obj_pagina,
        "rendas": rendas,
        "total_ganho": total_ganho,
    }
    return render(request, "rendas/listagem_renda.html", context)


@login_required(login_url="/auth/login")
def add_renda(request):
    if request.method == "POST":
        form = GanhoForm(request.POST)
        if form.is_valid():
            renda = form.save(commit=False)
            renda.user = request.user
            renda.save()

            messages.success(request, "Renda lançada com sucesso!")
            return redirect("listagem_renda")
        return render(request, "rendas/add_renda.html", {"form": form})
    form = GanhoForm()
    return render(request, "rendas/add_renda.html", {"form": form})


@login_required(login_url="/auth/login")
def editar_renda(request, id):
    renda = Ganho.objects.get(id=id)
    form = GanhoForm(
        initial={
            "descricao": renda.descricao,
            "valor": renda.valor,
            "data": renda.data,
        }
    )
    if request.method == "POST":
        form = GanhoForm(request.POST, instance=renda)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                messages.success(request, "Renda atualizada com sucesso!")
                return redirect("listagem_renda")
            except Exception as e:
                pass
    return render(request, "rendas/editar_renda.html", {"form": form})


@login_required(login_url="/auth/login")
def remove_renda(request, id):
    renda = Ganho.objects.get(pk=id)
    renda.delete()
    messages.success(request, "Renda removida com sucesso!")

    return redirect("listagem_renda")


# Gera gráfico de gastos por categoria
@login_required(login_url="/auth/login")
def view_graph(request):
    labels = []
    data = []

    queryset = (
        Despesas.objects.values("categoria__nome")
        .annotate(categoria_valor=Sum("valor"))
        .order_by("-categoria_valor")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["categoria__nome"])
        data.append(entry["categoria_valor"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


# Gera gráfico de renda por mês
@login_required(login_url="/auth/login")
def view_graph2(request):
    labels = []
    data = []

    queryset = (
        Ganho.objects.values("data__month")
        .annotate(ganho_valor=Sum("valor"))
        .order_by("data__month")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__month"])
        data.append(entry["ganho_valor"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


# Gera gráfico de renda por ano
@login_required(login_url="/auth/login")
def view_graph3(request):
    labels = []
    data = []

    queryset = (
        Ganho.objects.values("data__year")
        .annotate(ganho_valor=Sum("valor"))
        .order_by("data__year")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__year"])
        data.append(entry["ganho_valor"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@login_required(login_url="/auth/login")
def graph_despesas_mensal(request):
    labels = []
    data = []

    queryset = (
        Despesas.objects.values("data__month")
        .annotate(ganho_valor=Sum("valor"))
        .order_by("data__month")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__month"])
        data.append(entry["ganho_valor"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


@login_required(login_url="/auth/login")
def graph_despesas_anual(request):
    labels = []
    data = []

    queryset = (
        Despesas.objects.values("data__year")
        .annotate(ganho_valor=Sum("valor"))
        .order_by("data__year")
        .filter(user=request.user)
    )
    for entry in queryset:
        labels.append(entry["data__year"])
        data.append(entry["ganho_valor"])

    return JsonResponse(
        data={
            "labels": labels,
            "data": data,
        }
    )


# View gráficos de despesas
@login_required(login_url="/auth/login")
def exibe_graph(request):
    despesas = Despesas.objects.filter(user=request.user)
    total_despesas = 0

    for despesa in despesas:
        total_despesas += despesa.valor

    context = {"despesas": despesas, "total_despesas": total_despesas}
    return render(request, "despesas/estatistica.html", context)


# View gráficos de renda
@login_required(login_url="/auth/login")
def exibe_graph2(request):
    rendas = Ganho.objects.filter(user=request.user)
    total_ganho = 0

    for renda in rendas:
        total_ganho += renda.valor

    context = {"rendas": rendas, "total_ganho": total_ganho}
    return render(request, "rendas/estatistica_renda.html", context)


def exportar_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=Despesas" + str(datetime.datetime.now()) + ".xls"
    )
    wb = xlwt.Workbook(encoding="UTF-8")
    ws = wb.add_sheet("Despesas")
    row_num = 0
    sum = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    cols = ["Descrição", "Categoria", "Valor", "Data"]

    for col_num in range(len(cols)):
        ws.write(row_num, col_num, cols[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Despesas.objects.filter(user=request.user).values_list(
        "descricao", "categoria__nome", "valor", "data"
    )
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response
