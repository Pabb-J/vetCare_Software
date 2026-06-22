import docx
from docx.shared import Pt

doc = docx.Document(r'C:\Users\brian\Downloads\Grupo_4_TP2_entrega_4.docx')

print('=== DETAILED PARAGRAPH 2 (index item) ===')
p = doc.paragraphs[2]
print(f'Text: "{p.text[:200]}"')
print(f'Style: {p.style.name}')
print(f'Alignment: {p.alignment}')
print('Runs:')
for ri, r in enumerate(p.runs):
    print(f'  Run {ri}: text="{r.text[:80]}" bold={r.bold} size={r.font.size}')

print()
print('=== PARAGRAPH 2 XML (short) ===')
print(p._p.xml[:3000])
