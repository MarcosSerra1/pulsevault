# PulseVault 💰

O PulseVault é uma API RESTful para gerenciamento de finanças pessoais, permitindo controle de receitas, despesas e orçamentos de forma organizada e segura.

## 🚀 Tecnologias

- Python 3.12
- Django 5.1
- Django REST Framework
- PostgreSQL
- Docker e Docker Compose
- Nginx

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git
- Python 3.12+

## 🏗️ Estrutura do Projeto

```
pulsevault/
├── common/           # Modelos e utilitários compartilhados
│   ├── models.py     # Modelos base e específicos
│   ├── admin.py      # Configurações do admin
│   └── tests.py      # Testes unitários
├── core/            # Configurações do projeto
├── users/           # Gestão de usuários
├── api/             # Views e endpoints da API
├── scripts/         # Scripts úteis
└── docker/          # Configurações Docker
```

## 📦 Modelos

### BaseModel
- Campos compartilhados por todos os modelos
- Gestão por usuário
- Controle de ativo/inativo
- Timestamps automáticos

### Category
- Categorização de transações
- Tipos: Receita/Despesa
- Slug automático
- Unique por usuário+nome+tipo

### Bank
- Cadastro de bancos
- Código bancário único por usuário
- Normalização de nomes

### PaymentMethod
- Formas de pagamento
- Específico por usuário
- Gestão de status ativo

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pulsevault.git
cd pulsevault
```

2. Configure o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp env.example .env
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

## 🧪 Testes

Execute os testes unitários:
```bash
python manage.py test
```

Verificação de estilo:
```bash
flake8
```

## 🤝 Contribuindo

1. Faça um Fork
2. Crie sua Feature Branch:
```bash
git checkout -b feature/NomeFeature
```

3. Commits devem seguir Conventional Commits:
```bash
git commit -m "feat(escopo): descrição"
git commit -m "fix(escopo): descrição"
git commit -m "docs(escopo): descrição"
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
⌨️ com ❤️ por [Marcos Serra](https://github.com/MarcosSerra1)
