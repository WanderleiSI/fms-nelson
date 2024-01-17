from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="main"),
    path("minhas_despesas", views.minhas_despesas, name="minhas_despesas"),
    path("criar_despesa", views.CreateDespesaView.as_view(), name="criar_despesa"),
    path("editar_despesa/<int:id>", views.edit_despesa, name="editar_despesa"),
    path("delete_despesa/<int:id>", views.remove_despesa, name="delete_despesa"),
    path("listagem_categorias", views.listar_categoria, name="listagem_categorias"),
    path("add_categoria", views.add_categoria, name="add_categoria"),
    path("delete_categoria/<int:id>", views.remove_categoria, name="delete_categoria"),
    path("listagem_renda", views.listagem_ganhos, name="listagem_renda"),
    path("add_renda", views.add_renda, name="add_renda"),
    path("editar_renda/<int:id>", views.editar_renda, name="editar_renda"),
    path("delete_renda/<int:id>", views.remove_renda, name="delete_renda"),
    path("graph/", views.view_graph, name="graph"),  # gráfico por categoria de despesa
    path("graph2/", views.view_graph2, name="graph2"),  # gráfico de renda por mês
    path("graph3/", views.view_graph3, name="graph3"),  # gráfico de renda por ano
    path("exportar_excel", views.exportar_excel, name="exportar_excel"),
    path("estatistica", views.exibe_graph, name="estatistica"),
    path("estatistica_renda", views.exibe_graph2, name="estatistica_renda"),
    path(
        "graph_despesas_mensal",
        views.graph_despesas_mensal,
        name="graph_despesas_mensal",
    ),
    path(
        "graph_despesas_anual", views.graph_despesas_anual, name="graph_despesas_anual"
    ),
]