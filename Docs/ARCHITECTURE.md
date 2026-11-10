# Arquitetura da Skill de Auditoria de Segurança (`security-audit`)

## 1. Visão Geral
A skill `security-audit` foi projetada para atuar como um auditor sênior de segurança em aplicações web e APIs. Ela sistematiza o protocolo de revisão de código originalmente descrito em `prompt.md`, expandindo-o em uma skill modular, reutilizável e orientada a evidências concretas no padrão Google Antigravity.

## 2. Princípios de Engenharia e Auditoria
1. **Verificação Factual Rigorosa**: É expressamente proibida a especulação ou alarme falso. Todo achado deve ter caminho do arquivo, número exato de linha, trecho de código e análise de explorabilidade.
2. **Adaptação Contextual à Stack**: Antes da varredura, a skill identifica a stack completa (linguagem, framework, ORM, autenticação, frontend e infraestrutura/deploy) e traduz as vulnerabilidades para os padrões equivalentes daquela arquitetura.
3. **Equilíbrio (Pontos Fortes vs. Riscos)**: Para provar a cobertura e profundidade da auditoria, a skill documenta tanto o que está vulnerável quanto o que foi examinado e validado como seguro.
4. **Acionabilidade Imediata**: Toda vulnerabilidade acionável é convertida em uma issue completa pronta para o GitHub, com descrição, impacto, mitigação e checklist de critérios de aceite.
5. **Geração Isolada de Relatório**: A geração do relatório executivo em PDF utiliza scripts autônomos que operam em ambiente isolado (virtualenv), preservando o sistema do usuário sem instalações globais.

## 3. Fluxo de Execução da Skill
```
[Início da Auditoria]
        │
        ▼
[Fase 1: Reconhecimento da Stack & Superfície de Ataque]
        │
        ▼
[Fase 2: Varredura Sistemática das 5 Categorias Críticas]
  ├─ 1. Banco Sem Tranca (Isolamento de Inquilino/Tenant/Dono)
  ├─ 2. Permissão Definida no Navegador (Client-side Only Auth)
  ├─ 3. IDOR (Insecure Direct Object Reference em rotas de backend)
  ├─ 4. Chaves Expostas (Hardcode, Defaults Perigosos e Bundles)
  └─ 5. Inputs Sem Tratamento (XSS e Template Injections)
        │
        ▼
[Fase 3: Consolidação dos Achados e Evidências Fatuais]
        │
        ▼
[Fase 4: Geração dos Artefatos]
  ├─ Resumo e Tabela Linha a Linha no Chat
  ├─ Exportação dos Dados Estruturados (JSON)
  ├─ Execução do Script Isolado de PDF (docs/security-audit/relatorio-auditoria-seguranca.pdf)
  └─ Seção de Issues para GitHub com Checklist de Aceite
```

## 4. Estrutura de Diretórios
- `SKILL.md`: Instrução mestra acionada pelo agente, com regras metodológicas e fluxo operacional.
- `references/`: Manuais conceituais e catálogos de vulnerabilidade por stack (`vulnerability-catalog.md`, `pdf-design-system.md`).
- `resources/`: Esquemas de dados e templates de issues (`report-data-schema.json`, `issue-template.md`).
- `scripts/`: Scripts executáveis para geração de relatórios isolados em Python (`generate_report.py`).
- `Docs/`: Documentação de engenharia e governança da própria skill.

