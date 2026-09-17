"""
Модул за конвертиране на Markdown (.md) документи в Word (.docx) и PDF (.pdf) формати.
Поддържа форматиране на заглавия, списъци, таблици, блокове с код, цитати и пълна кирилица.
"""

import io
import os
import re
from typing import Optional, Tuple, Union

import markdown
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf.document import pisaDocument
from xhtml2pdf.files import ResourceAccessPolicy


# ----------------------------------------------------------------------
# Помощни функции за шрифтове (PDF)
# ----------------------------------------------------------------------

def _get_pdf_fonts():
    """
    Връща набор от шрифтове с пълна поддръжка на кирилица.
    Приоритет:
    1. Вградени в проекта шрифтове DejaVu Sans (в irida_app/main/fonts)
    2. Системни шрифтове в Linux / cPanel / Ubuntu / CentOS / CloudLinux
    3. Системни шрифтове в Windows
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_fonts_dir = os.path.join(base_dir, 'fonts')

    # 1. Проверка за вградени в проекта шрифтове
    bundled_reg = os.path.join(bundled_fonts_dir, 'DejaVuSans.ttf')
    if os.path.exists(bundled_reg):
        bundled_bold = os.path.join(bundled_fonts_dir, 'DejaVuSans-Bold.ttf')
        bundled_it = os.path.join(bundled_fonts_dir, 'DejaVuSans-Oblique.ttf')
        bundled_bi = os.path.join(bundled_fonts_dir, 'DejaVuSans-BoldOblique.ttf')
        mono_reg = os.path.join(bundled_fonts_dir, 'DejaVuSansMono.ttf')
        mono_bold = os.path.join(bundled_fonts_dir, 'DejaVuSansMono-Bold.ttf')

        return {
            'family': 'DejaVuSans',
            'regular': bundled_reg.replace('\\', '/'),
            'bold': bundled_bold.replace('\\', '/') if os.path.exists(bundled_bold) else bundled_reg.replace('\\', '/'),
            'italic': bundled_it.replace('\\', '/') if os.path.exists(bundled_it) else bundled_reg.replace('\\', '/'),
            'bold_italic': bundled_bi.replace('\\', '/') if os.path.exists(bundled_bi) else bundled_reg.replace('\\', '/'),
            'mono_family': 'DejaVuSansMono' if os.path.exists(mono_reg) else 'DejaVuSans',
            'mono_regular': mono_reg.replace('\\', '/') if os.path.exists(mono_reg) else bundled_reg.replace('\\', '/'),
            'mono_bold': mono_bold.replace('\\', '/') if os.path.exists(mono_bold) else bundled_bold.replace('\\', '/'),
        }

    # 2. Системни шрифтове (Linux, Windows, macOS)
    candidates = [
        # Linux (CentOS / RHEL / CloudLinux / cPanel)
        (
            'DejaVuSans',
            '/usr/share/fonts/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf',
            '/usr/share/fonts/dejavu/DejaVuSans-BoldOblique.ttf'
        ),
        (
            'DejaVuSans',
            '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf',
            '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Oblique.ttf',
            '/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-BoldOblique.ttf'
        ),
        # Linux (Ubuntu / Debian)
        (
            'DejaVuSans',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'
        ),
        # Liberation Sans (Linux)
        (
            'LiberationSans',
            '/usr/share/fonts/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/liberation/LiberationSans-Bold.ttf',
            '/usr/share/fonts/liberation/LiberationSans-Italic.ttf',
            '/usr/share/fonts/liberation/LiberationSans-BoldItalic.ttf'
        ),
        (
            'LiberationSans',
            '/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf',
            '/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf',
            '/usr/share/fonts/liberation-sans/LiberationSans-Italic.ttf',
            '/usr/share/fonts/liberation-sans/LiberationSans-BoldItalic.ttf'
        ),
        (
            'LiberationSans',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf'
        ),
        # Windows Fonts
        (
            'Arial',
            'C:/Windows/Fonts/arial.ttf',
            'C:/Windows/Fonts/arialbd.ttf',
            'C:/Windows/Fonts/ariali.ttf',
            'C:/Windows/Fonts/arialbi.ttf'
        ),
        (
            'Calibri',
            'C:/Windows/Fonts/calibri.ttf',
            'C:/Windows/Fonts/calibrib.ttf',
            'C:/Windows/Fonts/calibrii.ttf',
            'C:/Windows/Fonts/calibriz.ttf'
        ),
    ]

    for family, reg, bold, it, bi in candidates:
        if os.path.exists(reg):
            return {
                'family': family,
                'regular': reg.replace('\\', '/'),
                'bold': bold.replace('\\', '/') if os.path.exists(bold) else reg.replace('\\', '/'),
                'italic': it.replace('\\', '/') if os.path.exists(it) else reg.replace('\\', '/'),
                'bold_italic': bi.replace('\\', '/') if os.path.exists(bi) else reg.replace('\\', '/'),
                'mono_family': family,
                'mono_regular': reg.replace('\\', '/'),
                'mono_bold': bold.replace('\\', '/') if os.path.exists(bold) else reg.replace('\\', '/'),
            }

    return None


def _register_reportlab_fonts(fonts_info):
    """Регистрира откритите шрифтове в ReportLab енджина за гарантирано разпознаване на кирилица."""
    if not fonts_info:
        return

    try:
        family = fonts_info['family']
        reg_name = family
        bold_name = f"{family}-Bold"
        it_name = f"{family}-Italic"
        bi_name = f"{family}-BoldItalic"

        registered = pdfmetrics.getRegisteredFontNames()

        if reg_name not in registered:
            pdfmetrics.registerFont(TTFont(reg_name, fonts_info['regular']))
        if bold_name not in registered:
            pdfmetrics.registerFont(TTFont(bold_name, fonts_info['bold']))
        if it_name not in registered:
            pdfmetrics.registerFont(TTFont(it_name, fonts_info['italic']))
        if bi_name not in registered:
            pdfmetrics.registerFont(TTFont(bi_name, fonts_info['bold_italic']))

        pdfmetrics.registerFontFamily(
            family,
            normal=reg_name,
            bold=bold_name,
            italic=it_name,
            boldItalic=bi_name
        )

        mono_family = fonts_info.get('mono_family')
        if mono_family and mono_family != family:
            mono_reg_name = mono_family
            mono_bold_name = f"{mono_family}-Bold"
            if mono_reg_name not in registered:
                pdfmetrics.registerFont(TTFont(mono_reg_name, fonts_info['mono_regular']))
            if mono_bold_name not in registered:
                pdfmetrics.registerFont(TTFont(mono_bold_name, fonts_info['mono_bold']))
            pdfmetrics.registerFontFamily(
                mono_family,
                normal=mono_reg_name,
                bold=mono_bold_name,
                italic=mono_reg_name,
                boldItalic=mono_bold_name
            )
    except Exception:
        # Пропускаме, ако шрифтът вече е регистриран или възникне проблем при регистрацията
        pass


# ----------------------------------------------------------------------
# DOCX Helper Styling
# ----------------------------------------------------------------------

def _set_cell_background(cell, fill_hex: str):
    """Задава цвят на фона на клетка от таблица в docx."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Задава отстъпи вътре в клетката (в dxa, 1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def _add_inline_formatted_text(paragraph, text: str, default_color=None, default_size=11):
    """
    Парсва инлайн Markdown форматиране (bold, italic, code, link) и добавя runs към параграфа.
    """
    # Regex токенизатор за inline Markdown
    pattern = re.compile(
        r'(\*\*\*[^*]+\*\*\*|___[^_]+___|'  # Bold Italic
        r'\*\*[^*]+\*\*|__[^_]+__|'          # Bold
        r'\*[^*]+\*|_[^_]+_|'                # Italic
        r'`[^`]+`|'                          # Inline Code
        r'\[([^\]]+)\]\(([^)]+)\)|'          # Links [text](url)
        r'~~[^~]+~~)'                        # Strikethrough
    )

    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            plain = text[last_end:start]
            run = paragraph.add_run(plain)
            run.font.name = 'Calibri'
            run.font.size = Pt(default_size)
            if default_color:
                run.font.color.rgb = default_color

        token = match.group(0)
        link_text = match.group(2)
        link_url = match.group(3)

        if token.startswith('***') and token.endswith('***'):
            inner = token[3:-3]
            run = paragraph.add_run(inner)
            run.bold = True
            run.italic = True
        elif token.startswith('___') and token.endswith('___'):
            inner = token[3:-3]
            run = paragraph.add_run(inner)
            run.bold = True
            run.italic = True
        elif (token.startswith('**') and token.endswith('**')) or (token.startswith('__') and token.endswith('__')):
            inner = token[2:-2]
            run = paragraph.add_run(inner)
            run.bold = True
        elif (token.startswith('*') and token.endswith('*')) or (token.startswith('_') and token.endswith('_')):
            inner = token[1:-1]
            run = paragraph.add_run(inner)
            run.italic = True
        elif token.startswith('`') and token.endswith('`'):
            inner = token[1:-1]
            run = paragraph.add_run(inner)
            run.font.name = 'Consolas'
            run.font.size = Pt(default_size - 1)
            run.font.color.rgb = RGBColor(180, 40, 40)
        elif token.startswith('~~') and token.endswith('~~'):
            inner = token[2:-2]
            run = paragraph.add_run(inner)
            run.font.strike = True
        elif link_text and link_url:
            run = paragraph.add_run(f'{link_text} ({link_url})')
            run.font.color.rgb = RGBColor(37, 99, 235)
            run.underline = True
        else:
            run = paragraph.add_run(token)

        run.font.name = run.font.name or 'Calibri'
        run.font.size = run.font.size or Pt(default_size)
        if default_color and not run.font.color.rgb:
            run.font.color.rgb = default_color

        last_end = end

    if last_end < len(text):
        plain = text[last_end:]
        run = paragraph.add_run(plain)
        run.font.name = 'Calibri'
        run.font.size = Pt(default_size)
        if default_color:
            run.font.color.rgb = default_color


