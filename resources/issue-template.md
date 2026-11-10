# Template de Issue para GitHub

Este template padroniza a formatação de cada achado de segurança acionável gerado pela auditoria, facilitando a abertura direta no GitHub.

---

```markdown
--- ISSUE [NÚMERO] ---
### [Segurança] [Descrição curta e objetiva da falha]

**Labels sugeridas:** `security`, `severidade: [critica|alta|media|baixa]`
**Categoria:** [Banco sem Tranca | Permissão no Navegador | IDOR | Chaves Expostas | XSS]

#### 1. Descrição do Problema
[Explicação clara do defeito técnico identificado e por que ele é explorável no contexto da aplicação]

#### 2. Evidência
- **Arquivo:** `[caminho/do/arquivo]`
- **Linha(s):** `[L12-L25]`

```[linguagem]
// Trecho de código vulnerável com contexto
```

#### 3. Condições de Explorabilidade e Vetor de Ataque
- **Pré-requisitos:** [Ex: usuário autenticado comum / sem autenticação / feature flag X ativa]
- **Vetor:** [Ex: Requisição POST para /api/v1/invoices/999 com token de outro tenant]

#### 4. Impacto
[Consequências para o negócio: vazamento de dados de múltiplos clientes, sequestro de conta, perda de integridade, etc.]

#### 5. Sugestão de Correção
[Explicação da correção recomendada acompanhada de snippet corrigido]

```[linguagem]
// Exemplo de código seguro
```

#### 6. Critérios de Aceite (Checklist)
- [ ] [ ] O endpoint/consulta valida explicitamente o vínculo entre o registro e o usuário/tenant autenticado.
- [ ] [ ] Testes automatizados (unitários ou de integração) cobrem tentativas de acesso com ID de outro tenant (esperado 403/404).
- [ ] [ ] Validação manual realizada em ambiente de homologação.
--- FIM ISSUE [NÚMERO] ---
```

