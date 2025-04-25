from rest_framework import serializers
from .models import Prato, Pedido
from django.contrib.auth.models import User

class PratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'
        extra_kwargs = {
            'preco': {'min_value': 0.01}
        }

    def validate_nome(self, value):
        """Valida se o nome do prato não está vazio"""
        if not value.strip():
            raise serializers.ValidationError("O nome do prato não pode estar vazio.")
        return value

    def validate_preco(self, value):
        """Garante que o preço seja positivo"""
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'username', 'email']


class PedidoSerializer(serializers.ModelSerializer):
    itens = serializers.PrimaryKeyRelatedField(
        queryset=Prato.objects.all(),
        many=True,
        required=True
    )
    usuario = UserSerializer(read_only=True)
    usuario_id = serializers.PrimaryKeyRelatedField(
        source='usuario',
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    total_itens = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            'id',
            'usuario',
            'usuario_id',
            'itens',
            'total',
            'status',
            'status_display',
            'criado_em',
            'modificado_em',
            'total_itens'
        ]
        read_only_fields = ['total', 'criado_em', 'modificado_em']
        extra_kwargs = {
            'status': {'help_text': 'Status do pedido: pendente, preparando, entregue ou cancelado'}
        }

    def get_total_itens(self, obj):
        """Retorna a quantidade total de itens no pedido"""
        return obj.itens.count()

    def validate_itens(self, value):
        """Valida se há pelo menos um item no pedido"""
        if not value:
            raise serializers.ValidationError("O pedido deve conter pelo menos um prato.")
        return value

    def validate_status(self, value):
        """Valida se o status é um dos valores permitidos"""
        status_validos = [choice[0] for choice in Pedido.STATUS_CHOICES]
        if value not in status_validos:
            raise serializers.ValidationError(
                f"Status inválido. Opções válidas: {', '.join(status_validos)}."
            )
        return value

    def validate(self, data):
        """Validações em nível de objeto"""
        request = self.context.get('request')

        # Só valida permissões se estiver atualizando um objeto existente
        if self.instance:
            if self.instance.usuario != request.user and not request.user.is_staff:
                raise serializers.ValidationError(
                    "Você não tem permissão para modificar este pedido."
                )

        return data

    def create(self, validated_data):
        """Cria um novo pedido garantindo que o usuário correto seja associado"""
        request = self.context.get('request')
        if request:
            validated_data['usuario'] = request.user

        # Remove usuario_id se existir (usado apenas para escrita)
        validated_data.pop('usuario_id', None)

        pedido = super().create(validated_data)
        pedido.calcular_total()
        return pedido
