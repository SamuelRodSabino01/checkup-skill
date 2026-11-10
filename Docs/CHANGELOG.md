# Histórico de Alterações (`Docs/CHANGELOG.md`)

Todas as modificações notáveis neste projeto serão documentadas neste arquivo em ordem cronológica reversa.

---

## [1.1.0] - 2026-11-09

### Modificado
- Remoção da geração obrigatória de blocos de issues para o GitHub em `SKILL.md`, `scripts/generate_report.py`, `resources/report-data-schema.json` e `references/pdf-design-system.md`.
- Foco exclusivo no diagnóstico factual linha a linha no chat e no relatório executivo em PDF (reduzido para 4 páginas densas e concisas), otimizando o fluxo para uso próprio e direto pelo desenvolvedor.

---

## [1.0.0] - 2026-11-09

### Adicionado
- Criação inicial da skill `security-audit` a partir das especificações de `prompt.md`.
- Implementação de `SKILL.md` contendo o ciclo completo de auditoria (Fase de Reconhecimento, Análise das 5 Categorias Críticas, Rigor Factual e Entrega Dupla: Chat + PDF).
- Criação de `references/vulnerability-catalog.md` mapeando vulnerabilidades reais nas stacks mais comuns (Node/Express/Nest, Laravel, Django/FastAPI, Next.js, Go).
- Criação de `references/pdf-design-system.md` definindo a paleta de cores corporativa, paginação e regras tipográficas do relatório.
- Criação de `resources/issue-template.md` e `resources/report-data-schema.json` para padronização de dados.
- Implementação do script utilitário `scripts/generate_report.py` com isolamento em virtualenv e renderização de PDF profissional via ReportLab e Matplotlib.
- Criação da governança documental em `Docs/` (`ARCHITECTURE.md`, `FILE_MAP.md`, `MODULES.md`, `CHANGELOG.md`, `DECISIONS.md`).

