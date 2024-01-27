from django.forms import ModelForm
from .models import Categoria, Despesas, Ganho
from django import forms


class DespesasForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = ["descricao", "categoria", "valor", "data"]

        widgets = {
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesasForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            user=request.user
        )


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]


class GanhoForm(ModelForm):
    class Meta:
        model = Ganho
        fields = "__all__"
