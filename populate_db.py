#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

# Configuração inicial do Django
def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_api.settings')
    django.setup()
    print("✅ Configuração do Django concluída!")

def criar_usuarios():
    from django.contrib.auth.models import User
    
    users = [
        # Superuser
        {'username': 'admin_master', 'email': 'admin@restaurante.com', 'password': 'senha123', 'is_superuser': True, 'is_staff': True},
        # Staff
        {'username': 'gerente', 'password': 'senha123', 'is_staff': True},
        # Usuários comuns
        {'username': 'cliente1', 'password': 'senha123'},
        {'username': 'cliente2', 'password': 'senha123'}
    ]
    
    for user_data in users:
        if user_data.get('is_superuser'):
            User.objects.create_superuser(**user_data)
        else:
            User.objects.create_user(**user_data)
    
    print(f"✅ {len(users)} usuários criados!")

def criar_pratos():
    from restaurante.models import Prato
    
    cardapio = [
        {'nome': 'Pizza Margherita', 'descricao': 'Molho de tomate, mussarela e manjericão', 'preco': 45.90},
        {'nome': 'Hambúrguer Artesanal', 'descricao': 'Pão brioche, carne 180g e queijo cheddar', 'preco': 32.50},
        {'nome': 'Salada Caesar', 'descricao': 'Alface romana, croutons e molho caesar', 'preco': 28.75},
        {'nome': 'Sushi Sashimi', 'descricao': '10 peças de sashimi variado', 'preco': 59.90},
        {'nome': 'Água Mineral', 'descricao': '500ml sem gás', 'preco': 5.00}
    ]
    
    for item in cardapio:
        Prato.objects.create(**item)
    
    print(f"✅ {len(cardapio)} pratos criados!")

def criar_pedidos():
    from django.contrib.auth.models import User
    from restaurante.models import Pedido, Prato
    
    # Pedido para cliente1
    cliente1 = User.objects.get(username='cliente1')
    pedido1 = Pedido.objects.create(usuario=cliente1)
    pedido1.itens.set(Prato.objects.filter(id__in=[1, 2]))  # Pizza + Hambúrguer
    pedido1.calcular_total()
    
    # Pedido para cliente2
    cliente2 = User.objects.get(username='cliente2')
    pedido2 = Pedido.objects.create(usuario=cliente2)
    pedido2.itens.set(Prato.objects.filter(id__in=[3, 5]))  # Salada + Água
    pedido2.calcular_total()
    
    print("✅ 2 pedidos criados!")

def main():
    print("\n=== POPULANDO BANCO DE DADOS ===")
    try:
        setup_django()
        criar_usuarios()
        criar_pratos()
        criar_pedidos()
        print("\n🎉 População concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {str(e)}")

if __name__ == '__main__':
    main()