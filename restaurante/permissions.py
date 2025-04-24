from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas:
    - O dono do objeto (pedido) ou
    - Um administrador
    possa acessar ou editar o objeto.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer requisição,
        # então sempre permitimos GET, HEAD ou OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Permissões de escrita apenas para o dono do pedido ou admin
        return obj.usuario == request.user or request.user.is_staff