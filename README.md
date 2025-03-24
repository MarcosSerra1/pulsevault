# PulseVault 💰

O PulseVault é uma API RESTful para gerenciamento de finanças pessoais.

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

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/pulsevault.git
cd pulsevault
```

2. Configure as variáveis de ambiente:
```bash
cp env.example .env
```

3. Inicie os containers:
```bash
docker compose up -d
```

4. Acesse:
- API: http://localhost
- Admin: http://localhost/admin

## 🔧 Desenvolvimento

Para executar os testes:
```bash
docker compose exec web python manage.py test
```

Para verificar o código com Flake8:
```bash
docker compose exec web flake8
```

## 📦 Estrutura do Projeto

```
pulsevault/
├── core/              # Configurações do projeto
├── api/               # Aplicação principal
├── scripts/          # Scripts úteis
├── tests/            # Testes
└── docker/           # Arquivos Docker
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'feat: add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Autor

* **Marcos Serra** - [GitHub](https://github.com/seu-usuario)

---
⌨️ [Marcos Serra](https://github.com/seu-usuario)
