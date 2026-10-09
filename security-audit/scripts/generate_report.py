#!/usr/bin/env python3
"""Generate the pt-BR security audit PDF from canonical audit-results.json."""
from __future__ import annotations
import argparse, json, os, sys, tempfile, textwrap
from collections import Counter
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Preformatted
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
except ImportError as e:
    raise SystemExit('Missing ReportLab. Use an isolated venv and install requirements-report.txt') from e

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise SystemExit('Missing Matplotlib. Use an isolated venv and install requirements-report.txt') from e

PALETTE={'Critical':'#B91C1C','High':'#EA580C','Medium':'#D97706','Low':'#2563EB','Informational':'#6B7280','Strength':'#059669'}
CAT_LABEL={'tenant-isolation':'Isolamento de tenant/dono','authorization':'Autorização privilegiada','idor-bola':'IDOR / BOLA','secrets':'Segredos expostos','xss':'XSS / renderização insegura'}
SEV_PT={'Critical':'Crítica','High':'Alta','Medium':'Média','Low':'Baixa','Informational':'Informativa'}

MOJIBAKE_TOKENS=(
    'Ã', 'Â', 'â€', 'â€™', 'â€œ', 'â€�', 'â€“', 'â€”', 'â€¢', 'ðŸ', '\ufffd'
)

def _mojibake_score(value: str) -> int:
    """Return a conservative score for common UTF-8 decoded as Latin-1/CP1252."""
    return sum(value.count(token) for token in MOJIBAKE_TOKENS)

def repair_mojibake(value: str) -> str:
    """Repair common UTF-8/Latin-1/CP1252 mojibake only when confidence improves."""
    current=value
    # Two passes also recover common double-encoded text without touching valid pt-BR.
    for _ in range(2):
        base_score=_mojibake_score(current)
        if base_score == 0:
            break
        best=current
        best_score=base_score
        for encoding in ('cp1252','latin-1'):
            try:
                candidate=current.encode(encoding).decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            score=_mojibake_score(candidate)
            if score < best_score:
                best, best_score=candidate, score
        if best == current:
            break
        current=best
    return current

def normalize_text_tree(obj):
    """Normalize all user-facing strings while preserving the JSON structure."""
    repairs=[]
    def walk(value, path='$'):
        if isinstance(value, str):
            fixed=repair_mojibake(value)
            if fixed != value:
                repairs.append(path)
            return fixed
        if isinstance(value, list):
            return [walk(v, f'{path}[{i}]') for i,v in enumerate(value)]
        if isinstance(value, dict):
            return {k: walk(v, f'{path}.{k}') for k,v in value.items()}
        return value
    return walk(obj), repairs

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def first_location(f):
    ev=f.get('evidence') or []
    return ev[0].get('location','') if ev else ''

def build_github_issue(f):
    sev=SEV_PT.get(f.get('severity'),f.get('severity','')).lower()
    evidence='\n\n'.join(f"`{e.get('location','')}`\n\n```text\n{e.get('snippet','')}\n```" for e in f.get('evidence',[]))
    mappings=', '.join(f.get('mappings') or [])
    return f"""# [Segurança] {f.get('title','')}\n\n**Labels sugeridas:** `security`, `{sev}`\n\n## Problema\n\n{f.get('description','')}\n\n**Explorabilidade:** {f.get('exploitability','')}\n\n## Evidência\n\n{evidence}\n\n## Impacto\n\n{f.get('impact','')}\n\n## Sugestão de correção\n\n{f.get('remediation','')}\n\n## Critérios de aceite\n\n- [ ] A causa raiz foi corrigida em todos os caminhos equivalentes.\n- [ ] O cenário não autorizado descrito acima é negado pelo backend/camada confiável.\n- [ ] Teste de regressão implementado: {f.get('regression_test','')}\n- [ ] Fluxos autorizados equivalentes continuam funcionando.\n""" + (f"\n**Mapeamentos:** {mappings}\n" if mappings else '')

def chart_severity(findings, path):
    counts=Counter(f.get('severity','Informational') for f in findings)
    order=[s for s in ['Critical','High','Medium','Low','Informational'] if counts[s]]
    if not order: return False
    vals=[counts[s] for s in order]
    fig,ax=plt.subplots(figsize=(5.2,3.2))
    ax.pie(vals,labels=[f'{SEV_PT[s]} ({counts[s]})' for s in order],colors=[PALETTE[s] for s in order],startangle=90,wedgeprops={'width':0.42,'edgecolor':'white'})
    ax.set_title('Achados por severidade')
    fig.tight_layout(); fig.savefig(path,dpi=170,bbox_inches='tight'); plt.close(fig); return True

