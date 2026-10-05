# Roteiro da apresentação — TP03 (5 a 10 min)

Demonstração ao vivo no Swagger (<http://localhost:8000/docs>).

## Antes de começar

Comece com o banco vazio, para os ids da demo serem 1, 2, 3:

```bash
cd tp03-api
rm -f biblioteca.db
alembic upgrade head
uvicorn app.main:app --reload
```

Deixe o Swagger aberto e o VS Code com o projeto ao lado.

## Sequência

### 1. Estrutura e migração — Hélio (~2 min)

- Mostrar as pastas: `models` (tabelas), `schemas` (entrada e saída), `routers` (endpoints), `core/database.py` (conexão).
- Mostrar os models `Autor` e `Livro`: a `ForeignKey` em `livros.autor_id` e o `relationship()` nos dois lados (1:N).
- Mostrar a migração em `alembic/versions/` e explicar que o banco nasce só pelo `alembic upgrade head`, não pelo código da API.
- Comentar o `PRAGMA foreign_keys=ON`: o SQLite ignora FK sem ele.

### 2. Autores — Augusto (~2 min)

1. **Criar um autor → 201.** `POST /autores/`:

   ```json
   { "nome": "Machado de Assis", "nacionalidade": "Brasileira" }
   ```

   Anotar o `id` devolvido (1).
2. **Listar** com `GET /autores/` e **buscar** com `GET /autores/1` → 200.
3. **Buscar um id que não existe**: `GET /autores/999` → 404.

### 3. Livros e validação — Yan (~3 min)

1. **Criar um livro com esse autor → 201.** `POST /livros/`:

   ```json
   { "titulo": "Dom Casmurro", "ano": 1899, "autor_id": 1 }
   ```

2. **Criar um livro com `autor_id` inexistente → 404.** `POST /livros/`:

   ```json
   { "titulo": "Livro Fantasma", "autor_id": 999 }
   ```

   Ler a mensagem: `Autor 999 não encontrado. Cadastre o autor antes do livro.` Explicar que o router confere o autor antes de gravar (validação da FK).
3. **Enviar body inválido → 422.** `POST /livros/` sem o título:

   ```json
   { "ano": 1899 }
   ```

   Explicar que o Pydantic recusa a requisição antes de chegar ao banco e diz qual campo falta.
4. **Listar** com `GET /livros/` e mostrar o filtro `GET /livros/?autor_id=1` → 200.
5. **Atualizar** só o ano com `PATCH /livros/1` → 200. Mostrar que o título não mudou:

   ```json
   { "ano": 1900 }
   ```

### 4. Regra de exclusão — Augusto e Yan (~1 min)

1. **Augusto:** tentar apagar o autor que tem livro: `DELETE /autores/1` → **409**. Ler a mensagem: a API não apaga os livros em silêncio.
2. **Yan:** apagar o livro: `DELETE /livros/1` → 204. Repetir o `DELETE /livros/1` → 404.
3. **Augusto:** apagar o autor de novo: `DELETE /autores/1` → agora 204.

### 5. Fechamento — Hélio (~30 s)

Resumir: três camadas (models, schemas, routers), banco versionado com Alembic, validações com 404, 409 e 422.

## Checklist dos status mostrados

| Status | Onde aparece |
|---|---|
| 201 | Criar autor; criar livro |
| 200 | Listar, buscar e atualizar |
| 204 | Apagar livro; apagar autor sem livros |
| 404 | Id inexistente; livro com `autor_id` inexistente |
| 409 | Apagar autor com livros |
| 422 | Body sem campo obrigatório |
