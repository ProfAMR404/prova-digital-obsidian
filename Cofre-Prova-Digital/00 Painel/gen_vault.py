#!/usr/bin/env python3
"""Gera o cofre Obsidian do Painel de Ementas Prova Digital a partir de painel.json.
Uso: python3 gen_vault.py painel.json PASTA_DO_COFRE"""
import json, re, sys, os, collections

src, out = sys.argv[1], sys.argv[2]
URL = sys.argv[3] if len(sys.argv) > 3 else ''
PD = '00 Painel'
LOGO = os.path.exists(os.path.join(out, PD, 'prof_amr_logo.png'))
S = json.load(open(src, encoding='utf-8'))

def fname(s):
    s = s.replace('/', '-').replace('\\', '-').replace(':', ' -').replace('[', '(').replace(']', ')')
    s = re.sub(r'[|#^?*"<>]', '', s)
    return re.sub(r'\s+', ' ', s).strip().rstrip('.')
def w(rel, text):
    p = os.path.join(out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(text.rstrip() + '\n')
def yq(v): return '"' + str(v).replace('\\', '\\\\').replace('"', '\\"') + '"'
def fm(d):
    L = ['---']
    for k, v in d.items():
        if isinstance(v, list):
            L.append(k + ':'); L += ['  - ' + yq(x) for x in v]
        else: L.append(k + ': ' + yq(v))
    return '\n'.join(L + ['---', ''])
def link(name, alias=None): return '[[' + fname(name) + ('|' + alias if alias else '') + ']]'
def quote(t): return '\n'.join('> ' + l if l else '>' for l in t.split('\n'))

# ---------- entidades [mesma lógica do grafo do painel] ----------
def cpp(n): return re.compile(r'(?:CPP|Código de Processo Penal)[^.;\n]{0,60}?\b%s\b(?!-)|\b%s\b(?!-)[^.;\n]{0,80}?(?:CPP|Código de Processo Penal)' % (n, n))
PL = 'https://www.planalto.gov.br/ccivil_03/'
CPPU, CRU, STJS = PL + 'decreto-lei/del3689.htm', PL + 'constituicao/constituicao.htm', 'https://scon.stj.jus.br/SCON/sumstj/'
DISP = [
 ('CPP, arts. 158-A a 158-F', re.compile(r'158-[A-F]'), CPPU),
 ('CPP, art. 155', cpp(155), CPPU), ('CPP, art. 157', cpp(157), CPPU), ('CPP, art. 158', cpp(158), CPPU), ('CPP, art. 159', cpp(159), CPPU),
 ('CPP, art. 386', cpp(386), CPPU), ('CPP, art. 400', cpp(400), CPPU),
 ('CPP, art. 563', re.compile(cpp(563).pattern + r'|pas de nullit', re.I), CPPU), ('CPP, art. 565', cpp(565), CPPU), ('CPP, art. 619', cpp(619), CPPU),
 ('CR, art. 5º, XII', re.compile(r'5º,\s*(?:inciso\s*)?XII\b'), CRU), ('CR, art. 5º, LIV', re.compile(r'5º,\s*(?:inciso\s*)?LIV\b'), CRU), ('CR, art. 5º, LVI', re.compile(r'5º,\s*(?:inciso\s*)?LVI\b'), CRU),
 ('Lei 13.964-2019', re.compile(r'13\.964'), PL + '_ato2019-2022/2019/lei/l13964.htm'),
 ('Lei 12.965-2014', re.compile(r'12\.965'), PL + '_ato2011-2014/2014/lei/l12965.htm'),
 ('Lei 12.850-2013', re.compile(r'12\.850'), PL + '_ato2011-2014/2013/lei/l12850.htm'),
 ('Lei 11.340-2006', re.compile(r'11\.340'), PL + '_ato2004-2006/2006/lei/l11340.htm'),
 ('Súmula 7-STJ', re.compile(r'Súmulas?\s*(?:n\.?º?\s*)?7\b'), STJS + 'toc.jsp?livre=%277%27.num.&O=JT'),
 ('Súmula 83-STJ', re.compile(r'Súmulas?\s*(?:n\.?º?\s*)?(?:7\s*e\s*)?83\b'), STJS + 'toc.jsp?livre=%2783%27.num.&O=JT'),
 ('Súmula 182-STJ', re.compile(r'Súmulas?\s*(?:n\.?º?\s*)?(?:7\s*e\s*)?182\b'), STJS + 'toc.jsp?livre=%27182%27.num.&O=JT'),
 ('Súmula Vinculante 14', re.compile(r'Súmula Vinculante\s*(?:n\.?º?\s*)?14\b'), 'https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26&sumula=1230'),
]
NKEY = {'Lei 13.964-2019': None, 'Súmula 7-STJ': 'Súmula 7/STJ', 'Súmula 83-STJ': 'Súmula 83/STJ', 'Súmula 182-STJ': 'Súmula 182/STJ'}
# conceito do grafo -> termo do glossário [quando existe]
CONC = [
 ('ABNT NBR ISO/IEC 27037', re.compile(r'27037|ABNT')),
 ('Hash [função hash; código hash]', re.compile(r'\bhash', re.I)), ('Mesmidade', re.compile(r'mesmidade', re.I)), ('Metadados', re.compile(r'metadados', re.I)),
 ('Printscreen [captura de tela]', re.compile(r'prints?\b|printscreen|capturas? de tela', re.I)),
 ('UFED [Universal Forensic Extraction Device]', re.compile(r'cellebrite|\bUFED|\bUFDR', re.I)),
 ('Imagem forense [cópia espelhada; espelhamento; cópia bit a bit]', re.compile(r'espelha|bit[- ]a[- ]bit|cópia forense', re.I)),
 ('Lacre', re.compile(r'\blacr', re.I)), ('Auditabilidade', re.compile(r'auditab', re.I)), ('Geotag', re.compile(r'geotag', re.I)),
 ('Assinatura digital', re.compile(r'assinatura digital', re.I)), ('Repetibilidade', re.compile(r'repetibilidade', re.I)), ('Reprodutibilidade', re.compile(r'reprodutibilidade', re.I)),
 ('Laudo pericial', re.compile(r'laudo pericial', re.I)), ('Perícia oficial', re.compile(r'per[íi]cia oficial|perito oficial', re.I)),
 ('ERB [estação rádio base]', re.compile(r'\bERB|estaç(?:ão|ões) r[áa]dio', re.I)), ('Vestígio digital', re.compile(r'vest[íi]gios? digita', re.I)),
 ('Cadeia de custódia [cadeia de custódia informacional]', re.compile(r'cadeia de cust[óo]dia', re.I)),
]
PREC = re.compile(r'((?:(?:AgRg|EDcl|AgInt|RCD)\s+n[oa]s?\s+)*(?:HC|RHC|REsp|AREsp|EAREsp|EREsp|ARE|RE|Inq|APn|RMS|ADI|Rcl))\s*(?:n\.?º?\s*)?(\d{1,3}(?:\.\d{3})+|\d{4,7})\s*/\s*([A-Z]{2})\b')
def pkey(c, n, u): return (re.sub(r'\s+', ' ', c).strip() + ' ' + n.replace('.', '') + '/' + u).lower()
def own(j):
    m = PREC.search(j['classe']); return pkey(*m.groups()) if m else ''

gl_names = {g['t'] for g in S['glossario']}
eixos = {e['id']: (i + 1, e) for i, e in enumerate(S['eixos'])}
order = [j for e in S['eixos'] for j in S['julgados'] if j['eixo'] == e['id']]
num = {j['id']: i + 1 for i, j in enumerate(order)}
CONV = {j['rel']: ('Desa. ' if 'Convocada' in j['conv'] else 'Des. ') for j in S['julgados'] if j['conv']}
def tr(r): return CONV.get(r, 'Min. ') + r
def jname(j): return fname('%s - %s' % (j['trib'], j['classe']))
def cit(j):
    p = [j['trib'], j['classe'], tr(j['rel']) + (' [' + j['conv'] + ']' if j['conv'] else ''), j['orgao'], 'j. ' + j['data']]
    return ', '.join(x for x in p if x)
def verbete(j):
    for l in j['ementa'].split('\n'):
        if l.strip() and l.strip().upper() != 'EMENTA': return l.strip()
    return ''
def eixo_name(eid): n, e = eixos[eid]; return 'Eixo %02d - %s' % (n, e['titulo'])
key2j = {own(j): j for j in order if own(j)}
names = collections.Counter(jname(j) for j in order)
assert max(names.values()) == 1, [k for k, v in names.items() if v > 1]

by_rel, by_org, by_disp, by_conc, cited_by = (collections.defaultdict(list) for _ in range(5))
for j in order:
    t = j['ementa']
    j['_d'] = [d[0] for d in DISP if d[1].search(t)]
    j['_c'] = [c[0] for c in CONC if c[1].search(t) and c[0] in gl_names]
    seen, ps = set(), []
    for m in PREC.finditer(t):
        k = pkey(*m.groups())
        if k != own(j) and k not in seen and k in key2j: seen.add(k); ps.append(key2j[k])
    j['_p'] = ps
    for p in ps: cited_by[p['id']].append(j)
    by_rel[j['rel']].append(j)
    if j['relac']: by_rel[j['relac']].append(j)
    by_org[j['trib'] + ' ' + j['orgao']].append(j)
    for d in j['_d']: by_disp[d].append(j)
    for c in j['_c']: by_conc[c].append(j)

# ---------- julgados ----------
for j in order:
    n, e = eixos[j['eixo']]
    tags = ['julgado', 'tribunal/' + j['trib'].lower(), 'eixo/%02d' % n]
    d = collections.OrderedDict(tipo='julgado', item=str(num[j['id']]), tribunal=j['trib'], classe=j['classe'])
    if j['registro']: d['registro'] = j['registro']
    d['relator'] = j['rel']
    if j['conv']: d['condicao_relator'] = j['conv']
    if j['relac']: d['relator_acordao'] = j['relac']
    d.update(orgao=j['orgao'], julgamento=j['data'], publicacao=j['dje'], eixo=eixo_name(j['eixo']))
    if j.get('grupo'): d['subgrupo'] = j['grupo']
    d['inteiro_teor'] = j['link']; d['aliases'] = [j['classe'], cit(j)]; d['tags'] = tags
    b = [fm(d), '# ' + cit(j), '']
    b += ['**Eixo:** ' + link(eixo_name(j['eixo'])) + (' · ' + j['grupo'] if j.get('grupo') else ''),
          '**Relator:** ' + link(tr(j['rel'])) + (' [' + j['conv'] + ']' if j['conv'] else '') + (' · **Relator para acórdão:** ' + link(tr(j['relac'])) if j['relac'] else ''),
          '**Órgão julgador:** ' + link(j['trib'] + ' ' + j['orgao']) + ' · **Julgamento:** ' + j['data'] + ' · **Publicação:** ' + j['dje'],
          ('**Registro:** ' + j['registro'] + ' · ' if j['registro'] else '') + '**Inteiro teor:** [portal do tribunal](' + j['link'] + ')',
          '**Origem:** ' + j['origem'], '']
    b += ['## Verbetação', '', quote('“' + verbete(j) + '”'), '']
    b += ['## Ementa', '', '> [!quote]- Ementa completa [transcrição literal]', quote('“' + j['ementa'] + '”'), '', j['cit'], '']
    if j['_d']: b += ['## Dispositivos Citados', ''] + ['- ' + link(x) for x in j['_d']] + ['']
    if j['_c']: b += ['## Termos do Glossário', ''] + ['- ' + link(x, x) for x in j['_c']] + ['']
    if j['_p']: b += ['## Precedentes Citados [no Painel]', ''] + ['- ' + link(jname(p), cit(p)) for p in j['_p']] + ['']
    if cited_by[j['id']]: b += ['## Citado Por', ''] + ['- ' + link(jname(p), cit(p)) for p in cited_by[j['id']]] + ['']
    w('Julgados/' + jname(j) + '.md', '\n'.join(b))

def jl(j): return '- [%d] %s' % (num[j['id']], link(jname(j), cit(j)))
# ---------- eixos ----------
for eid, (n, e) in eixos.items():
    L = [x for x in order if x['eixo'] == eid]
    b = [fm(collections.OrderedDict(tipo='eixo', numero=str(n), julgados=str(len(L)), tags=['eixo'])), '# Eixo %d · %s' % (n, e['titulo']), '', e['desc'], '']
    groups = collections.OrderedDict()
    use_g = any(x.get('grupo') for x in L)
    for x in L: groups.setdefault(x.get('grupo') or 'Demais Julgados' if use_g else (x['trib'] + ' · ' + x['orgao'] if len(L) > 12 else ''), []).append(x)
    for k, (g, items) in enumerate(groups.items(), 1):
        if g: b += ['## %d.%d %s [%d]' % (n, k, g, len(items)), '']
        b += [jl(x) for x in items] + ['']
    b += ['Voltar: ' + link('Painel de Ementas Prova Digital')]
    w('Eixos/' + fname(eixo_name(eid)) + '.md', '\n'.join(b))

# ---------- relatores e órgãos ----------
for r, L in by_rel.items():
    w('Relatores/' + fname(tr(r)) + '.md', '\n'.join([fm(collections.OrderedDict(tipo='relator', julgados=str(len(L)), tags=['relator'])), '# ' + tr(r), '', '## Julgados no Painel [%d]' % len(L), ''] + [jl(x) for x in L]))
for o, L in by_org.items():
    w('Órgãos Julgadores/' + fname(o) + '.md', '\n'.join([fm(collections.OrderedDict(tipo='orgao', julgados=str(len(L)), tags=['orgao'])), '# ' + o, '', '## Julgados no Painel [%d]' % len(L), ''] + [jl(x) for x in L]))

# ---------- base legal ----------
N = S.get('normas', {})
for name, rx, url in DISP:
    L = by_disp.get(name, [])
    if not L and name not in ('CPP, arts. 158-A a 158-F',): continue
    key = NKEY.get(name, name) if name in NKEY else name.replace('-STJ', '/STJ')
    txt = N.get(key) if key else None
    b = [fm(collections.OrderedDict(tipo='dispositivo', fonte=url, julgados=str(len(L)), aliases=[name.replace('-', '/')] if '-' in name and 'Lei' in name or 'Súmula' in name else [name], tags=['base-legal'])), '# ' + name.replace('-STJ', '/STJ').replace('ISO-IEC', 'ISO/IEC').replace('-20', '/20'), '']
    if url: b += ['**Fonte oficial:** [abrir](' + url + ')', '']
    if txt: b += ['## Texto [transcrição literal]', '', quote('“' + txt + '”'), '']
    b += ['## Julgados Que Citam [%d]' % len(L), ''] + [jl(x) for x in L]
    w('Base Legal/' + fname(name) + '.md', '\n'.join(b))
b = [fm(collections.OrderedDict(tipo='norma-tecnica', tags=['base-legal'])), '# Normas Técnicas e Procedimentos Operacionais', '']
for x in S['base']: b += ['- **' + x['t'] + '.** ' + x['d'] + (' [Abrir](' + x['url'] + ')' if x['url'] else '')]
w('Base Legal/Normas Técnicas e POPs do MJSP.md', '\n'.join(b))
bl = [fm(collections.OrderedDict(tipo='indice', tags=['base-legal'])), '# Base Legal', '', '- ' + link('Normas Técnicas e POPs do MJSP'), ''] + ['- ' + link(d[0]) + ' [%d julgados]' % len(by_disp[d[0]]) for d in DISP if by_disp.get(d[0])]
w('Base Legal/Base Legal.md', '\n'.join(bl))

# ---------- glossário ----------
for g in S['glossario']:
    L = by_conc.get(g['t'], [])
    b = [fm(collections.OrderedDict(tipo='termo', aliases=[g['t']] + [a.strip() for a in re.findall(r'\[([^\]]+)\]', g['t'])[0].split(';')] if '[' in g['t'] else [g['t']], tags=['glossario'])), '# ' + g['t'], '', g['d'], '']
    if L: b += ['## Julgados Que Mencionam [%d]' % len(L), ''] + [jl(x) for x in L]
    w('Glossário/' + fname(g['t']) + '.md', '\n'.join(b))
gi = [fm(collections.OrderedDict(tipo='indice', tags=['glossario'])), '# Glossário de Termos', '', '%d termos digitais.' % len(S['glossario']), '']
gi += ['- ' + link(g['t'], g['t']) + ': ' + g['d'] for g in sorted(S['glossario'], key=lambda g: g['t'].lower().lstrip('$'))]
w('Glossário/Glossário de Termos.md', '\n'.join(gi))

# ---------- página inicial ----------
m = S['meta']; stj = sum(1 for j in order if j['trib'] == 'STJ'); stf = sum(1 for j in order if j['trib'] == 'STF')
abrir = ('**[Abrir o Painel em HTML](' + URL + ')** · ' if URL else '') + '[[Abrir o Painel]]'
h = [fm(collections.OrderedDict(tipo='indice', tags=['painel']))] + (['![[prof_amr_logo.png|170]]', ''] if LOGO else []) + ['# ' + m['titulo'], '', abrir, '', m['lead'], '', m['fonte'], '',
     '| Julgados | STJ | STF | Eixos | Termos |', '|---|---|---|---|---|', '| %d | %d | %d | %d | %d |' % (len(order), stj, stf, len(S['eixos']), len(S['glossario'])), '',
     '## Sumário dos Eixos', '']
for eid, (n, e) in eixos.items():
    L = [x for x in order if x['eixo'] == eid]
    h += ['%d. %s: %d %s. %s' % (n, link(eixo_name(eid), e['titulo']), len(L), 'julgado' if len(L) == 1 else 'julgados', e['desc'])]
h += ['', '## Demais Entradas', '', '- ' + link('Glossário de Termos'), '- ' + link('Base Legal'), '- ' + link('Todos os Julgados'),
      '- Artefato do painel: `Painel/Painel_de_Ementas_Prova_Digital.html` [abre no navegador]', '',
      '## Relatores', '', ' · '.join(link(tr(r), tr(r)) + ' [%d]' % len(L) for r, L in sorted(by_rel.items(), key=lambda kv: -len(kv[1]))), '',
      '## Órgãos Julgadores', '', ' · '.join(link(o) + ' [%d]' % len(L) for o, L in sorted(by_org.items(), key=lambda kv: -len(kv[1])))]
ap = [fm(collections.OrderedDict(tipo='indice', tags=['painel']))] + (['![[prof_amr_logo.png|170]]', ''] if LOGO else []) + ['# Abrir o Painel', '']
if URL: ap += ['- [Painel em HTML na web](' + URL + ') [abre no navegador]']
ap += ['- [[Painel_de_Ementas_Prova_Digital.html|Painel em HTML, arquivo do cofre]] [abre no navegador]', '- ' + link('Painel de Ementas Prova Digital', 'Página inicial do cofre')]
w(PD + '/Abrir o Painel.md', '\n'.join(ap))
w('Painel de Ementas Prova Digital.md', '\n'.join(h))
t = [fm(collections.OrderedDict(tipo='indice', tags=['painel'])), '# Todos os Julgados', '', '| Item | Julgado | Relator | Órgão | Julgamento | Eixo |', '|---|---|---|---|---|---|']
t += ['| %d | %s | %s | %s | %s | %s |' % (num[j['id']], link(jname(j), j['trib'] + ' ' + j['classe']).replace('|', '\\|'), j['rel'], j['orgao'], j['data'], link(eixo_name(j['eixo']), 'Eixo %d' % eixos[j['eixo']][0]).replace('|', '\\|')) for j in order]
w('Todos os Julgados.md', '\n'.join(t))
print('notas:', sum(len(f) for _, _, f in os.walk(out)), '| julgados', len(order), '| relatores', len(by_rel), '| órgãos', len(by_org), '| glossário', len(S['glossario']))
