#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração de Relatório de Auditoria de Segurança em PDF
Gera um documento PDF em formato A4, visualmente amigável, com gráficos,
tabelas, chips de severidade e issues prontas para o GitHub.

Utiliza ambiente isolado (venv) para dependências (reportlab + matplotlib).
"""

import os
import sys
import json
import argparse
import tempfile
import subprocess
from pathlib import Path

# Paleta de Cores Obrigatória
COLOR_CRITICAL = "#B91C1C"
COLOR_HIGH = "#EA580C"
COLOR_MEDIUM = "#D97706"
COLOR_LOW = "#2563EB"
COLOR_STRENGTH = "#059669"
COLOR_INFORMATIVE = "#64748B"

SEVERITY_COLORS = {
    "Crítica": COLOR_CRITICAL,
    "Alta": COLOR_HIGH,
    "Média": COLOR_MEDIUM,
    "Baixa": COLOR_LOW,
    "Informativa": COLOR_INFORMATIVE,
}

def ensure_dependencies():
    """Garante que reportlab e matplotlib estejam disponíveis em um venv isolado."""
    try:
        import reportlab
        import matplotlib
        return True
    except ImportError:
        pass

    script_dir = Path(__file__).resolve().parent
    venv_dir = script_dir / ".venv_audit"
    python_bin = venv_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    if not venv_dir.exists():
        print(f"[+] Criando ambiente virtual isolado em {venv_dir}...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])

    print("[+] Instalando dependências (reportlab, matplotlib) no venv isolado...")
    pip_bin = venv_dir / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    subprocess.check_call([str(pip_bin), "install", "--quiet", "reportlab", "matplotlib"])

    print(f"[+] Re-executando através do venv isolado ({python_bin})...")
    args = [str(python_bin), str(__file__)] + sys.argv[1:]
    sys.exit(subprocess.call(args))

ensure_dependencies()

# Imports das bibliotecas gráficas e de PDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas com duas passadas para calcular dinamicamente o número total de páginas."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Cabeçalho (a partir da página 2)
        if self._pageNumber > 1:
            project_title = getattr(self, "report_project_name", "Auditoria de Segurança")
            self.drawString(2 * cm, 28.5 * cm, f"Relatório de Auditoria de Segurança — {project_title}")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(2 * cm, 28.3 * cm, 19 * cm, 28.3 * cm)

        # Rodapé
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.6 * cm, 19 * cm, 1.6 * cm)

        self.drawString(2 * cm, 1.1 * cm, "Confidencial • Uso Interno • Gerado pela Skill security-audit")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(19 * cm, 1.1 * cm, page_text)
        self.restoreState()


def generate_charts(data, temp_dir):
    """Gera os gráficos de rosca e barras usando Matplotlib."""
    summary = data.get("summary", {})
    charts = {}

    # 1. Gráfico de Rosca por Severidade
    labels = []
    sizes = []
    chart_colors = []

    mapping = [
        ("Crítica", summary.get("critical", 0), COLOR_CRITICAL),
        ("Alta", summary.get("high", 0), COLOR_HIGH),
        ("Média", summary.get("medium", 0), COLOR_MEDIUM),
        ("Baixa", summary.get("low", 0), COLOR_LOW),
        ("Informativa", summary.get("informative", 0), COLOR_INFORMATIVE),
    ]

    for label, count, color in mapping:
        if count > 0:
            labels.append(f"{label} ({count})")
            sizes.append(count)
            chart_colors.append(color)

    if not sizes:
        labels = ["Nenhum achado"]
        sizes = [1]
        chart_colors = [COLOR_STRENGTH]

    fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=200)
    wedges, texts = ax.pie(
        sizes,
        labels=labels,
        colors=chart_colors,
        startangle=140,
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
        textprops=dict(color="#1E293B", fontsize=8, weight="bold")
    )
    total_findings = summary.get("total", sum(sizes) if sizes != [1] else 0)
    ax.text(
        0, 0, f"{total_findings}\nAchados",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color="#0F172A"
    )
    ax.set_title("Achados por Severidade", fontsize=10, fontweight="bold", pad=10, color="#0F172A")
    plt.tight_layout()
    donut_path = os.path.join(temp_dir, "donut_chart.png")
    fig.savefig(donut_path, transparent=False, facecolor="#FFFFFF")
    plt.close(fig)
    charts["donut"] = donut_path

    # 2. Gráfico de Barras por Categoria
    categories = [
        "Banco sem Tranca",
        "Permissão Navegador",
        "IDOR",
        "Chaves Expostas",
        "Inputs sem Tratamento"
    ]
    
    cat_counts = {c: 0 for c in categories}
    for finding in data.get("findings", []):
        cat = finding.get("category", "")
        if "Banco" in cat:
            cat_counts["Banco sem Tranca"] += 1
        elif "Navegador" in cat or "Permiss" in cat:
            cat_counts["Permissão Navegador"] += 1
        elif "IDOR" in cat:
            cat_counts["IDOR"] += 1
        elif "Chave" in cat:
            cat_counts["Chaves Expostas"] += 1
        elif "Input" in cat or "XSS" in cat:
            cat_counts["Inputs sem Tratamento"] += 1

    fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=200)
    y_pos = range(len(categories))
    counts = [cat_counts[c] for c in categories]
    bar_colors = ["#334155" if c == 0 else "#2563EB" for c in counts]

    bars = ax.barh(y_pos, counts, color=bar_colors, height=0.55, edgecolor="#E2E8F0")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=7.5, color="#334155")
    ax.invert_yaxis()
    ax.set_xlabel("Quantidade de Ocorrências", fontsize=8, color="#64748B")
    ax.set_title("Achados por Categoria", fontsize=10, fontweight="bold", pad=10, color="#0F172A")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.xaxis.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")

    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 0.1, bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                va="center", ha="left", fontsize=8, fontweight="bold", color="#0F172A"
            )

    plt.tight_layout()
    bar_path = os.path.join(temp_dir, "bar_chart.png")
    fig.savefig(bar_path, transparent=False, facecolor="#FFFFFF")
    plt.close(fig)
    charts["bars"] = bar_path

    return charts


def build_pdf(data, output_pdf_path):
    """Constrói o documento PDF A4 estruturado a partir dos dados auditados."""
    output_dir = os.path.dirname(os.path.abspath(output_pdf_path))
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        charts = generate_charts(data, temp_dir)

        # Margens de 2cm = 2 * 28.3465 = 56.69 pt
        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2.2 * cm,
            bottomMargin=2.2 * cm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CoverTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=8
        )

        subtitle_style = ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#475569"),
            spaceAfter=14
        )

        h1_style = ParagraphStyle(
            "Heading1_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=14,
            spaceAfter=8
        )

        h2_style = ParagraphStyle(
            "Heading2_Custom",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "Body_Custom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155")
        )

        code_style = ParagraphStyle(
            "Code_Custom",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#0F172A")
        )

        story = []

        # =========================================================================
        # 1. CAPA EXECUTIVA
        # =========================================================================
        story.append(Spacer(1, 1.5 * cm))
        badge_style = ParagraphStyle(
            "BadgeStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#2563EB")
        )
        story.append(Paragraph("RELATÓRIO DE AUDITORIA DE SEGURANÇA", badge_style))
        story.append(Spacer(1, 0.2 * cm))

        project_name = data.get("project_name", "Projeto")
        story.append(Paragraph(f"Auditoria de Segurança & Código: {project_name}", title_style))
        story.append(Paragraph(f"Data da Auditoria: {data.get('audit_date', 'N/A')} • Escopo: {data.get('scope', 'Repositório Completo')}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=15))

        # Metodologia & Stack Detectada
        story.append(Paragraph("<b>Stack Tecnológica Detectada:</b>", h2_style))
        stack = data.get("detected_stack", {})
        stack_text = (
            f"<b>Linguagem:</b> {stack.get('language', 'N/D')} | "
            f"<b>Framework:</b> {stack.get('framework', 'N/D')} | "
            f"<b>ORM/DB:</b> {stack.get('orm_db', 'N/D')}<br/>"
            f"<b>Auth:</b> {stack.get('auth', 'N/D')} | "
            f"<b>Frontend:</b> {stack.get('frontend', 'N/D')} | "
            f"<b>Deploy/Infra:</b> {stack.get('deploy_infra', 'N/D')}"
        )
        story.append(Paragraph(stack_text, body_style))
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph("<b>Nota Metodológica de Auditoria:</b>", h2_style))
        story.append(Paragraph(data.get("methodology_note", "Auditoria baseada em 5 categorias críticas de vulnerabilidade com checagem factual."), body_style))
        story.append(Spacer(1, 0.6 * cm))

        # =========================================================================
        # 2. RESUMO EXECUTIVO & GRÁFICOS
        # =========================================================================
        story.append(Paragraph("Resumo Executivo", h1_style))
        
        # Cards de métricas
        summary = data.get("summary", {})
        summary_data = [
            [
                Paragraph("<b>Total</b>", body_style),
                Paragraph("<b>Crítica</b>", body_style),
                Paragraph("<b>Alta</b>", body_style),
                Paragraph("<b>Média</b>", body_style),
                Paragraph("<b>Baixa</b>", body_style),
                Paragraph("<b>Informativa</b>", body_style),
            ],
            [
                Paragraph(f"<b>{summary.get('total', 0)}</b>", title_style),
                Paragraph(f"<font color='{COLOR_CRITICAL}'><b>{summary.get('critical', 0)}</b></font>", title_style),
                Paragraph(f"<font color='{COLOR_HIGH}'><b>{summary.get('high', 0)}</b></font>", title_style),
                Paragraph(f"<font color='{COLOR_MEDIUM}'><b>{summary.get('medium', 0)}</b></font>", title_style),
                Paragraph(f"<font color='{COLOR_LOW}'><b>{summary.get('low', 0)}</b></font>", title_style),
                Paragraph(f"<font color='{COLOR_INFORMATIVE}'><b>{summary.get('informative', 0)}</b></font>", title_style),
            ]
        ]
        summary_table = Table(summary_data, colWidths=[2.8 * cm] * 6)
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5 * cm))

        # Gráficos Lado a Lado
        chart_table_data = [
            [Image(charts["donut"], width=8.2 * cm, height=6.2 * cm),
             Image(charts["bars"], width=8.2 * cm, height=6.2 * cm)]
        ]
        chart_table = Table(chart_table_data, colWidths=[8.5 * cm, 8.5 * cm])
        chart_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(chart_table)

        # =========================================================================
        # 3. PONTOS FORTES E RISCOS CENTRAIS
        # =========================================================================
        story.append(PageBreak())
        story.append(Paragraph("Pontos Fortes (Mecanismos Corretos & Protegidos)", h1_style))
        story.append(Paragraph("Evidências de áreas examinadas que apresentaram defesas robustas e isolamento eficaz:", body_style))
        story.append(Spacer(1, 0.2 * cm))

        strengths = data.get("strengths", [])
        if strengths:
            for s in strengths:
                p_text = f"• <font color='{COLOR_STRENGTH}'><b>[PROTEGIDO] {s.get('component', '')}:</b></font> {s.get('description', '')} <i>(Evidência: {s.get('evidence', '')})</i>"
                story.append(Paragraph(p_text, body_style))
                story.append(Spacer(1, 0.15 * cm))
        else:
            story.append(Paragraph("Nenhum mecanismo de defesa destacado formalmente.", body_style))

        story.append(Spacer(1, 0.4 * cm))
        story.append(Paragraph("Riscos Centrais (Pontos Fracos)", h1_style))
        weaknesses = data.get("weaknesses", [])
        if weaknesses:
            for w in weaknesses:
                story.append(Paragraph(f"• <font color='{COLOR_HIGH}'><b>[RISCO]</b></font> {w}", body_style))
                story.append(Spacer(1, 0.15 * cm))
        else:
            story.append(Paragraph("Nenhum risco sistêmico generalizado identificado.", body_style))

        # =========================================================================
        # 4. TABELA DE ACHADOS DETALHADOS
        # =========================================================================
        story.append(Spacer(1, 0.6 * cm))
        story.append(Paragraph("Achados Detalhados por Categoria", h1_style))
        story.append(Paragraph("Varredura linha por linha dos achados verificados no código real:", body_style))
        story.append(Spacer(1, 0.3 * cm))

        findings = data.get("findings", [])
        if findings:
            table_rows = [
                [
                    Paragraph("<b>Sev.</b>", body_style),
                    Paragraph("<b>Arquivo : Linha</b>", body_style),
                    Paragraph("<b>Categoria & Descrição do Problema</b>", body_style),
                ]
            ]
            for f in findings:
                sev = f.get("severity", "Média")
                sev_color = SEVERITY_COLORS.get(sev, COLOR_MEDIUM)
                chip_html = f"<font color='white'><b>&nbsp;{sev.upper()}&nbsp;</b></font>"
                
                desc_html = (
                    f"<b>{f.get('title', '')}</b><br/>"
                    f"<font color='#64748B'>Categoria: {f.get('category', '')}</font><br/>"
                    f"{f.get('description', '')}<br/>"
                    f"<b>Explorabilidade:</b> <i>{f.get('exploitability', 'N/D')}</i><br/>"
                    f"<b>Correção Sugerida:</b> {f.get('mitigation', '')}"
                )

                table_rows.append([
                    Paragraph(chip_html, body_style),
                    Paragraph(f"<code>{f.get('file_line', '')}</code>", code_style),
                    Paragraph(desc_html, body_style)
                ])

            findings_table = Table(table_rows, colWidths=[2.2 * cm, 4.3 * cm, 10.5 * cm])
            t_style = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
            # Estilizar chip de fundo para a coluna de severidade
            for idx, f in enumerate(findings, start=1):
                sev = f.get("severity", "Média")
                sev_color = SEVERITY_COLORS.get(sev, COLOR_MEDIUM)
                t_style.append(("BACKGROUND", (0, idx), (0, idx), colors.HexColor(sev_color)))
                t_style.append(("ALIGN", (0, idx), (0, idx), "CENTER"))

            findings_table.setStyle(TableStyle(t_style))
            story.append(findings_table)
        else:
            story.append(Paragraph("Nenhum achado de segurança registrado.", body_style))

        # =========================================================================
        # 5. RECOMENDAÇÕES PRIORIZADAS
        # =========================================================================
        story.append(PageBreak())
        story.append(Paragraph("Recomendações Priorizadas", h1_style))
        story.append(Paragraph("Plano de mitigação baseado na severidade e complexidade:", body_style))
        story.append(Spacer(1, 0.3 * cm))

        recs = data.get("recommendations", [])
        if recs:
            for r in recs:
                p_text = f"<b>[{r.get('priority', 'P1')}] {r.get('title', '')}</b>: {r.get('action', '')}"
                story.append(Paragraph(p_text, body_style))
                story.append(Spacer(1, 0.2 * cm))

        # Configurar nome do projeto no canvas para o cabeçalho
        def on_first_page(canvas_obj, document):
            canvas_obj.report_project_name = project_name

        def on_later_pages(canvas_obj, document):
            canvas_obj.report_project_name = project_name

        doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=on_first_page, onLaterPages=on_later_pages)
        print(f"[✓] Relatório em PDF gerado com sucesso em: {output_pdf_path}")


def get_sample_data():
    """Retorna dados de exemplo ricos para validação da geração do PDF."""
    return {
        "project_name": "Demo SaaS Platform",
        "audit_date": "2026-11-09",
        "scope": "Backend API, Frontend Next.js e Infraestrutura Docker",
        "detected_stack": {
            "language": "TypeScript / Node.js",
            "framework": "Next.js (App Router) + Express API",
            "orm_db": "Prisma ORM + PostgreSQL",
            "auth": "NextAuth.js (JWT session)",
            "frontend": "React 19 + Tailwind CSS",
            "deploy_infra": "Docker Compose + GitHub Actions"
        },
        "methodology_note": "Varredura focada em isolamento multitenant, RLS/filtros de query, autorização simétrica frontend/backend, prevenção de IDOR, sanitização de segredos e higienização de inputs no DOM e e-mails.",
        "summary": {
            "critical": 1,
            "high": 2,
            "medium": 2,
            "low": 1,
            "informative": 1,
            "total": 7
        },
        "strengths": [
            {
                "component": "Rotas de Faturamento (Billing)",
                "evidence": "src/controllers/billing.controller.ts:45-80",
                "description": "Todas as consultas de invoices validam estritamente o tenantId extraído do token JWT autenticado."
            },
            {
                "component": "Hashing de Senhas",
                "evidence": "src/services/auth.service.ts:18",
                "description": "Utilização correta de bcrypt com salt rounds = 12 em todas as operações de cadastro e redefinição."
            }
        ],
        "weaknesses": [
            "Falta de validação de tenantId no endpoint de exportação de relatórios CSV.",
            "Rota de remoção de usuários sem verificação de role administrativa no backend.",
            "Default de segredo JWT inseguro no docker-compose.yml."
        ],
        "findings": [
            {
                "id": "SEC-001",
                "category": "Banco sem Tranca",
                "severity": "Crítica",
                "title": "Exportação CSV sem filtro de inquilino (Tenant Leak)",
                "file_line": "src/routes/reports.ts:78",
                "code_snippet": "const allUsers = await prisma.user.findMany(); // Sem where: { tenantId }",
                "exploitability": "Qualquer usuário logado pode chamar GET /api/reports/export-all e baixar dados de todos os inquilinos cadastrados.",
                "description": "A query de exportação busca registros sem filtrar pelo tenantId da sessão do usuário autenticado.",
                "mitigation": "Adicionar where: { tenantId: req.user.tenantId } obrigatoriamente."
            },
            {
                "id": "SEC-002",
                "category": "Permissão no Navegador",
                "severity": "Alta",
                "title": "Exclusão de usuário sem verificação de role no backend",
                "file_line": "src/routes/users.ts:142",
                "code_snippet": "app.delete('/api/users/:id', authMiddleware, deleteUserHandler);",
                "exploitability": "O frontend oculta o botão com {user.role === 'admin'}, mas requisição manual via cURL com token comum executa a exclusão com sucesso.",
                "description": "O endpoint de exclusão checa apenas autenticação mas não exige autorização RBAC de administrador.",
                "mitigation": "Inserir middleware requireRole('admin') na definição da rota."
            },
            {
                "id": "SEC-003",
                "category": "IDOR",
                "severity": "Alta",
                "title": "Modificação de perfil de outro usuário por ID",
                "file_line": "src/routes/profile.ts:55",
                "code_snippet": "await prisma.profile.update({ where: { id: req.params.id }, data: req.body });",
                "exploitability": "Usuário A altera o ID na URL para o ID de usuário B e sobrescreve telefone, e-mail e preferências alheias.",
                "description": "O handler de atualização confia no ID passado na rota sem comparar com o ID autenticado na sessão.",
                "mitigation": "Utilizar req.user.id diretamente na cláusula where ou validar if (req.params.id !== req.user.id) return 403."
            },
            {
                "id": "SEC-004",
                "category": "Chaves Expostas",
                "severity": "Média",
                "title": "Fallback de segredo JWT fraco e previsível",
                "file_line": "docker-compose.yml:24",
                "code_snippet": "JWT_SECRET: ${JWT_SECRET:-super-secret-default-key-change-me}",
                "exploitability": "Se o container subir sem .env em produção, qualquer atacante pode forjar tokens JWT válidos.",
                "description": "Variável de ambiente com fallback padrão fraco e ausência de verificação no startup.",
                "mitigation": "Remover o fallback e adicionar verificação em src/index.ts que encerra a aplicação se JWT_SECRET não estiver definido."
            },
            {
                "id": "SEC-005",
                "category": "Inputs sem Tratamento",
                "severity": "Média",
                "title": "Renderização de bio de usuário com dangerouslySetInnerHTML",
                "file_line": "src/components/UserProfile.tsx:64",
                "code_snippet": "<div dangerouslySetInnerHTML={{ __html: user.bio }} />",
                "exploitability": "Injeção de scripts maliciosos através do campo de biografia, executando roubo de sessão de outros visitantes.",
                "description": "Conteúdo vindo de entrada de usuário renderizado no DOM sem sanitização prévia.",
                "mitigation": "Sanitizar o HTML usando DOMPurify.sanitize(user.bio) ou utilizar renderização como texto comum."
            }
        ],
        "recommendations": [
            {
                "priority": "P1",
                "title": "Correção Imediata do Isolamento de Inquilino",
                "action": "Aplicar filtro compulsório de tenantId na rota de exportação CSV e auditar todos os findMany do Prisma.",
                "target_findings": ["SEC-001"]
            },
            {
                "priority": "P2",
                "title": "Alinhamento de Permissões Backend e Proteção IDOR",
                "action": "Implantar requireRole('admin') nas rotas sensíveis e validar posse nos updates por ID.",
                "target_findings": ["SEC-002", "SEC-003"]
            },
            {
                "priority": "P3",
                "title": "Eliminação de Segredos Padrão e Sanitização de DOM",
                "action": "Remover fallback de segredos no docker-compose e aplicar DOMPurify na exibição de bios.",
                "target_findings": ["SEC-004", "SEC-005"]
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="Gerador de Relatório de Auditoria de Segurança em PDF")
    parser.add_argument("--input", "-i", help="Caminho para o arquivo JSON com os dados da auditoria")
    parser.add_argument("--output", "-o", default="docs/security-audit/relatorio-auditoria-seguranca.pdf", help="Caminho do PDF de saída")
    parser.add_argument("--sample", action="store_true", help="Gera o PDF usando dados de exemplo de demonstração")
    args = parser.parse_args()

    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif args.sample or not args.input:
        print("[i] Modo demonstração/amostra ativado. Usando dados de exemplo...")
        data = get_sample_data()

    build_pdf(data, args.output)

if __name__ == "__main__":
    main()

