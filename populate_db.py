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
        {'nome': 'Lasagna alla Bolognese', 'descricao': 'Massa em camadas com ragu de carne, molho bechamel e parmesão', 'preco': 46.90},
        {'nome': 'Risotto ai Funghi', 'descricao': 'Arroz arbório cremoso com cogumelos porcini e parmesão', 'preco': 42.50},
        {'nome': 'Gnocchi al Pesto', 'descricao': 'Nhoque de batata com molho pesto de manjericão e nozes', 'preco': 39.00},
        {'nome': 'Spaghetti Carbonara', 'descricao': 'Espaguete com molho de ovos, queijo pecorino, pancetta e pimenta preta', 'preco': 44.75},
        {'nome': 'Fettuccine Alfredo', 'descricao': 'Massa fettuccine com creme de leite, manteiga e parmesão', 'preco': 40.00},
        {'nome': 'Polenta con Funghi', 'descricao': 'Polenta cremosa servida com cogumelos salteados e azeite trufado', 'preco': 36.80},
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
    pedido1.itens.set(Prato.objects.filter(id__in=[1, 2])) 
    pedido1.calcular_total()
    
    # Pedido para cliente2
    cliente2 = User.objects.get(username='cliente2')
    pedido2 = Pedido.objects.create(usuario=cliente2)
    pedido2.itens.set(Prato.objects.filter(id__in=[3, 5]))  
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