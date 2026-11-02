
# Sistema de Gestão de Estoque

Sistema de gerenciamento de estoque desenvolvido em Python, com persistência de dados em SQLite.

O projeto tem como objetivo aplicar conceitos de programação orientada a objetos, manipulação de banco de dados, operações CRUD, transações SQL e testes automatizados.

## Funcionalidades

- Cadastro de produtos.
- Listagem de produtos cadastrados.
- Controle de entrada e saída de estoque.
- Consulta ao histórico de movimentações.
- Relatório gerencial de estoque.
- Cálculo do valor investido e da receita potencial.
- Identificação de produtos com estoque baixo.
- Validação de dados e prevenção de códigos duplicados.
- Transações SQL com rollback em caso de falhas.

## Tecnologias utilizadas

- Python
- SQLite
- SQL
- Pytest
- Git e GitHub

## Estrutura do projeto

```text
01-sistema-gestao-estoque/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
│   ├── test_product.py
│   └── test_repository.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── estoque.db
```

## Instalação e execução

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd 01-sistema-gestao-estoque
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o sistema:

```bash
python -m app.main
```

## Testes automatizados

Para executar os testes:

```bash
python -m pytest -v
```

## Aprendizados e conceitos aplicados

Durante o desenvolvimento foram aplicados conceitos de:

- Programação Orientada a Objetos.
- Validação e tratamento de exceções.
- Operações CRUD.
- Integração entre Python e SQLite.
- Consultas SQL e agregações.
- Transações e integridade de dados.
- Testes unitários e testes de repositório.

## Status do projeto

Em desenvolvimento.
