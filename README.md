<h1 align="center">
<p align="center">Análise de Transações Financeiras</p>
<img height=120 src="https://user-images.githubusercontent.com/71675056/168167122-54b0216f-8b87-4672-b201-5ae8be07afba.svg">
</h1>

<div align="center">
<img src="https://img.shields.io/badge/Python-3.9-success?style=for-the-badge">
<img src="https://img.shields.io/badge/Django-4.0-informational?style=for-the-badge">
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-brightgreen?style=for-the-badge">
</div>

<h3>
  <p align="center">Alura Challenge | Desafio Back-End 3ª Edição</p>
</h3>

Projeto desenvolvido como parte da 3ª edição de desafios Back-End da Alura, ao longo dos meses de abril e maio/2022

Realizei a construção de uma aplicação web completa com suporte para upload de arquivos, controle de acesso de usuários e análise de dados.

A lógica da aplicação se baseia na análise de transações importadas por usuários cadastrados em arquivos CSV ou XML, visando detectar operações suspeitas seguindo as regras de negócio definidas pelo desafio.

## Funcionalidades

 - `Controle de Acesso:` CRUD de usuários com funcionalidades de Login, Logout, Cadastro e Exclusão de contas de usuário
 - `Upload de arquivos:` Suporte para arquivos CSV ou XML contendo dados de transações financeiras
 - `Armazenamento em banco de dados:` Persistência em Banco de Dados SQL
 - `Transações Suspeitas:` Análise das transações importadas em busca de operações consideradas suspeitas

## Como funciona?

- `Login:` Somente usuários logados podem acessar o sistema, fazer upload de arquivos e gerar análises.
- `Cadastro:` Apenas usuários existentes podem cadastrar novos usuários, os quais receberão uma senha por e-mail para acessar a aplicação
- `Upload de arquivos:` Usuários logados podem enviar arquivos detalhando transações financeiras através da página inicial, e visualizar as importações já realizadas na aba "Importações"
- `Análise:` Pode ser realizada na aba "Transações Suspeitas", selecionando um mês para filtrar. São consideradas suspeitas:
  - Transações acima de R$100.000
  - Contas bancárias que enviarem ou receberem R$1.000.000 ou mais no mesmo mês
  - Agências bancárias que enviarem ou receberem R$1.000.000.000 ou mais no mesmo mês

## Ferramentas e Tecnologias utilizadas

 - `Python 3.9.7`
 - `Django 4.0.4`
 - `PostgreSQL 14.2`
 - `Bulma`
 - `Visual Studio Code`

## Aprendizados

Tive, através desse projeto, minha primeira experiência desenvolvendo uma aplicação web completa do começo ao fim, sem cursos ou professores para me guiar.

Confesso que as primeiras semanas do projeto foram levemente desesperadoras. Tinha uma boa base teórica sobre o framework, mas sendo minha primeira aplicação prática desses conhecimentos fiquei meio perdido em relação a como encontrar as informações necessárias para executar o que estava sendo pedido.

Mas foi justamente essa sensação que me motivou tanto para seguir em frente. Ouço muito na comunidade sobre como a rotina de um desenvolvedor envolve muito mais pesquisa e estudo do que escrever código de fato, e fiquei muito feliz de estar passando por essa experiência justamente por poder desenvolver essa habilidade tão importante.  

A partir do momento que me familiarizei com a documentação do Django, entrei em outro ritmo. Fiquei muito empolgado por estar aprendendo tanto a cada dia passando horas na frente do computador, apenas lendo e buscando encontrar a melhor forma de fazer o que me estava propondo.

Ainda estou no processo de finalizar a parte de testes do projeto e realizar o deploy da aplicação, dois assuntos sobre os quais ainda estou estudando, mas tudo que desenvolvi até aqui me enche de orgulho e motivação para continuar desenvolvendo!

Só tenho a agradecer à comunidade da Alura pelo desafio, sei que foi extremamente enriquecedor para mim. Nos vemos no próximo Alura Challenge!

<div align="center">
<img width=250 height=250 src="https://user-images.githubusercontent.com/71675056/168167233-f49f2d22-280f-4b94-969c-dfdc5930fccb.png">
<img width=250 height=250 src="https://user-images.githubusercontent.com/71675056/169566763-64de57c1-6de8-462e-b74e-155ddc650cf3.png">
</div>
