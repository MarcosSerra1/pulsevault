# PulseVault 💰

O PulseVault é uma API RESTful para gerenciamento de finanças pessoais, permitindo controle de receitas, despesas e orçamentos de forma organizada e segura.

## 🚀 Tecnologias

- Python 3.12
- Django 5.1
- Django REST Framework
- PostgreSQL
- Docker e Docker Compose
- Nginx
- Argon2 para hash de senhas
- JWT para autenticação

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git
- Python 3.12+

## 🏗️ Estrutura do Projeto

```
pulsevault/
├── users/           # Gestão de usuários
│   ├── models.py     # Modelo CustomUser
│   ├── validators.py # Validadores de senha
│   ├── serializers.py# Serializers REST
│   ├── views.py     # Views da API
│   ├── middleware.py# Middleware de auditoria
│   └── tests/       # Testes unitários
├── common/          # Modelos compartilhados
├── transactions/    # Gestão financeira
├── core/           # Configurações do projeto
└── scripts/        # Scripts úteis
```

## 📦 Modelos Principais

### CustomUser
- UUID como identificador primário
- Email como login
- Validação forte de senha
- Histórico de senhas anteriores
- Auditoria de ações

### Validadores de Senha
- Mínimo 8 caracteres
- Letras maiúsculas e minúsculas
- Números e caracteres especiais
- Prevenção de partes do email/nome
- Histórico de senhas anteriores

### Segurança
- Rate limiting para criação/login
- Argon2 para hash de senhas
- JWT para autenticação
- Middleware de auditoria
- Logs estruturados

## 🔒 Endpoints de Usuário

```
POST /api/v1/users/register/    # Criação de usuário
GET  /api/v1/users/list/        # Listagem de usuários
GET  /api/v1/users/<uuid>/      # Detalhes do usuário
PUT  /api/v1/users/<uuid>/      # Atualização de usuário
DEL  /api/v1/users/<uuid>/      # Remoção de usuário
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pulsevault.git
cd pulsevault
```

2. Configure o ambiente:
```bash
cp env.example .env
# Configure as variáveis no .env
```

3. Execute com Docker:
```bash
docker compose up -d
```

## 🧪 Testes

Execute os testes:
```bash
# Todos os testes
python manage.py test

# Apenas testes de usuários
python manage.py test users.tests
```

Verificação de estilo:
```bash
flake8
```

## 📊 Monitoramento

Logs disponíveis:
- `debug.log`: Logs gerais do sistema
- `audit.log`: Auditoria de ações dos usuários

## 🤝 Contribuindo

1. Faça um Fork
2. Crie sua Feature Branch:
```bash
git checkout -b feature/NomeFeature
```

3. Commits devem seguir Conventional Commits:
```bash
git commit -m "feat(users): adiciona validação de senha"
git commit -m "fix(auth): corrige rate limiting"
git commit -m "docs(api): atualiza documentação"
```

4. Push para sua branch:
```bash
git push origin feature/NomeFeature
```

5. Abra um Pull Request

## 📝 Licença

Projeto sob licença MIT. Veja [LICENSE](LICENSE) para detalhes.

## ✨ Autor

* **Marcos Serra** - [GitHub](https://github.com/MarcosSerra1)

---
⌨️ por [Marcos Serra](https://github.com/MarcosSerra1)
