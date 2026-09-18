# cpfAPI

API bem simples que valida CPFs (o documento de identificação usado no Brasil). Você manda um CPF, ela te diz se é válido e devolve ele já formatado (`123.456.789-09`).

Serve, por exemplo, para plugar num formulário de cadastro e garantir que o CPF digitado pelo usuário é numericamente válido, sem precisar reescrever essa lógica em todo projeto novo.

## O que ela faz

- Recebe um CPF (com ou sem pontuação) e valida os dígitos verificadores.
- Formata o CPF no padrão `000.000.000-00`.
- Gera CPFs válidos aleatórios, úteis para testar formulários e telas de cadastro sem usar dados reais.

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado.

## Como rodar o projeto

1. Baixe o projeto e entre na pasta dele pelo terminal.

2. Crie um ambiente virtual (isola as bibliotecas do projeto do resto do seu computador):

   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:

   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

5. Suba a API:

   ```bash
   python -m uvicorn main:app --reload
   ```

6. Pronto! A API está rodando em `http://127.0.0.1:8000`.

## Como usar

A forma mais fácil de testar é abrir `http://127.0.0.1:8000/docs` no navegador: o FastAPI gera uma página interativa onde dá pra clicar e testar cada endpoint sem escrever código.

### Validar um CPF

`POST /cpf/validar`

Envie um CPF no corpo da requisição:

```json
{
  "cpf": "111.444.777-35"
}
```

Resposta:

```json
{
  "cpf_sem_formatacao": "111.444.777-35",
  "cpf_formatado": "111.444.777-35",
  "valido": true
}
```

### Gerar um CPF válido para testes

`GET /cpf/gerar`

Não precisa enviar nada. A resposta é um CPF válido gerado na hora:

```json
{
  "cpf_sem_formatacao": "11144477735",
  "cpf_formatado": "111.444.777-35",
  "valido": true
}
```

## Sobre o código

Toda a regra de validação e formatação de CPF mora na classe `CPF`, em `main.py`. As rotas da API só chamam essa classe — assim, se um dia esse projeto crescer, a lógica de CPF continua num lugar só.
