# 🛡️ Security Audit Skill (`security-audit`)

> **Skill de Auditoria de Segurança de Código para SaaS e APIs no padrão Google Antigravity & Agentes de IA.**
>
> 💡 **Créditos:** Esta skill foi concebida a partir da metodologia e do conteúdo criado pelo mestre **[Mano Deyvin](https://www.youtube.com/@manodeyvin)** em seu vídeo clássico sobre **[Auditoria de Segurança em SaaS](https://youtu.be/mjSOFCDV_wA)**.

---

## 📺 Créditos & Inspiração

Esta skill é uma adaptação direta dos ensinamentos de segurança do canal **Mano Deyvin**:
- **Canal Oficial:** [@manodeyvin](https://www.youtube.com/@manodeyvin)
- **Vídeo de Referência:** [Auditoria de Segurança de SaaS (YouTube)](https://youtu.be/mjSOFCDV_wA)

O Mano Deyvin sistematizou as 5 falhas mais comuns e catastróficas que derrubam plataformas SaaS e startups. Esta skill transforma essas diretrizes em um agente de auditoria autônomo, factual e contextualizado para a stack do seu projeto.

---

## 🎯 As 5 Falhas de Segurança Auditadas

1. 🔒 **BANCO SEM TRANCA (Isolamento de Inquilino / Dono):**
   - **Supabase / PostgreSQL:** Falhas ou ausência de Row Level Security (RLS) em tabelas públicas, policies permissivas com `USING (true)` ou exposição da chave `service_role`.
   - **ORMs Próprios (Prisma, Drizzle, Eloquent, TypeORM, SQLAlchemy):** Consultas de listagem, busca, agregação (`count`, `sum`), relatórios e exportações (CSV/JSON) que esquecem de filtrar pelo usuário/tenant autenticado.

2. 🌐 **PERMISSÃO DEFINIDA NO NAVEGADOR (Client-Side Only Authorization):**
   - Operações sensíveis (painel admin, exclusão de dados, configurações) onde a UI esconde o botão com base em papéis (`isAdmin`, `role === 'admin'`), mas o backend não valida a autorização no endpoint correspondente.

3. 🔑 **IDOR (Insecure Direct Object References):**
   - Rotas que recebem identificadores (`id`, `uuid`, `slug`) via path param, query string ou body para buscar, alterar ou deletar um registro sem verificar se o objeto pertence ao usuário chamador.

4. 🏷️ **CHAVES EXPOSTAS (Hardcode & Defaults Inseguros):**
   - Tokens, senhas de banco, segredos de assinatura (JWT, webhooks) embutidos no código, `docker-compose.yml`, Helm ou CI/CD.
   - Defaults perigosos de variáveis de ambiente (`${JWT_SECRET:-secret123}`) que viram senhas reais se não forem sobrescritos em produção, sem validação no startup.
   - Credenciais privadas expostas em variáveis públicas de frontend (`NEXT_PUBLIC_` / `VITE_`).

5. 💉 **INPUTS SEM TRATAMENTO (XSS & Injeções de Template):**
   - **Frontend:** Injeção direta de HTML no DOM (`dangerouslySetInnerHTML`, `v-html`, `[innerHTML]`), URLs `javascript:` em tags `<a href>` e execução dinâmica com `eval()`.
   - **Backend:** Concatenação de entradas de usuários em e-mails HTML transacionais ou relatórios sem escape contextual.

---

## ⚡ Como Instalar a Skill

Escolha o método mais conveniente para o seu ambiente:

### Método 1: Pedindo para a sua IA (Recomendado) 🤖

Abra o seu assistente de código favorito (**Google Antigravity**, **Claude Code**, **Cursor**, **Windsurf**, **Roo Code** ou **Copilot**) e cole o seguinte prompt no chat:

```markdown
Por favor, instale a skill de auditoria de segurança a partir deste repositório na minha pasta global de skills:
- Se for Antigravity: configure como junction/pasta em ~/.gemini/config/skills/security-audit
- Se for local do projeto: copie para a pasta .agents/skills/security-audit/
Certifique-se de que o arquivo SKILL.md e as pastas references/, resources/ e scripts/ estejam acessíveis.
```

---

### Método 2: Via NPM / NPX 📦

Se você já possui Node.js instalado, pode instalar diretamente via terminal:

```bash
# Clone e instalação rápida usando npx degit
npx degit seu-usuario/checkup-skill ~/.gemini/config/skills/security-audit

# Ou se você clonou este repositório localmente:
npm run install:global
```

---

### Método 3: Instalação Manual via Terminal 💻

#### Windows (PowerShell):
Para instalar globalmente no Antigravity vinculando via Junction (qualquer atualização na pasta reflete instantaneamente):

```powershell
New-Item -ItemType Junction -Path "$HOME\.gemini\config\skills\security-audit" -Target "C:\caminho\para\checkup-skill" -Force
```

#### Linux / macOS (Bash):
Para instalar criando um link simbólico global:

```bash
ln -s "/caminho/para/checkup-skill" "$HOME/.gemini/config/skills/security-audit"
```

#### Para um único projeto:
Basta copiar os arquivos para a pasta `.agents/skills/security-audit/` na raiz do repositório alvo.

---

## 🚀 Como Usar no Dia a Dia

Com a skill instalada, abra qualquer projeto no seu editor e peça ao assistente no chat:

- *"Faça uma auditoria de segurança completa no código deste projeto."*
- *"Execute o checkup do Mano Deyvin nos endpoints e nas queries de banco."*
- *"Audite a aplicação atrás de IDOR, falhas de RLS/tenant e credenciais expostas."*

### O que o assistente entrega:
1. **Diagnóstico linha a linha no chat:** Lista categorizada com arquivo, linha exata, trecho vulnerável e condição de explorabilidade.
2. **Pontos Fortes:** Registro do que foi analisado e está devidamente protegido.
3. **Relatório Executivo em PDF:** Um documento A4 visualmente amigável gerado em `docs/security-audit/relatorio-auditoria-seguranca.pdf`, contendo:
   - Capa executiva e nota metodológica adaptada à stack detectada.
   - Resumo numérico e gráficos de rosca e barras horizontais por severidade/categoria.
   - Tabela zebra de achados detalhados com chips de severidade coloridos.
   - Plano de recomendações priorizadas (P1, P2, P3).

---

## 📊 Geração Manual / Teste do Relatório em PDF

O script gerador roda em ambiente isolado via virtualenv (`.venv_audit`), sem instalar pacotes globais na sua máquina:

```bash
# Gerar PDF de demonstração com dados de amostra
python scripts/generate_report.py --sample --output docs/security-audit/relatorio-auditoria-seguranca.pdf

# Gerar PDF a partir de um arquivo JSON personalizado
python scripts/generate_report.py --input resources/sample-audit-data.json --output docs/security-audit/relatorio-auditoria-seguranca.pdf
```

---

## 📁 Estrutura de Arquivos

```text
checkup-skill/
├── SKILL.md                          # Instrução mestra acionada pelo Antigravity
├── README.md                         # Guia de instalação e documentação
├── package.json                      # Scripts e metadados npm
├── .gitignore                        # Regras de exclusão do git
├── .gitattributes                    # Normalização de line endings
├── references/
│   ├── vulnerability-catalog.md      # Guia de identificação das 5 falhas por stack
│   └── pdf-design-system.md          # Especificação de cores e layout A4 do PDF
├── resources/
│   ├── report-data-schema.json       # Schema de validação do JSON da auditoria
│   └── sample-audit-data.json        # Dados de teste para demonstração do PDF
├── scripts/
│   └── generate_report.py            # Gerador de PDF em Python com venv isolado
└── Docs/                             # Governança documental (Padrão Antigravity)
    ├── ARCHITECTURE.md
    ├── FILE_MAP.md
    ├── MODULES.md
    ├── CHANGELOG.md
    └── DECISIONS.md
```

---

## 🤝 Créditos Finais

Agradecimento especial ao **[Mano Deyvin](https://www.youtube.com/@manodeyvin)** pelo conteúdo original, pela didática e pela contribuição fundamental à comunidade de desenvolvimento de software e segurança na web!

Vídeo original: [https://youtu.be/mjSOFCDV_wA](https://youtu.be/mjSOFCDV_wA)
