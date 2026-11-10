# Sistema de Design do Relatório em PDF (`references/pdf-design-system.md`)

Este guia define a identidade visual, padrões tipográficos e especificações de diagramação para o relatório executivo de segurança gerado em PDF (`docs/security-audit/relatorio-auditoria-seguranca.pdf`).

---

## 1. Paleta de Cores Obrigatória

| Identificador | Cor Hex | Uso no Relatório |
| :--- | :--- | :--- |
| **Crítica** | `#B91C1C` | Achados críticos, fatias de risco iminente, chips de alerta máximo |
| **Alta** | `#EA580C` | Achados de severidade alta, chips de impacto elevado |
| **Média** | `#D97706` | Achados de severidade média, avisos de atenção |
| **Baixa** | `#2563EB` | Achados de severidade baixa, notas de melhoria |
| **Ponto Forte / Seguro** | `#059669` | Mecanismos verificados e validados, chips de conformidade |
| **Superfície Primária** | `#0F172A` | Títulos principais, texto de alto contraste, cabeçalhos escuros |
| **Superfície Secundária** | `#475569` | Textos de apoio, legendas e descrições técnicas |
| **Bordas e Linhas** | `#E2E8F0` | Divisores de seção e grades de tabela |
| **Fundo Alternado (Zebra)** | `#F8FAFC` | Linhas pares de tabelas e caixas de código |

---

## 2. Geometria da Página e Diagramação

- **Formato do Papel:** A4 padrão internacional (`210mm x 297mm` / `595.27pt x 841.89pt`).
- **Margens:** 2 cm em todas as bordas (`~56.7 pt`).
- **Área Útil de Conteúdo:** Largura aproximada de `482 pt`.
- **Cabeçalho Fixo (a partir da pág. 2):**
  - Alinhado à esquerda: "Relatório de Auditoria de Segurança — [Nome do Projeto]" (`text-xs`, `#64748B`).
  - Linha sutil inferior (`0.5pt`, `#E2E8F0`).
- **Rodapé Fixo:**
  - Alinhado à esquerda: "Confidencial • Uso Interno".
  - Alinhado à direita: "Página X de Y" com contador dinâmico totalizado.

---

## 3. Tipografia e Escala

- **Famílias Recomendadas (PDF):** `Helvetica`, `Helvetica-Bold` e `Courier` (para trechos de código).
- **Escala de Tamanhos:**
  - Título da Capa: `24pt` (Negrito, `#0F172A`).
  - Subtítulo / Metadados da Capa: `12pt` (`#475569`).
  - Título de Seção (H1): `16pt` (Negrito, `#0F172A`, com espaçamento superior de `18pt`).
  - Subtítulo de Seção (H2): `12pt` (Negrito, `#1E293B`, com espaçamento superior de `12pt`).
  - Corpo de Texto: `9.5pt` / Entrelinha `13.5pt` (`#334155`).
  - Células de Tabela: `8.5pt` / Entrelinha `11.5pt`.
  - Código Inline e Blocos de Código: `7.5pt` em fonte monoespaçada com fundo `#F1F5F9`.

---

## 4. Gráficos Executivos

1. **Gráfico de Rosca (Severidade):**
   - Diâmetro proporcional para caber na metade da largura útil (`~220pt`).
   - Centro vazado com percentual de risco ou total de achados.
   - Ordem estrita das fatias e cores: Crítica (`#B91C1C`), Alta (`#EA580C`), Média (`#D97706`), Baixa (`#2563EB`).
2. **Gráfico de Barras Horizontais (Categorias):**
   - Altura de barra calibrada com rótulos das 5 categorias: Banco sem Tranca, Permissão no Navegador, IDOR, Chaves Expostas, Inputs sem Tratamento.
   - Valores numéricos impressos nas extremidades das barras.

---

## 5. Estrutura das Seções do Relatório

1. **Capa Executiva:**
   - Título formal, nome do projeto, data da auditoria, escopo auditado e nota metodológica (como as 5 categorias foram adaptadas à stack).
2. **Resumo Executivo:**
   - Cards de métricas rápidas (Total de Achados, Críticos, Altos, Médios, Baixos).
   - Painel lado a lado com gráfico de rosca e gráfico de barras.
3. **Pontos Fortes e Riscos Centrais:**
   - Lista comprovada do que está protegido com evidência factual.
   - Síntese dos riscos estruturais identificados.
4. **Tabela de Achados Detalhados por Categoria:**
   - Colunas: `Severidade` (chip colorido), `Arquivo:Linha`, `Descrição & Impacto`.
5. **Recomendações Priorizadas:**
   - Matriz P1 (Imediato), P2 (Curto Prazo), P3 (Higiene de Segurança).

