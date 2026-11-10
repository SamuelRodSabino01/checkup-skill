# Módulos e Regras de Negócio (`Docs/MODULES.md`)

Este documento detalha as funções, regras operacionais e estruturas dos componentes da skill `security-audit`.

---

## 1. Módulo Principal: `SKILL.md`

### 1.1 Assinatura e Gatilho (Frontmatter)
- **`name`**: `security-audit`
- **`description`**: Gatilho para acionamento pelo agente quando requisitado checkup, auditoria, revisão de segurança ou varredura de vulnerabilidades (IDOR, RLS, hardcoded keys, client authorization bypass, XSS) em qualquer repositório.

### 1.2 Regras de Negócio Operacionais
1. **Detecção Preliminar de Stack**:
   - Varrer manifestos (`package.json`, `composer.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, etc.).
   - Identificar framework web (Express, Fastify, Next.js, Laravel, Django, FastAPI, Spring Boot, Gin).
   - Identificar ORM/DB (Prisma, Drizzle, TypeORM, Eloquent, SQLAlchemy, Django ORM, Supabase).
   - Identificar Auth (NextAuth, Supabase Auth, Clerk, JWT próprio, Laravel Sanctum, Passport).
   - Identificar Frontend (React, Vue, Blade, Jinja, Angular, Svelte) e Infraestrutura (Docker, Kubernetes, CI/CD, Terraform).
2. **As 5 Categorias Críticas**:
   - **Cat. 1 - Banco sem Tranca**: Falhas de RLS ou falta de filtro por tenant/user_id em queries de listagem, agregação e exportação.
   - **Cat. 2 - Permissão Definida no Navegador**: Rota protegida visualmente no frontend sem validação no endpoint do backend.
   - **Cat. 3 - IDOR**: Manipulação de IDs sem checagem de propriedade/posse no backend.
   - **Cat. 4 - Chaves Expostas**: Chaves, tokens, segredos hardcoded ou defaults inseguros em configs/docker/CI e histórico git.
   - **Cat. 5 - Inputs sem Tratamento**: Injeção XSS no client (`dangerouslySetInnerHTML`, `v-html`, `eval`) ou no backend (templates de e-mail/HTML sem escape).
3. **Padrão de Severidade**:
   - `Crítica`: Execução de código remoto, bypass total de autenticação/banco, vazamento massivo multitenant.
   - `Alta`: IDOR com alteração/deleção de dados alheios, vazamento de credenciais de produção, XSS armazenado.
   - `Média`: Falha de isolamento em relatórios secundários, segredos com defaults fracos em desenvolvimento, XSS refletido.
   - `Baixa`: Falta de validação estrita sem impacto direto de exploração, headers de segurança ausentes.
   - `Informativa`: Boas práticas sugeridas, redundâncias de segurança recomendadas.

---

## 2. Módulo de Script: `scripts/generate_report.py`

### 2.1 Funções Principais
- **`ensure_environment()`**:
  - Verifica se o ambiente possui `reportlab` e `matplotlib`.
  - Se ausentes, cria ou utiliza um ambiente virtual Python isolado (`.venv_audit` temporário) e instala as dependências sem afetar o sistema global.
- **`generate_charts(data, output_dir)`**:
  - `generate_donut_chart(severity_counts, output_path)`: Gera gráfico de rosca de severidades com a paleta exata (#B91C1C, #EA580C, #D97706, #2563EB, #059669).
  - `generate_bar_chart(category_counts, output_path)`: Gera gráfico de barras de achados por categoria.
- **`build_pdf(data_json_path, pdf_output_path)`**:
  - Carrega os dados estruturados do JSON.
  - Constrói o documento com margens de 2cm, cabeçalho/rodapé com paginação ("Página X de Y").
  - Renderiza:
    1. Capa executiva
    2. Resumo executivo com métricas e gráficos inseridos
    3. Seção de Pontos Fortes e Riscos
    4. Tabela de Achados Detalhados com Chips de Severidade Coloridos
    5. Recomendações Priorizadas (P1, P2, P3...)
- **`main()`**:
  - Interface CLI que aceita caminhos de entrada JSON e saída PDF.

---

## 3. Módulo de Recursos e Referências

- **`resources/report-data-schema.json`**:
  - Valida o payload de dados coletados para assegurar que o gerador de PDF receba todos os campos necessários.
- **`resources/issue-template.md`**:
  - Define o formato canônico de cada issue a ser aberta no repositório.
- **`references/vulnerability-catalog.md`**:
  - Base de conhecimento com sintaxes reais por framework para aceleração de diagnóstico pelo auditor.
- **`references/pdf-design-system.md`**:
  - Padronização estética para garantir apresentação profissional e executiva.

