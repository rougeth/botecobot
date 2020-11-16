# 🍻 botecobot
O Garçom da Python Brasil 2020

[![badge](https://img.shields.io/static/v1?label=Discord&message=Add%20to%20Server&color=blueviolet&logo=discord)](https://discord.com/api/oauth2/authorize?client_id=773865304479629323&permissions=3152&scope=bot)

#### Como usar?

O botecobot é simple e contém apenas os dois comandos abaixo:

- `!boteco build`: Criar a categoria *#boteco* e o canal de texto *#peca-uma-mesa*. Esse comando precisa ser executado apenas uma vez para que o bot comece a funcionar.
- `!mesa <nome da mesa>`: A partir de qualquer canal que o bot tenha acesso, o comando `!mesa <nome da mesa>` criará um novo canal de voz dentro da categoria *#boteco*.

O **botecobot** removerá qualquer mesa (canal de voz no *#boteco*) que ficar vazia por mais de 5 minutos.

### Instalando e rodando localmente

```
$ cp local.env .env
# Atualize o arquivo .env com as informações necessárias.
$ pipenv install
$ pipenv run python boteco.py
```