def chart_category(findings,path):
    counts=Counter(f.get('category') for f in findings)
    cats=['tenant-isolation','authorization','idor-bola','secrets','xss']
    vals=[counts[c] for c in cats]
    fig,ax=plt.subplots(figsize=(7.2,3.4))
    labels=['Tenant','Autorização','IDOR/BOLA','Segredos','XSS']
    bars=ax.bar(labels,vals)
    ax.set_ylabel('Achados'); ax.set_title('Achados por categoria'); ax.set_ylim(0,max(vals+[1])+1)
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.05,str(v),ha='center',va='bottom',fontsize=9)
    ax.tick_params(axis='x',labelrotation=18); fig.tight_layout(); fig.savefig(path,dpi=170,bbox_inches='tight'); plt.close(fig)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('--output'); args=ap.parse_args()
    inp=Path(args.input).resolve(); data=json.loads(inp.read_text(encoding='utf-8-sig')); data, encoding_repairs=normalize_text_tree(data); out=Path(args.output).resolve() if args.output else inp.with_name('relatorio-auditoria-seguranca.pdf')
    out.parent.mkdir(parents=True,exist_ok=True)
    project=data.get('project',{}).get('name','Projeto'); findings=data.get('findings',[])
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CoverTitle',parent=styles['Title'],fontSize=24,leading=29,spaceAfter=18,textColor=colors.HexColor('#111827')))
    styles.add(ParagraphStyle(name='H1x',parent=styles['Heading1'],fontSize=17,leading=21,spaceBefore=8,spaceAfter=9,textColor=colors.HexColor('#111827')))
    styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontSize=13,leading=17,spaceBefore=8,spaceAfter=6,textColor=colors.HexColor('#1F2937')))
    styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontSize=9.5,leading=13,spaceAfter=6,textColor=colors.HexColor('#1F2937')))
    styles.add(ParagraphStyle(name='Small',parent=styles['BodyText'],fontSize=8,leading=10,textColor=colors.HexColor('#4B5563')))
    styles.add(ParagraphStyle(name='Codex',fontName='Courier',fontSize=7.2,leading=9,leftIndent=8,rightIndent=8,spaceBefore=4,spaceAfter=7,backColor=colors.HexColor('#F3F4F6'),borderPadding=6,wordWrap='CJK'))
    styles.add(ParagraphStyle(name='CenterSmall',parent=styles['Small'],alignment=TA_CENTER))

    title=f'Relatório de Auditoria de Segurança - {project}'
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont('Helvetica',7.5); canvas.setFillColor(colors.HexColor('#6B7280'))
        canvas.drawString(2*cm,1.1*cm,title[:90]); canvas.drawRightString(A4[0]-2*cm,1.1*cm,f'Página {doc.page}')
        canvas.restoreState()

    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=2*cm,leftMargin=2*cm,topMargin=2*cm,bottomMargin=1.8*cm,title=title,author='Security Audit Skill')
    story=[]
    story += [Spacer(1,3.2*cm),Paragraph(esc(title),styles['CoverTitle']),Spacer(1,0.4*cm)]
    p=data.get('project',{}); scope=data.get('scope',{})
    cover=[['Data',p.get('audit_date','')],['Repositório',p.get('repository','') or 'Não informado'],['Escopo auditado','; '.join(scope.get('audited',[])) or 'Conforme repositório analisado'],['Exclusões','; '.join(scope.get('excluded',[])) or 'Nenhuma exclusão registrada']]
    t=Table([[Paragraph(f'<b>{esc(a)}</b>',styles['Bodyx']),Paragraph(esc(b),styles['Bodyx'])] for a,b in cover],colWidths=[3.6*cm,11.7*cm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#F3F4F6')),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#D1D5DB')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])); story += [t,Spacer(1,0.5*cm)]
    if scope.get('methodology_note'): story.append(Paragraph('<b>Nota metodológica.</b> '+esc(scope['methodology_note']),styles['Bodyx']))
    story.append(PageBreak())

    # Executive summary
    story += [Paragraph('1. Resumo executivo',styles['H1x'])]
    counts=Counter(f.get('severity') for f in findings)
    summary='; '.join(f"{SEV_PT[s]}: {counts[s]}" for s in ['Critical','High','Medium','Low','Informational'] if counts[s]) or 'Nenhum achado verificado.'
    story += [Paragraph(f'<b>Total de achados verificados:</b> {len(findings)}. {esc(summary)}',styles['Bodyx'])]
    chart_tmp = None
    if findings:
        chart_tmp = Path(tempfile.mkdtemp(prefix='security-audit-charts-'))
        sev=chart_tmp/'sev.png'; cat=chart_tmp/'cat.png'; chart_severity(findings,sev); chart_category(findings,cat)
        from reportlab.platypus import Image
        story += [Table([[Image(str(sev),width=7.3*cm,height=4.5*cm),Image(str(cat),width=8.5*cm,height=4.1*cm)]],colWidths=[7.6*cm,8.7*cm]),Spacer(1,0.2*cm)]
    else:
        story.append(Paragraph('Não foram identificados achados de segurança verificados dentro do escopo revisado. Isso não equivale a uma garantia de ausência de vulnerabilidades; consulte cobertura e limitações.',styles['Bodyx']))
    if data.get('executive_summary'): story.append(Paragraph(esc(data['executive_summary']),styles['Bodyx']))

    # Stack and coverage
    story += [Paragraph('2. Stack, escopo e cobertura',styles['H1x'])]
    st=data.get('stack',{})
    for key,label in [('languages','Linguagens'),('backend','Backend'),('frontend','Frontend'),('database','Banco'),('data_access','ORM / acesso a dados'),('authentication','Autenticação'),('authorization','Autorização'),('tenant_isolation','Isolamento'),('deployment','Deploy / CI / IaC')]:
        vals=st.get(key,[])
        if vals: story.append(Paragraph(f'<b>{label}:</b> {esc("; ".join(map(str,vals)))}',styles['Bodyx']))
    cov=data.get('coverage',{})
    cov_rows=[['Handlers backend',f"{cov.get('backend_handlers_reviewed',0)} / {cov.get('backend_handlers_discovered',0)} revisados"],['Operações privilegiadas',str(cov.get('privileged_operations',0))],['Handlers com identificadores',str(cov.get('object_id_handlers',0))],['Gates frontend',f"{cov.get('frontend_gates_mapped',0)} / {cov.get('frontend_privilege_gates',0)} mapeados"],['Sinks de renderização revisados',str(cov.get('unsafe_rendering_sinks',0))],['Histórico Git',('revisado' if cov.get('git_history_scanned') else ('disponível, não revisado' if cov.get('git_history_available') else 'indisponível'))],['Arquivos deploy/CI/IaC revisados',str(cov.get('deployment_files_reviewed',0))]]
    ct=Table([[Paragraph(f'<b>{esc(a)}</b>',styles['Small']),Paragraph(esc(b),styles['Small'])] for a,b in cov_rows],colWidths=[6*cm,9.2*cm]); ct.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#D1D5DB')),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#F9FAFB')),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),5)])); story += [ct]
    for n in cov.get('notes',[]): story.append(Paragraph('• '+esc(n),styles['Small']))

    # Strengths/weaknesses
    story += [Paragraph('3. Pontos fortes e pontos fracos',styles['H1x']),Paragraph('Pontos fortes',styles['H2x'])]
    strengths=data.get('strengths',[])
    if not strengths: story.append(Paragraph('Nenhum ponto forte foi registrado explicitamente.',styles['Bodyx']))
    for s in strengths:
        ev='; '.join(s.get('evidence',[])); text=f"<b>{esc(s.get('title',''))}</b> - {esc(s.get('description',''))}" + (f" <font color='#059669'>Evidência: {esc(ev)}</font>" if ev else '')
        story.append(Paragraph(text,styles['Bodyx']))
    story.append(Paragraph('Pontos fracos',styles['H2x']))
    if findings:
        for f in findings[:8]: story.append(Paragraph(f"• <b>{esc(f.get('title',''))}</b> ({SEV_PT.get(f.get('severity'),f.get('severity'))})",styles['Bodyx']))
    else: story.append(Paragraph('Nenhum risco central verificado foi registrado.',styles['Bodyx']))

    # Detailed findings
    story += [Paragraph('4. Achados detalhados',styles['H1x'])]
    if not findings:
        story.append(Paragraph('Nenhum achado verificado.',styles['Bodyx']))
    else:
        for cat in ['tenant-isolation','authorization','idor-bola','secrets','xss']:
            group=[f for f in findings if f.get('category')==cat]
            if not group: continue
            story.append(Paragraph(CAT_LABEL[cat],styles['H2x']))
            rows=[[Paragraph('<b>Severidade</b>',styles['Small']),Paragraph('<b>Arquivo:linha</b>',styles['Small']),Paragraph('<b>Descrição</b>',styles['Small'])]]
            for f in group:
                sev=f.get('severity','Informational')
                rows.append([Paragraph(f"<font color='white'><b>{SEV_PT.get(sev,sev)}</b></font>",styles['CenterSmall']),Paragraph(esc(first_location(f)),styles['Small']),Paragraph(esc(f.get('title','')),styles['Small'])])
            tab=Table(rows,colWidths=[2.5*cm,5.6*cm,7.3*cm],repeatRows=1)
            ts=[('BACKGROUND',(0,0),(-1,0),colors.HexColor('#111827')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#D1D5DB')),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),5)]
            for idx,f in enumerate(group,1): ts.append(('BACKGROUND',(0,idx),(0,idx),colors.HexColor(PALETTE.get(f.get('severity'),'#6B7280'))))
            tab.setStyle(TableStyle(ts)); story += [tab,Spacer(1,0.2*cm)]
            for f in group:
                elems=[Paragraph(f"<b>{esc(f.get('id',''))} - {esc(f.get('title',''))}</b>",styles['H2x']),Paragraph(esc(f.get('description','')),styles['Bodyx']),Paragraph('<b>Explorabilidade:</b> '+esc(f.get('exploitability','')),styles['Bodyx']),Paragraph('<b>Impacto:</b> '+esc(f.get('impact','')),styles['Bodyx'])]
                for e in f.get('evidence',[]):
                    elems.append(Paragraph('<b>Evidência:</b> '+esc(e.get('location','')),styles['Small'])); elems.append(Paragraph(esc(e.get('snippet','')).replace('\n','<br/>'),styles['Codex']))
                elems += [Paragraph('<b>Correção recomendada:</b> '+esc(f.get('remediation','')),styles['Bodyx']),Paragraph('<b>Teste de regressão:</b> '+esc(f.get('regression_test','')),styles['Bodyx'])]
                if f.get('mappings'): elems.append(Paragraph('<b>Mapeamentos:</b> '+esc(', '.join(f['mappings'])),styles['Small']))
                story.append(KeepTogether(elems[:4])); story.extend(elems[4:]); story.append(Spacer(1,0.15*cm))

    # Recommendations
    story += [Paragraph('5. Recomendações priorizadas',styles['H1x'])]
    recs=data.get('recommendations',[])
    if not recs: story.append(Paragraph('Nenhuma recomendação adicional registrada.',styles['Bodyx']))
    for r in recs: story.append(Paragraph(f"<b>{esc(r.get('priority',''))} - {esc(r.get('title',''))}</b>: {esc(r.get('description',''))}",styles['Bodyx']))

    # limitations
    story += [Paragraph('6. Limitações e acompanhamento manual',styles['H1x'])]
    lim=data.get('limitations',[])
    if not lim: story.append(Paragraph('Nenhuma limitação material registrada.',styles['Bodyx']))
    for x in lim: story.append(Paragraph('• '+esc(x),styles['Bodyx']))

    # GitHub issues
    story += [PageBreak(),Paragraph('ISSUES PARA O GITHUB',styles['H1x'])]
    issues=data.get('github_issues') or []
    if not issues and findings:
        issues=[{'title':f"[Segurança] {f.get('title','')}",'labels':['security',SEV_PT.get(f.get('severity'),f.get('severity','')).lower()],'body':build_github_issue(f),'finding_ids':[f.get('id')]} for f in findings]
    if not issues: story.append(Paragraph('Nenhuma issue acionável gerada porque não há achados verificados.',styles['Bodyx']))
    for i,issue in enumerate(issues,1):
        block=f"--- ISSUE {i} ---\n\n{issue.get('body','')}\n--- FIM ISSUE {i} ---"
        story.append(Paragraph(esc(block).replace('\n','<br/>'),styles['Codex']))

    try:
        doc.build(story,onFirstPage=footer,onLaterPages=footer)
    finally:
        if chart_tmp is not None:
            import shutil
            shutil.rmtree(chart_tmp, ignore_errors=True)
    if encoding_repairs:
        print(f'WARNING: repaired likely UTF-8 mojibake in {len(encoding_repairs)} field(s): '+', '.join(encoding_repairs[:8])+(' ...' if len(encoding_repairs)>8 else ''), file=sys.stderr)
    print(out)
if __name__=='__main__': main()
