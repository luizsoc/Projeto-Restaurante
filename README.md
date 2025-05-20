# API Restaurante

Sistema de gerenciamento de cardápio e pedidos para restaurantes utilizando Django REST Framework.

## 📋 Sobre o projeto

Esta API permite gerenciar o cardápio de um restaurante e os pedidos dos clientes. O sistema conta com:

- Cadastro e gerenciamento de pratos do cardápio
- Criação e acompanhamento de pedidos
- Sistema de autenticação de usuários
- Documentação automática da API

## 🛠️ Tecnologias utilizadas

- Python 3.x
- Django
- Django REST Framework
- Django Filter
- drf-yasg (Swagger/ReDoc)
- Simple JWT para autenticação

## ⚙️ Estrutura do projeto

O sistema é composto pelos seguintes modelos principais:

- **Prato**: representa os itens do cardápio
- **Pedido**: representa os pedidos realizados pelos clientes

## 🔧 Instalação

### Pré-requisitos

- Python 3.x
- pip
- virtualenv (recomendado)

### Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/restaurante-api.git
   cd restaurante-api
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # ou
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

6. Popule o banco de dados com dados iniciais (opcional):
   ```bash
   python populate_db.py
   ```

7. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## 🚀 Endpoints da API

### Autenticação

- `POST /api/token/`: Obter token JWT
- `POST /api/token/refresh/`: Renovar token JWT

### Pratos

- `GET /api/v1/pratos/`: Listar todos os pratos
- `POST /api/v1/pratos/`: Adicionar novo prato (apenas admin)
- `GET /api/v1/pratos/{id}/`: Detalhes de um prato específico
- `PUT/PATCH /api/v1/pratos/{id}/`: Atualizar prato (apenas admin)
- `DELETE /api/v1/pratos/{id}/`: Remover prato (apenas admin)
- `GET /api/v1/pratos/mais-vendidos/`: Listar os 5 pratos mais vendidos

### Pedidos

- `GET /api/v1/pedidos/`: Listar pedidos (usuários normais veem apenas seus próprios pedidos)
- `POST /api/v1/pedidos/`: Criar novo pedido
- `GET /api/v1/pedidos/{id}/`: Detalhes de um pedido específico
- `PUT/PATCH /api/v1/pedidos/{id}/`: Atualizar pedido
- `DELETE /api/v1/pedidos/{id}/`: Remover pedido
- `POST /api/v1/pedidos/{id}/cancelar/`: Cancelar pedido
- `GET /api/v1/pedidos/meus-pedidos/`: Listar apenas os pedidos do usuário atual

## 📊 Filtros e ordenação

### Pratos
- **Filtrar**: `?preco=XX.XX`
- **Buscar**: `?search=termo` (busca em nome e descrição)
- **Ordenar**: `?ordering=nome` ou `?ordering=-preco` (preço decrescente)

### Pedidos
- **Filtrar**: `?status=pendente` ou `?usuario=1`
- **Buscar**: `?search=username` (busca por nome de usuário)
- **Ordenar**: `?ordering=-criado_em` (mais recentes primeiro) ou `?ordering=total`

## 📘 Documentação

A API conta com documentação automática através do Swagger e ReDoc:

- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## 🔐 Permissões

- Usuários anônimos: Não têm acesso à API
- Usuários autenticados: Podem visualizar o cardápio e gerenciar seus próprios pedidos
- Administradores: Acesso completo a todas as funcionalidades

## 🧪 Dados de teste

O script `populate_db.py` cria:
- 2 usuários: `cliente1` e `cliente2` (senha: `senha123` para ambos)
- 6 pratos variados no cardápio
- 2 pedidos iniciais para demonstração

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
