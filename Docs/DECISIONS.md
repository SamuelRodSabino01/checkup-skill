# Registro de Decisões Arquiteturais (`Docs/DECISIONS.md`)

Este registro adota o padrão Architecture Decision Records (ADR). Consulte este arquivo antes de alterar padrões ou premissas técnicas estabelecidas.

---

## ADR 001: Transformação do `prompt.md` em Skill Modular no Padrão Antigravity

- **Data:** 2026-11-09
- **Status:** Aceito
- **Contexto:**
  O arquivo original `prompt.md` continha um prompt direto e denso para auditoria de segurança em 5 categorias e posterior emissão de relatório PDF e issues para GitHub. Era necessário transformá-lo em uma Skill oficial do Antigravity, garantindo acionamento inteligente por agentes, conformidade com a convenção de skills (`SKILL.md`, `references/`, `resources/`, `scripts/`) e reutilização em múltiplos projetos.
- **Decisão:**
  1. Estruturar a raiz do projeto como a própria skill ou utilizável em `.agents/skills/security-audit/` e `~/.gemini/config/skills/security-audit/`.
  2. Adicionar o frontmatter YAML com instruções assertivas no campo `description` para ativação automática quando houver pedidos de revisão de segurança, auditoria, IDOR, RLS, XSS ou checkup.
  3. Desacoplar detalhes volumosos em referências (`references/vulnerability-catalog.md` e `references/pdf-design-system.md`) para poupar janela de contexto durante o carregamento inicial (Progressive Disclosure).
- **Consequências:**
  - Carregamento rápido da skill com ativação sob demanda.
  - O agente ganha uma metodologia estruturada em fases bem delimitadas.

---

## ADR 002: Isolamento da Geração do Relatório PDF via Script Python Automatizado

- **Data:** 2026-11-09
- **Status:** Aceito
- **Contexto:**
  O requisito estipula que a geração do PDF deve ser visualmente profissional (A4, 2cm de margem, gráficos de rosca e barras, paleta de cores corporativa, tabela com chips coloridos, paginação e blocos de issues) e não deve poluir ou instalar pacotes de forma global no sistema operacional do usuário.
- **Decisão:**
  1. Criar um script Python `scripts/generate_report.py` capaz de orquestrar a geração com `reportlab` e `matplotlib`.
  2. Implementar no próprio script a capacidade de verificar e inicializar um ambiente virtual Python isolado temporário (`.venv_audit`) caso as bibliotecas não estejam presentes, instalando-as apenas dentro desse ambiente sem tocar no ambiente global.
  3. Salvar o PDF no diretório padrão solicitado (`docs/security-audit/relatorio-auditoria-seguranca.pdf`) e manter o script gerador acessível para reexecuções futuras.
- **Consequências:**
  - Atendimento total à restrição de segurança e isolamento.
  - Relatório reproduzível a qualquer momento em ambientes locais ou de CI.

