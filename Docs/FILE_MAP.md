# Mapa de Arquivos do Projeto (`Docs/FILE_MAP.md`)

Este documento mapeia todos os arquivos do projeto, sua finalidade, dependências importadas e relações cruzadas.

---

## 1. Núcleo da Skill
- **`SKILL.md`**
  - **Finalidade:** Arquivo principal de definição da skill no padrão Antigravity. Contém frontmatter YAML (`name`, `description`), protocolo de detecção de stack, procedimentos de varredura das 5 categorias, regras metodológicas e instruções para geração do relatório PDF executivo e diagnóstico no chat.
  - **Dependências / Referências:**
    - Consulta `references/vulnerability-catalog.md` para padrões por stack.
    - Consulta `references/pdf-design-system.md` para diretrizes de layout e cores.
    - Utiliza `scripts/generate_report.py` para geração do PDF executivo.

- **`README.md`**
  - **Finalidade:** Manual principal de apresentação da skill, guia de instalação global (`~/.gemini/config/skills/security-audit`), instruções de instalação via IA/NPM/Terminal e créditos ao Mano Deyvin.

- **`package.json`**
  - **Finalidade:** Manifesto do pacote Node.js com scripts auxiliares de teste e comando de instalação global via npm.

---

## 2. Referências (`references/`)
- **`references/vulnerability-catalog.md`**
  - **Finalidade:** Guia aprofundado com exemplos práticos de código vulnerável vs. seguro para cada uma das 5 categorias (Node.js, Next.js, Laravel, Django/FastAPI, Go, Supabase/Prisma).
  - **Usado por:** `SKILL.md` durante o processo de análise e auditoria de código.

- **`references/pdf-design-system.md`**
  - **Finalidade:** Guia visual e regras de layout do relatório corporativo em PDF (paleta de cores, tipografia, dimensões A4, margens de 2cm, cabeçalhos, rodapés e convenções dos gráficos).
  - **Usado por:** `scripts/generate_report.py` e `SKILL.md`.

---

## 3. Recursos (`resources/`)
- **`resources/report-data-schema.json`**
  - **Finalidade:** Schema JSON estruturado que padroniza os dados coletados na auditoria (metadados do projeto, resumo estatístico, pontos fortes, achados detalhados e recomendações).
  - **Usado por:** `scripts/generate_report.py` para carregar dados de entrada.

- **`resources/sample-audit-data.json`**
  - **Finalidade:** Conjunto de dados de exemplo representativos para teste e demonstração imediata do gerador de PDF.
  - **Usado por:** `scripts/generate_report.py`.

---

## 4. Scripts Utilitários (`scripts/`)
- **`scripts/generate_report.py`**
  - **Finalidade:** Script standalone em Python capaz de orquestrar a geração do relatório em PDF usando ReportLab e Matplotlib em ambiente virtual temporário/isolado, respeitando a paleta e os padrões estéticos definidos.
  - **Entrada:** Arquivo JSON aderente ao `report-data-schema.json`.
  - **Saída:** Arquivo PDF salvo no caminho indicado (por padrão `docs/security-audit/relatorio-auditoria-seguranca.pdf`).

---

## 5. Governança e Configurações
- **`Docs/ARCHITECTURE.md`**: Visão geral de arquitetura, fluxo de dados e princípios da skill.
- **`Docs/FILE_MAP.md`**: Este mapa de arquivos e referências cruzadas.
- **`Docs/MODULES.md`**: Detalhamento funcional de cada módulo, classe e função.
- **`Docs/CHANGELOG.md`**: Histórico cronológico de mudanças do projeto.
- **`Docs/DECISIONS.md`**: Registros de decisões arquiteturais (ADR).
- **`.gitignore`**: Configuração de exclusão de artefatos temporários e ambientes virtuais locais (`.venv_audit`).
- **`.gitattributes`**: Normalização de quebras de linha para controle de versão.
