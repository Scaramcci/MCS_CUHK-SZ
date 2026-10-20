#!/usr/bin/env python3
"""Convert the preserved Markdown edition into editable LaTeX chapters."""
from pathlib import Path
import json,re,subprocess,zipfile,hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent
(ROOT/'chapters').mkdir(exist_ok=True)
(ROOT/'assets').mkdir(exist_ok=True)
(ROOT/'figures').mkdir(exist_ok=True)
repo=SRC.parents[2]
with zipfile.ZipFile(repo/'templates/latex/报告模板.zip') as z:
 (ROOT/'assets/CUHK_Logo.png').write_bytes(z.read('assets/CUHK_Logo.png'))

def esc(s):
 return ''.join({'\\':r'\textbackslash{}','{':r'\{','}':r'\}','_':r'\_','%':r'\%','&':r'\&','#':r'\#','$':r'\$','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in s)
SYMS={'σ':r'\sigma','π':r'\pi','ρ':r'\rho','γ':r'\gamma','⋈':r'\bowtie','÷':r'\div','∀':r'\forall','∃':r'\exists','∈':r'\in','∉':r'\notin','⊆':r'\subseteq','⊂':r'\subset','∪':r'\cup','∩':r'\cap','∧':r'\land','∨':r'\lor','¬':r'\neg','≠':r'\ne','∅':r'\varnothing','≤':r'\le','≥':r'\ge','×':r'\times','→':r'\rightarrow','←':r'\leftarrow','⇒':r'\Longrightarrow','−':'-','θ':r'\theta','…':r'\ldots'}
MATHCHARS='σπργ⋈÷∀∃∈⊆∪∩∧∨≠∅θ'
def math(s,group=False):
 out=[];i=0
 while i<len(s):
  c=s[i]
  if c=="'":
   j=s.find("'",i+1)
   if j!=-1:out.append(r'\texttt{'+esc(s[i:j+1])+'}');i=j+1;continue
  if c=='_' and i+1<len(s):
   if s[i+1]=='{':
    depth=1;j=i+2
    while j<len(s) and depth:
     depth+=(s[j]=='{')-(s[j]=='}');j+=1
    out.append('_{'+math(s[i+2:j-1],True)+'}');i=j;continue
   m=re.match(r'[A-Za-z0-9]+',s[i+1:])
   if m:out.append('_{'+math(m.group())+'}');i+=1+len(m.group());continue
  m=re.match(r'[A-Za-z][A-Za-z0-9_]*',s[i:])
  if m:
   t=m.group();out.append(t if len(t)==1 else (r'\operatorname{'+t+'}' if t in ['COUNT','AVG','SUM','MIN','MAX'] else r'\mathsf{'+esc(t)+'}'));i+=len(t);continue
  m=re.match(r'[0-9]+(?:\.[0-9]+)?',s[i:])
  if m:out.append(m.group());i+=len(m.group());continue
  if c in SYMS:out.append(SYMS[c]+' ')
  elif c in '{}':out.append('\\'+c)
  elif c=='&':out.append(r'\&')
  elif c=='%':out.append(r'\%')
  elif c==' ':out.append(r'\,')
  elif ord(c)>127 and c not in SYMS:out.append(r'\text{'+esc(c)+'}')
  else:out.append(c)
  i+=1
 return ''.join(out)

def formula_block(s):
 rows=[]
 for line in s.splitlines():
  if not line.strip():rows.append(r'\noalign{\vskip3pt}');continue
  if re.search(r'[\u4e00-\u9fff]',line) or line.strip().startswith('['):rows.append(r'\text{'+esc(line.strip())+'}');continue
  rows.append(math(line.strip()))
 # A separate display for each row prevents one long expression shrinking all rows.
 return '\n'.join(r'\StudyFormula{'+x+'}' for x in rows if not x.startswith(r'\noalign'))

def stringify(xs):
 out=''
 for x in xs:
  if x['t']=='Str':out+=x['c']
  elif x['t'] in ('Space','SoftBreak','LineBreak'):out+=' '
  elif x['t']=='Code':out+=x['c'][1]
  elif isinstance(x.get('c'),list):
   try:out+=stringify(x['c'])
   except (TypeError,KeyError):pass
 return out

inserts={
 '01':[(r'## 7\.','schemas'),(r'## 9\.','dbms')],
 '02':[(r'## 5\.','weak')],
 '03':[(r'## 5\.','integrity')],
 '04':[(r'## 2\.','mapping')],
 '05':[(r'## 3\.','operators'),(r'## 9\.','division')],
 '06':[(r'## 1\.','sqlflow'),(r'## 4\.','null')]
}
manifest=[]
for f in sorted(SRC.glob('*.md')):
 stem=f.stem; lang='zh' if stem.endswith('_zh') else 'en'
 s=f.read_text()
 s=re.sub(r'<u>(.*?)</u>(\*)?',lambda m:'$\\underline{\\mathsf{'+m.group(1)+'}}$'+(r'\*' if m.group(2) else ''),s)
 # Replace obsolete workflow status with this edition's truthful provenance.
 s=re.sub(r'^- (?:整理者：|Prepared by Codex).*$',('- 本版为 2026-10-20 的 LaTeX 重排；示例证据状态沿用原说明，未新增数据库实测。' if lang=='zh' else '- LaTeX edition prepared on 20 October 2026; original evidence status is retained. No new database execution is claimed.'),s,flags=re.M)
 s=re.sub(r'^- (?:下一步：|Next:|本篇完成后，|With this chapter,).*\n?','',s,flags=re.M)
 for pattern,key in inserts.get(stem[:2],[]):
  s=re.sub('('+pattern+r'[^\n]*\n)',lambda m:m.group(1)+'\n```{=latex}\n\\StudyVisual{'+key+'}{'+lang+'}\n```\n',s,count=1)
 ast=json.loads(subprocess.check_output(['pandoc','-f','markdown+raw_attribute','-t','json'],input=s.encode()))
 def walk(o):
  if isinstance(o,list):return [walk(x) for x in o]
  if not isinstance(o,dict):return o
  t=o.get('t');c=o.get('c')
  if t=='Header':
   c[1][0]=stem if c[0]==1 else stem+'-'+c[1][0]
  if t=='Link':
   target=c[2][0]
   if target.startswith('../../'):c[2][0]='../'+target
   elif target.endswith('.md'):
    name=Path(target).stem
    if name.endswith('_zh') or name.endswith('_en'):
     same=name.endswith('_'+lang) and stem.endswith('_'+lang)
     c[2][0]='#'+name if same else ('notes_zh.pdf' if name.endswith('_zh') else 'notes_en.pdf')
    elif name.startswith('tutorial'):c[2][0]='tutorial_answers.pdf'
    elif name.startswith('practice'):c[2][0]='practice_papers.pdf'
  if t=='Image':
   target=c[2][0]
   if target.endswith('.svg'):
    image_stem=Path(target).stem
    c[2][0]='figures/'+image_stem+'.pdf'
    if stem=='tutorial1_answers':
     return {'t':'RawInline','c':['latex',r'\StudyLandscapeER']}
  if t=='Code' and any(x in c[1] for x in MATHCHARS):return {'t':'Math','c':[{'t':'InlineMath'},math(c[1])]}
  if t=='CodeBlock':
   attrs,code=c
   if 'sql' in attrs[1]:return {'t':'RawBlock','c':['latex',r'\Needspace{'+str(30+15*len(code.splitlines()))+r'pt}'+ '\n\\begin{lstlisting}[language=SQL]\n'+code+'\n\\end{lstlisting}']}
   if any(x in code for x in MATHCHARS):return {'t':'RawBlock','c':['latex',formula_block(code)]}
  return {k:walk(v) for k,v in o.items()}
 ast=walk(ast)
 tex=subprocess.check_output(['pandoc','-f','json','-t','latex','--no-highlight','--wrap=none'],input=json.dumps(ast,ensure_ascii=False).encode()).decode()
 tex=re.sub(r'\\begin\{figure\}\s*\\centering\s*\\StudyLandscapeER\s*\\caption\{Complete Chen-style ER diagram\}\s*\\end\{figure\}',lambda m:r'\StudyLandscapeER',tex)
 tex=re.sub(r'\\texttt\{([0-9a-f]{64})\}',lambda m:r'\texttt{\seqsplit{'+m.group(1)+'}}',tex)
 tex=tex.replace('\\begin{verbatim}','\\begin{StudyCode}').replace('\\end{verbatim}','\\end{StudyCode}')
 tex=tex.replace(r'\includegraphics[',r'\includegraphics[')
 # Allow identifiers and schemas to wrap at semantic punctuation in tables.
 tex=re.sub(r'\\texttt\{([^{}]*)\}',lambda m:r'\texttt{'+re.sub(r'([,;/.()])',r'\1\\allowbreak{}',m.group(1))+'}',tex)
 # Each original document remains an independently editable chapter.
 tex=tex.replace('UNIQUE(empID,clinicID)',r'UNIQUE(empID,\allowbreak{}clinicID)')
 tex=tex.replace('Course.(dept,courseNo)',r'Course.\allowbreak{}(dept,\allowbreak{}courseNo)')
 tex=re.sub(r'(\\subsection\{[^\n]+\n)\n(\\StudyVisual)',r'\\Needspace{11cm}\n\1\n\2',tex)
 tex=tex.replace(r'\subsection{Q1(b) SQL}',r'\Needspace{150pt}'+'\n'+r'\subsection{Q1(b) SQL}')
 tex='\\clearpage\n'+tex
 (ROOT/'chapters'/f'{stem}.tex').write_text(tex)
 manifest.append({'source':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'chapter':f'chapters/{stem}.tex'})
(ROOT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# Existing SVG figures stay vector-based; originals are preserved alongside the MD edition.
for name in ['02_er_modelling_example','tutorial1_er']:
 svg=(SRC/(name+'.svg')).read_text()
 if name=='02_er_modelling_example':svg=svg.replace('font-size: 22px','font-size: 30px').replace('font-size: 30px; font-weight','font-size: 34px; font-weight').replace('font-size: 19px','font-size: 25px').replace('font-size:20px','font-size:26px')
 if name=='tutorial1_er':svg=svg.replace('font-size:25px','font-size:35px').replace('font-size:23px','font-size:30px').replace('class="small">HAS_TREATMENT', 'class="small" style="font-size:24px">HAS_TREATMENT')
 tmp=ROOT/'figures'/(name+'.svg');tmp.write_text(svg)
 subprocess.run(['rsvg-convert','-f','pdf','-o',str(ROOT/'figures'/(name+'.pdf')),str(tmp)],check=True)
print('Prepared',len(manifest),'editable LaTeX chapters.')
