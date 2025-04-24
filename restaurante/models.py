from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Prato(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Prato")
    descricao = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    preco = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Preço",
        validators=[MinValueValidator(0.01, "O preço deve ser maior que zero.")]
    )

    class Meta:
        verbose_name = "Prato"
        verbose_name_plural = "Pratos"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def clean(self):
        if self.preco and self.preco <= 0:
            raise models.ValidationError(
                {'preco': "O preço deve ser maior que zero."}
            )


class Pedido(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_PREPARANDO = 'preparando'
    STATUS_ENTREGUE = 'entregue'
    STATUS_CANCELADO = 'cancelado'

    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_PREPARANDO, 'Preparando'),
        (STATUS_ENTREGUE, 'Entregue'),
        (STATUS_CANCELADO, 'Cancelado')
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    itens = models.ManyToManyField(
        Prato,
        related_name='pedidos',
        verbose_name="Itens do Pedido"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name="Total do Pedido"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE,
        verbose_name="Status do Pedido"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    modificado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Modificado em"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

    def calcular_total(self):
        """Calcula o total do pedido somando os preços de todos os itens"""
        total = sum([prato.preco for prato in self.itens.all()])
        self.total = total
        self.save()

    def clean(self):
        """Validações adicionais para o modelo Pedido"""
        if self.total and self.total < 0:
            raise models.ValidationError(
                {'total': "O total não pode ser negativo."}
            )