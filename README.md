# Desafio Técnico - QA PayStore

Este repositório contém a resolução do desafio técnico para a vaga de QA de estágio, contemplando testes de API e Frontend.

## Estrutura do Projeto
* `/backend-api`: Contém a Collection exportada do Postman e o relatório de execução.
* `/frontend-web`: Contém o script de automação Web.

---

## PARTE 1: Planejamento e Testes de Backend (API)

* Swagger Petstore (`https://petstore.swagger.io/`)
* **Ferramenta:** Postman
* **Estratégia de Automação:** Utilização da aba *Tests* do Postman para asserções dinâmicas de Status Code e validação de chaves/valores no conteúdo do JSON de resposta.

**Plano de Testes - API (Swagger Petstore)**

* **REQ-01: Cadastro de um novo Pet**
  * Cenário Normal: Enviar uma requisição POST para `/pet` com um JSON válido contendo `id`, `name` e `status`. 
    * **Resultado Esperado:** Status Code 200 OK e o corpo da resposta deve retornar exatamente os mesmos dados enviados.
  * Cenário Edge Case (Violação de Regra de Negócio): Enviar a requisição POST com o campo `status` contendo um valor inexistente no Enum permitido pela documentação (ex: `"status": "fantasma"`). 
    * **Resultado Esperado:** A API deveria barrar a entrada e retornar *400 Bad Request*. 
    * **Bug Encontrado:** O backend falha na validação, aceita o status inválido e retorna *200 OK*. O teste automatizado no Postman falha propositalmente para evidenciar essa quebra de contrato.

* **REQ-02: Busca de um Pet por ID**
  * Cenário Normal: Enviar uma requisição GET para `/pet/{id}` utilizando o ID numérico válido do pet recém-criado. 
    * **Resultado Esperado:** Status Code 200 OK e a resposta deve conter o JSON com os dados exatos do pet.
  * Cenário Edge Case (Omissão e Formato Inválido):
    * 1) Omissão do ID na rota (`/pet/`). 
        * **Resultado Esperado:** API bloqueia e retorna *405 Method Not Allowed*. 
    * 2) Envio de ID com casa decimal (ex: `123.99`). 
        * **Resultado Esperado:** API retorna erro *404* e expõe indevidamente a *stacktrace* do Java (`NumberFormatException`).

* **REQ-03: Busca de ID inexistente (Tratamento de Erro)**
  * Cenário Normal: Enviar uma requisição GET para `/pet/{id}` com um ID gigante que não existe no banco. 
    * **Resultado Esperado:** Status Code 404 Not Found e validação da mensagem "Pet not found".
  * Cenário Edge Case (ID Negativo): Enviar a requisição GET com um ID negativo (ex: `/pet/-1`), violando o padrão numérico esperado.
    * **Resultado Esperado:** A API deve rejeitar a busca, retornando Status Code 404.

* **REQ-04: Exclusão do Pet criado**
  * Cenário Normal: Enviar uma requisição DELETE para `/pet/{id}` utilizando o ID do pet criado no REQ-01. 
    * **Resultado Esperado:** Status Code 200 OK, confirmando a exclusão do recurso.
  * Cenário Edge Case (Dupla Deleção): Enviar a mesma requisição DELETE para o pet que acabou de ser excluído. 
    * **Resultado Esperado:** Status Code 404 Not Found, validando que o pet não existe mais na base de dados.

**Diferencial Entregue:** Geração de relatório de execução das requisições documentando o sucesso dos testes básicos e a falha dos bugs mapeados.

---

## PARTE 2: Planejamento e Testes de Frontend (Web)

* [Site Phoebus](https://www.phoebus.com.br/)  
* **Ferramentas:** Python, Selenium, Pytest, pytest-html, webdriver-manager

### Plano de Testes

* **Validação da Linha do Tempo (História)**
  * **Cenário Normal:** Acessar o site oficial, navegar até o menu "História" e clicar em 3 anos distintos na linha do tempo (1997, 2000, 2022).
  * **Lógica Implementada:** O script lida com sobreposições dinâmicas (fechamento automático de banner de Cookies), realiza *scroll* de tela programado para enquadramento correto dos elementos e utiliza *Explicit Waits* (`WebDriverWait`) para garantir o carregamento da DOM antes das ações.
  * **Validação:** Uso de `assert` garantindo que o texto descritivo atualizado na tela corresponde exatamente ao botão do ano selecionado.

* **Diferenciais Entregues:**
  * **Evidências (Screenshots):** O código gera automaticamente um arquivo `.png` perfeitamente enquadrado para cada um dos 3 anos testados.
  * **Relatório de Execução:** Geração de um dashboard completo via Pytest (`relatorio_frontend.html`) narrando o passo a passo da execução com logs e prints embutidos de forma autossuficiente e interativa.

---

## Como Reproduzir os Testes

### Backend (Postman)
1. Tenha o [Postman](https://www.postman.com/) instalado.
2. Importe o arquivo `swagger-petstore-collection.json` (localizado na pasta `/backend-api`).
3. Execute a coleção utilizando o **Collection Runner** para visualizar a bateria de testes e as asserções de conteúdo de JSON.

### Frontend (Selenium/Python)
**Pré-requisitos:** Python 3.x e Google Chrome instalados na máquina.

1. Acesse o diretório do frontend via terminal:
   ```bash
   cd frontend-web
   ```
2. Instale as dependências necessárias do projeto:
    ```bash
    pip install selenium webdriver-manager pytest pytest-html
    ```
3. Execute a automação e gere o relatório interativo:
    ```bash
    python -m pytest automacao_phoebus.py --html=relatorio_frontend.html --self-contained-html
    ```