# ----------------------------------------------------------------------
# Конвертиране: Markdown -> DOCX
# ----------------------------------------------------------------------

def markdown_to_docx(md_content: str, title: str = '') -> bytes:
    """
    Преобразува Markdown текст в Microsoft Word (.docx) документ.
    """
    doc = Document()

    # Задаване на полета (margins)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Настройка на базовия стил
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(34, 34, 34)

    lines = md_content.replace('\r\n', '\n').split('\n')
    i = 0
    n = len(lines)

    in_code_block = False
    code_lines = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 1. Блокове с код (```)
        if stripped.startswith('```'):
            if in_code_block:
                # Край на кодов блок
                code_text = '\n'.join(code_lines)
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.3)
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15
                run = p.add_run(code_text)
                run.font.name = 'Consolas'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(40, 50, 70)
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Празна линия
        if not stripped:
            i += 1
            continue

        # 2. Хоризонтална разделителна линия (---, ***, ___)
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run('—' * 45)
            run.font.color.rgb = RGBColor(200, 205, 215)
            i += 1
            continue

        # 3. Заглавия (#, ##, ###, ####, #####)
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            p = doc.add_paragraph()
            if level == 1:
                p.paragraph_format.space_before = Pt(14)
                p.paragraph_format.space_after = Pt(6)
                _add_inline_formatted_text(p, heading_text, default_color=RGBColor(30, 58, 138), default_size=18)
                for run in p.runs:
                    run.bold = True
            elif level == 2:
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(4)
                _add_inline_formatted_text(p, heading_text, default_color=RGBColor(37, 99, 235), default_size=14)
                for run in p.runs:
                    run.bold = True
            elif level == 3:
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(3)
                _add_inline_formatted_text(p, heading_text, default_color=RGBColor(55, 65, 81), default_size=12)
                for run in p.runs:
                    run.bold = True
            else:
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                _add_inline_formatted_text(p, heading_text, default_color=RGBColor(75, 85, 99), default_size=11)
                for run in p.runs:
                    run.bold = True

            i += 1
            continue

        # 4. Цитати (> ...)
        if stripped.startswith('>'):
            quote_text = re.sub(r'^>\s*', '', line).strip()
            # Прочитане на евентуални следващи редове от цитата
            while i + 1 < n and lines[i + 1].strip().startswith('>'):
                i += 1
                quote_text += ' ' + re.sub(r'^>\s*', '', lines[i]).strip()

            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            _add_inline_formatted_text(p, quote_text, default_color=RGBColor(75, 85, 99), default_size=10.5)
            for run in p.runs:
                run.italic = True
            i += 1
            continue

        # 5. Таблици (| Col 1 | Col 2 |)
        if stripped.startswith('|') and '|' in stripped[1:]:
            table_lines = []
            while i < n and lines[i].strip().startswith('|') and '|' in lines[i].strip()[1:]:
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 2:
                # Проверка за разделителен ред (|---|---|)
                header_raw = table_lines[0]
                has_divider = re.match(r'^\|?\s*:?-+:?\s*(\|?\s*:?-+:?\s*)+\|?$', table_lines[1])
                data_start_idx = 2 if has_divider else 1

                def parse_table_row(r_text):
                    r_text = r_text.strip()
                    if r_text.startswith('|'):
                        r_text = r_text[1:]
                    if r_text.endswith('|'):
                        r_text = r_text[:-1]
                    return [c.strip() for c in r_text.split('|')]

                header_cells = parse_table_row(header_raw)
                num_cols = max(len(header_cells), 1)

                table = doc.add_table(rows=0, cols=num_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                table.autofit = True

                # Заглавен ред
                hdr_row = table.add_row()
                for c_idx, h_text in enumerate(header_cells):
                    if c_idx < num_cols:
                        cell = hdr_row.cells[c_idx]
                        _set_cell_background(cell, 'EBF3FA')
                        _set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
                        p = cell.paragraphs[0]
                        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        _add_inline_formatted_text(p, h_text, default_color=RGBColor(30, 58, 138), default_size=10)
                        for r in p.runs:
                            r.bold = True

                # Редове с данни
                for row_idx, r_text in enumerate(table_lines[data_start_idx:]):
                    row_cells_data = parse_table_row(r_text)
                    row_elm = table.add_row()
                    bg_color = 'F8FAFC' if row_idx % 2 == 1 else 'FFFFFF'
                    for c_idx in range(num_cols):
                        c_text = row_cells_data[c_idx] if c_idx < len(row_cells_data) else ''
                        cell = row_elm.cells[c_idx]
                        if bg_color != 'FFFFFF':
                            _set_cell_background(cell, bg_color)
                        _set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                        p = cell.paragraphs[0]
                        _add_inline_formatted_text(p, c_text, default_size=10)

                # Добавяне на малко разстояние след таблицата
                spacer = doc.add_paragraph()
                spacer.paragraph_format.space_before = Pt(2)
                spacer.paragraph_format.space_after = Pt(4)
                continue
            else:
                # Единствен ред с пайпове - третира се като обикновен текст
                p = doc.add_paragraph()
                _add_inline_formatted_text(p, table_lines[0])
                continue

        # 6. Списъци (неподредени: -, *, +)
        bullet_match = re.match(r'^(\s*)[-*+]\s+(.*)$', line)
        if bullet_match:
            indent_spaces = len(bullet_match.group(1))
            bullet_text = bullet_match.group(2)
            p = doc.add_paragraph(style='List Bullet')
            if indent_spaces >= 2:
                p.paragraph_format.left_indent = Inches(0.25 * (indent_spaces // 2 + 1))
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            _add_inline_formatted_text(p, bullet_text)
            i += 1
            continue

        # 7. Списъци (номерирани: 1., 2.)
        number_match = re.match(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if number_match:
            indent_spaces = len(number_match.group(1))
            num_val = number_match.group(2)
            item_text = number_match.group(3)
            p = doc.add_paragraph(style='List Number')
            if indent_spaces >= 2:
                p.paragraph_format.left_indent = Inches(0.25 * (indent_spaces // 2 + 1))
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            _add_inline_formatted_text(p, item_text)
            i += 1
            continue

        # 8. Стандартен параграф
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        _add_inline_formatted_text(p, stripped)
        i += 1

    # Запис във воден бинарен поток
    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()


# ----------------------------------------------------------------------
# Конвертиране: Markdown -> PDF
# ----------------------------------------------------------------------

def markdown_to_pdf(md_content: str, title: str = '') -> bytes:
    """
    Преобразува Markdown текст в PDF документ с отлична кирилица и стилизиране.
    """
    # 1. Преобразуване на Markdown към HTML чрез markdown ��иблиотеката
    html_body = markdown.markdown(
        md_content,
        extensions=[
            'extra',
            'tables',
            'fenced_code',
            'nl2br',
            'sane_lists',
            'toc',
        ]
    )

    # 2. Откриване на шрифтове с кирилица и регистрация в ReportLab
    fonts_info = _get_pdf_fonts()
    font_css = ''
    font_family = 'sans-serif'
    mono_font_family = 'monospace'

    if fonts_info:
        _register_reportlab_fonts(fonts_info)
        font_family = fonts_info['family']
        mono_font_family = fonts_info.get('mono_family', font_family)

        font_css = f"""
        @font-face {{
            font-family: {font_family};
            src: url('{fonts_info["regular"]}');
        }}
        @font-face {{
            font-family: {font_family};
            src: url('{fonts_info["bold"]}');
            font-weight: bold;
        }}
        @font-face {{
            font-family: {font_family};
            src: url('{fonts_info["italic"]}');
            font-style: italic;
        }}
        @font-face {{
            font-family: {font_family};
            src: url('{fonts_info["bold_italic"]}');
            font-weight: bold;
            font-style: italic;
        }}
        """

        if mono_font_family != font_family and 'mono_regular' in fonts_info:
            font_css += f"""
            @font-face {{
                font-family: {mono_font_family};
                src: url('{fonts_info["mono_regular"]}');
            }}
            @font-face {{
                font-family: {mono_font_family};
                src: url('{fonts_info["mono_bold"]}');
                font-weight: bold;
            }}
            """

    doc_title = title or 'Учебен материал'

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{doc_title}</title>
    <style>
        {font_css}

        @page {{
            size: a4 portrait;
            margin: 1.8cm 1.5cm 1.8cm 1.5cm;
        }}

        * {{
            font-family: {font_family};
        }}

        html, body, p, div, span, h1, h2, h3, h4, h5, h6, th, td, li, strong, em, b, i, a, blockquote {{
            font-family: {font_family};
        }}

        body {{
            font-size: 10.5pt;
            line-height: 1.45;
            color: #1e293b;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-weight: bold;
            color: #0f172a;
        }}

        h1 {{
            font-size: 18pt;
            color: #1e3a8a;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 4px;
            margin-top: 14pt;
            margin-bottom: 8pt;
        }}

        h2 {{
            font-size: 13.5pt;
            color: #2563eb;
            margin-top: 12pt;
            margin-bottom: 6pt;
        }}

        h3 {{
            font-size: 11.5pt;
            color: #334155;
            margin-top: 10pt;
            margin-bottom: 4pt;
        }}

        h4 {{
            font-size: 10.5pt;
            color: #475569;
            margin-top: 8pt;
            margin-bottom: 3pt;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 6pt;
            text-align: justify;
        }}

        blockquote {{
            border-left: 3px solid #3b82f6;
            background-color: #f8fafc;
            padding: 6px 12px;
            margin: 8pt 0;
            color: #475569;
        }}

        pre, code, kbd, samp, tt {{
            font-family: {mono_font_family};
            font-size: 9pt;
        }}

        code {{
            background-color: #f1f5f9;
            color: #b91c1c;
            padding: 1px 4px;
        }}

        pre {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 8px 12px;
            margin: 8pt 0;
            white-space: pre-wrap;
        }}

        pre code {{
            background: none;
            color: #1e293b;
            padding: 0;
        }}

        table {{
            width: 100%;
            margin: 10pt 0;
            font-size: 9.5pt;
        }}

        th, td {{
            border: 1px solid #cbd5e1;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background-color: #ebf3fa;
            color: #1e3a8a;
            font-weight: bold;
        }}

        tr:nth-child(even) td {{
            background-color: #f8fafc;
        }}

        ul, ol {{
            margin-top: 2pt;
            margin-bottom: 6pt;
            padding-left: 18pt;
        }}

        li {{
            margin-bottom: 2pt;
        }}

        hr {{
            border: 0;
            border-top: 1px solid #cbd5e1;
            margin: 12pt 0;
        }}

        a {{
            color: #2563eb;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    policy = ResourceAccessPolicy(allow_local_outside_base=True)
    output = io.BytesIO()
    pisa_status = pisaDocument(
        src=full_html,
        dest=output,
        encoding='utf-8',
        resource_policy=policy
    )

    if pisa_status.err:
        raise RuntimeError(f'Грешка при генериране на PDF: {pisa_status.err}')

    return output.getvalue()


# ----------------------------------------------------------------------
# Унифицирана функция за конвертиране на прикачен файл
# ----------------------------------------------------------------------

def convert_markdown_file(
    file_content: Union[bytes, str],
    target_format: str,
    original_filename: str = ''
) -> Tuple[bytes, str, str]:
    """
    Конвертира Markdown съдържание към желания формат (docx, pdf или оставя като md).
    
    Връща tuple: (converted_bytes, new_filename, content_type)
    """
    if isinstance(file_content, bytes):
        try:
            md_text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            md_text = file_content.decode('utf-8-sig', errors='replace')
    else:
        md_text = str(file_content)

    base_name, _ = os.path.splitext(original_filename or 'document.md')
    target = (target_format or '').strip().lower()

    if target == 'docx':
        out_bytes = markdown_to_docx(md_text, title=base_name)
        new_filename = f'{base_name}.docx'
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        return out_bytes, new_filename, content_type

    elif target == 'pdf':
        out_bytes = markdown_to_pdf(md_text, title=base_name)
        new_filename = f'{base_name}.pdf'
        content_type = 'application/pdf'
        return out_bytes, new_filename, content_type

    else:
        # Оригинален markdown формат
        out_bytes = md_text.encode('utf-8')
        new_filename = f'{base_name}.md'
        content_type = 'text/markdown'
        return out_bytes, new_filename, content_type
