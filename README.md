# Desafio Técnico - QA PayStore

Este repositório contém a resolução do desafio técnico para a vaga de QA de estágio, contemplando testes de API e Frontend.

## Estrutura do Projeto
* `/backend-api`: Contém a Collection exportada do Postman e o relatório de execução.
* `/frontend-web`: Contém o script de automação Web.

---

## PARTE 1: Planejamento e Testes de Backend (API)

**Plano de Testes - API (Swagger Petstore)**

* **REQ-01: Cadastro de um novo Pet**
  * Cenário Normal: Enviar uma requisição POST para `/pet` com um JSON válido contendo `id`, `name` e `status`. 
    * **Resultado Esperado:** Status Code 200 OK e o corpo da resposta deve retornar exatamente os mesmos dados enviados.
  * Cenário Edge Case (Violação de Regra de Negócio):** Enviar a requisição POST com o campo `status` contendo um valor inexistente no Enum permitido pela documentação (ex: `"status": "fantasma"`). 
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

---

## PARTE 2: Planejamento e Testes de Frontend (Web)

