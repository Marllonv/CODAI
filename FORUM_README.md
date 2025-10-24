# Sistema de Fórum Dinâmico - CODAI

## 📋 Funcionalidades Implementadas

### ✅ Modelos de Banco de Dados
- **Category**: Categorias para organizar posts (javascript, react, python, etc.)
- **Post**: Posts do fórum com título, conteúdo, categoria e destaque
- **Comment**: Comentários nos posts
- **User**: Usuários (já existente, integrado com o sistema)

### ✅ Rotas e Funcionalidades
- **Visualização**: Lista todos os posts com filtros por categoria
- **Criação**: Formulário para criar novos posts
- **Edição**: Editar posts próprios (ou todos se for admin)
- **Exclusão**: Deletar posts próprios (ou todos se for admin)
- **Comentários**: Sistema completo de comentários
- **Detalhes**: Página individual para cada post

### ✅ Interface Dinâmica
- Posts carregados dinamicamente do banco de dados
- Filtros por categoria com cores personalizadas
- Metadados dos posts (autor, data, número de comentários)
- Sistema de destaque para posts importantes
- Design responsivo e moderno

## 🚀 Como Usar

### 1. Executar o Sistema
```bash
python app.py
```

### 2. Acessar o Fórum
- URL: `http://localhost:5000/forum`
- Login: `admin@codai.com` / Senha: `123456`

### 3. Funcionalidades Disponíveis

#### Para Usuários Logados:
- ✅ Criar novos posts
- ✅ Comentar em posts
- ✅ Editar/deletar próprios posts
- ✅ Filtrar posts por categoria

#### Para Administradores:
- ✅ Todas as funcionalidades acima
- ✅ Editar/deletar qualquer post
- ✅ Destacar posts importantes

## 📁 Estrutura de Arquivos Criados

```
models/
├── forum.py              # Modelos Category, Post, Comment

routes/
└── forum/
    └── __init__.py       # Rotas do fórum (CRUD completo)

templates/
├── forum.html            # Lista de posts (atualizado)
└── forum/
    ├── create_post.html  # Formulário de criação
    ├── post_detail.html  # Detalhes do post + comentários
    └── edit_post.html    # Formulário de edição

static/css/
└── forum.css            # Estilos atualizados
```

## 🎨 Categorias Padrão

O sistema cria automaticamente as seguintes categorias:

| Categoria | Cor | Descrição |
|-----------|-----|-----------|
| javascript | #f7df1e | Discussões sobre JavaScript |
| react | #61dafb | React e bibliotecas relacionadas |
| python | #3776ab | Python e suas aplicações |
| frontend | #ff6b6b | Desenvolvimento front-end |
| git | #f05032 | Git e GitHub |
| datascience | #ff9f43 | Data Science e análise de dados |

## 🔧 Rotas Disponíveis

| Rota | Método | Descrição |
|------|--------|-----------|
| `/forum/` | GET | Lista todos os posts |
| `/forum/create` | GET/POST | Criar novo post |
| `/forum/post/<id>` | GET | Ver post específico |
| `/forum/post/<id>/edit` | GET/POST | Editar post |
| `/forum/post/<id>/delete` | POST | Deletar post |
| `/forum/post/<id>/comment` | POST | Adicionar comentário |
| `/forum/category/<id>` | GET | Posts por categoria |
| `/forum/api/posts` | GET | API JSON dos posts |

## 💡 Próximos Passos Sugeridos

1. **Sistema de Busca**: Implementar busca por texto nos posts
2. **Paginação**: Adicionar paginação para muitos posts
3. **Upload de Imagens**: Permitir imagens nos posts
4. **Sistema de Likes**: Curtir posts e comentários
5. **Notificações**: Notificar sobre novos comentários
6. **Moderação**: Sistema de denúncia e moderação

## 🐛 Solução de Problemas

### Banco de Dados
- Se houver problemas com o banco, delete o arquivo `instance/codai.db` e reinicie
- O sistema recriará automaticamente todas as tabelas e dados de exemplo

### Permissões
- Apenas o autor do post ou admin pode editar/deletar
- Usuários não logados podem apenas visualizar posts

### Estilos
- Todos os estilos estão no arquivo `static/css/forum.css`
- Design responsivo para mobile e desktop
