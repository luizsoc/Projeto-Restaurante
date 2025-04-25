from rest_framework import viewsets, filters, status  
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Prato, Pedido
from .serializers import PratoSerializer, PedidoSerializer
from .permissions import IsOwnerOrAdmin

class PratoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite gerenciar pratos do cardápio.
    
    Permissões:
    - Listagem: qualquer usuário autenticado
    - Criação/Edição: apenas administradores
    """
    queryset = Prato.objects.all().order_by('nome')
    serializer_class = PratoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'preco']
    filterset_fields = ['preco']

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que esta view requer.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], url_path='mais-vendidos')
    def mais_vendidos(self, request):
        """
        Retorna os pratos mais vendidos (ordenados por quantidade de pedidos)
        """
        pratos = Prato.objects.annotate(
            num_pedidos=Count('pedidos')
        ).order_by('-num_pedidos')[:5]
        serializer = self.get_serializer(pratos, many=True)
        return Response(serializer.data)


class PedidoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite gerenciar pedidos dos usuários.
    
    Permissões:
    - Usuários normais só podem ver/editar seus próprios pedidos
    - Administradores têm acesso completo
    """
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'usuario']
    ordering_fields = ['criado_em', 'total']
    search_fields = ['usuario__username']

    def get_queryset(self):
        """
        Retorna apenas os pedidos do usuário atual, exceto para administradores
        """
        queryset = Pedido.objects.all().select_related('usuario').prefetch_related('itens')
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(usuario=self.request.user)
            
        return queryset.order_by('-criado_em')

    def perform_create(self, serializer):
        """
        Cria um novo pedido associando automaticamente o usuário atual
        e calculando o total
        """
        print(self.request.user)
        pedido = serializer.save(usuario=self.request.user)
        pedido.calcular_total()

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar_pedido(self, request, pk=None):
        """
        Ação customizada para cancelar um pedido
        """
        pedido = self.get_object()
        
        if pedido.status == Pedido.STATUS_CANCELADO:
            return Response(
                {'detail': 'Este pedido já está cancelado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if pedido.status == Pedido.STATUS_ENTREGUE:
            return Response(
                {'detail': 'Pedidos já entregues não podem ser cancelados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        pedido.status = Pedido.STATUS_CANCELADO
        pedido.save()
        serializer = self.get_serializer(pedido)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='meus-pedidos')
    def meus_pedidos(self, request):
        """
        Endpoint alternativo para listar apenas os pedidos do usuário atual
        (mesmo comportamento do get_queryset, mas com URL dedicada)
        """
        queryset = self.filter_queryset(self.get_queryset().filter(usuario=request.user))
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)