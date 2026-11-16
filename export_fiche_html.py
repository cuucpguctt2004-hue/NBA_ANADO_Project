"""
Générateur de rendu HTML/PDF pour la Fiche Intermédiaire ANDO
Produit un document académique soigné, prêt à être imprimé ou exporté en PDF.
"""

import os
import base64
import re

PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(PROJET_DIR, "FICHE_INTERMEDIAIRE.md")
HTML_PATH = os.path.join(PROJET_DIR, "FICHE_INTERMEDIAIRE.html")

def image_to_base64(img_path):
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def main():
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Images à convertir en base64
    img_files = {
        "./eda_correlation_heatmap.png": os.path.join(PROJET_DIR, "eda_correlation_heatmap.png"),
        "./eda_3pt_by_position.png": os.path.join(PROJET_DIR, "eda_3pt_by_position.png"),
        "./eda_ts_vs_usg.png": os.path.join(PROJET_DIR, "eda_ts_vs_usg.png"),
    }

    b64_map = {}
    for rel_path, abs_path in img_files.items():
        if os.path.exists(abs_path):
            b64_map[rel_path] = image_to_base64(abs_path)
            print(f"Image encodée : {rel_path}")

    # CSS de style publication / article scientifique
    css = """
    @page {
        size: A4;
        margin: 1.8cm 1.8cm 1.8cm 1.8cm;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #222;
        line-height: 1.5;
        font-size: 11pt;
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    h1 {
        font-size: 18pt;
        color: #0b2545;
        border-bottom: 2px solid #0b2545;
        padding-bottom: 6px;
        margin-top: 0;
        text-align: center;
    }
    h2 {
        font-size: 13.5pt;
        color: #134074;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
        margin-top: 24px;
        page-break-after: avoid;
    }
    h3 {
        font-size: 11.5pt;
        color: #1d3557;
        margin-top: 14px;
        page-break-after: avoid;
    }
    blockquote {
        background-color: #f1f5f9;
        border-left: 4px solid #1d3557;
        margin: 12px 0;
        padding: 8px 14px;
        font-style: italic;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 9.5pt;
    }
    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 9px;
        text-align: left;
    }
    th {
        background-color: #f8fafc;
        font-weight: 600;
        color: #0f172a;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    img {
        max-width: 85%;
        display: block;
        margin: 12px auto;
        border-radius: 4px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    }
    .figure-caption {
        text-align: center;
        font-size: 9pt;
        color: #64748b;
        font-style: italic;
        margin-bottom: 15px;
    }
    .header-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 18px;
        margin-bottom: 20px;
        font-size: 10pt;
    }
    .page-break {
        page-break-before: always;
    }
    code {
        background: #f1f5f9;
        padding: 2px 5px;
        border-radius: 3px;
        font-family: Consolas, monospace;
        font-size: 9.5pt;
    }
    """

    # Conversion Markdown vers HTML via markdown-it-py (installé) ou parseur direct
    try:
        from markdown_it import MarkdownIt
        md = MarkdownIt('gfm-like')
        html_body = md.render(md_content)
    except Exception:
        # Parseur de secours
        lines = md_content.split('\n')
        in_table = False
        html_lines = []
        for line in lines:
            line_str = line.strip()
            if line_str.startswith('# '):
                html_lines.append(f"<h1>{line_str[2:]}</h1>")
            elif line_str.startswith('## '):
                html_lines.append(f"<h2>{line_str[3:]}</h2>")
            elif line_str.startswith('### '):
                html_lines.append(f"<h3>{line_str[4:]}</h3>")
            elif line_str.startswith('> '):
                html_lines.append(f"<blockquote>{line_str[2:]}</blockquote>")
            elif line_str.startswith('!['):
                match = re.search(r'!\[(.*?)\]\((.*?)\)', line_str)
                if match:
                    alt, src = match.groups()
                    b64_src = b64_map.get(src, src)
                    html_lines.append(f'<img src="{b64_src}" alt="{alt}" />')
            elif line_str.startswith('*Figure'):
                html_lines.append(f'<div class="figure-caption">{line_str}</div>')
            elif line_str.startswith('|'):
                if not in_table:
                    html_lines.append("<table>")
                    in_table = True
                cells = [c.strip() for c in line_str.split('|')[1:-1]]
                if all(set(c).issubset({'-', ':', ' '}) for c in cells):
                    continue
                tag = "th" if html_lines[-1] == "<table>" else "td"
                row_html = "".join([f"<{tag}>{c}</{tag}>" for c in cells])
                html_lines.append(f"<tr>{row_html}</tr>")
            else:
                if in_table:
                    html_lines.append("</table>")
                    in_table = False
                if line_str == "":
                    continue
                elif line_str.startswith('- '):
                    html_lines.append(f"<li>{line_str[2:]}</li>")
                else:
                    html_lines.append(f"<p>{line_str}</p>")
        if in_table:
            html_lines.append("</table>")
        html_body = "\n".join(html_lines)

    # Remplacement des chemins d'images par le base64 si pas déjà fait
    for rel_path, b64_data in b64_map.items():
        html_body = html_body.replace(f'src="{rel_path}"', f'src="{b64_data}"')
        html_body = html_body.replace(f'src="{rel_path[2:]}"', f'src="{b64_data}"')

    final_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Fiche Intermédiaire - Projet ANDO 2026</title>
    <style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\nDocument HTML prêt : {HTML_PATH}")
    print("Pour exporter en PDF : ouvrir ce fichier dans Chrome/Edge puis faire Ctrl+P > Enregistrer au format PDF.")

if __name__ == "__main__":
    main()
