import csv,json,re,collections,html,pathlib,networkx as nx
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'site';out.mkdir(exist_ok=True)
rows=list(csv.DictReader(open(root/'data/PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv',encoding='utf-8-sig')))
assert len(rows)==3179
assert all(r['transaction_type']=='P' and r['asset_type']=='ST' and r['ticker_parse_status']=='accepted' and r['transaction_date'].startswith('2025-') for r in rows)
clean=lambda s:re.sub(r'^(Hon\.\s*|Honorable\s+)','',s,flags=re.I).strip()
pairs=collections.Counter((clean(r['politician']),r['ticker_v8_2_cleaned'].strip().upper()) for r in rows)
buyers=collections.defaultdict(set)
for p,t in pairs:buyers[t].add(p)
shared={t for t,b in buyers.items() if len(b)>=2}
G=nx.Graph()
for (p,t),n in pairs.items():
 if t in shared:G.add_edge('p:'+p,'t:'+t,transactions=n)
pols=sorted(n for n in G if n.startswith('p:'))
P=nx.bipartite.weighted_projected_graph(G,pols)
top=sorted(((t,len(b)) for t,b in buyers.items()),key=lambda x:(-x[1],x[0]))[:5]
rank=sorted(((n[2:],d) for n,d in G.degree() if n.startswith('p:')),key=lambda x:(-x[1],x[0]))[:5]
connected=sorted(nx.connected_components(P),key=len,reverse=True)
metrics={'records':len(rows),'all_politicians':len({p for p,t in pairs}),'all_tickers':len(buyers),'shared_tickers':len(shared),'display_politicians':len(pols),'bipartite_ties':G.number_of_edges(),'projection_ties':P.number_of_edges(),'components':len(connected),'largest_component':len(connected[0]),'top_stocks':top,'degree_leaders':rank,'projection_density':nx.density(P)}
(out/'analysis.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
# A small, explicitly labeled slice shows the bipartite rule legibly.
ts=[t for t,n in top[:3]]
ps=sorted(set.union(*(buyers[t] for t in ts)))
pos={p:(120,65+i*460/max(1,len(ps)-1)) for i,p in enumerate(ps)}
pos.update({t:(650,120+i*170) for i,t in enumerate(ts)})
svg=['<svg viewBox="0 0 840 590" role="img" aria-label="Politicians connected to the three most widely shared stock tickers">']
for p in ps:
 for t in ts:
  if (p,t) in pairs:
   x,y=pos[p];a,b=pos[t];svg.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="#577182" stroke-opacity=".5"/>')
for p in ps:
 x,y=pos[p];svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#2780e3"/><text x="{x-10}" y="{y+4}" text-anchor="end" fill="#333333" font-size="10">{html.escape(p)}</text>')
for t in ts:
 x,y=pos[t];svg.append(f'<rect x="{x-7}" y="{y-7}" width="14" height="14" fill="#c76b16"/><text x="{x+18}" y="{y+6}" fill="#c76b16" font-size="22">{t}</text>')
svg.append('</svg>');network=''.join(svg)
bars=''.join(f'<div class="bar"><span>{t}</span><i style="width:{n/top[0][1]*72}%"></i><b>{n}</b></div>' for t,n in top)
leaders=''.join(f'<tr><td>{html.escape(p)}</td><td>{n}</td></tr>' for p,n in rank)
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Who bought the same stocks? | Sean Ryan</title>
<style>*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#ffffff;color:#222222;font:17px/1.6 "Source Sans Pro",system-ui,sans-serif}a{color:#2780e3}header{position:fixed;z-index:3;inset:0 0 auto;background:#f8f9faf5;border-bottom:1px solid #dee2e6;padding:14px 4vw;display:flex;justify-content:space-between;align-items:center;font-size:13px}nav{display:flex;gap:16px}button{border:1px solid #2780e3;background:transparent;color:#2780e3;border-radius:4px;padding:7px 12px;cursor:pointer}section{min-height:0;padding:85px max(6vw,calc((100vw - 1180px)/2)) 70px;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid #dee2e6;scroll-margin-top:40px;position:relative}h1{font-size:clamp(36px,4vw,56px);line-height:1.03;max-width:1000px;letter-spacing:-.045em;margin:20px 0}h2{font-size:clamp(28px,3vw,40px);line-height:1.12;letter-spacing:-.035em;margin:12px 0 28px;max-width:1000px}h3{font-size:22px;color:#c76b16}.eyebrow{text-transform:uppercase;letter-spacing:.17em;font-size:12px;color:#2780e3}.lede{font-size:21px;max-width:780px;color:#555555}.split{display:grid;grid-template-columns:1fr 1.1fr;gap:6vw;align-items:center}.number{font-size:52px;line-height:1;color:#c76b16}.stats{display:flex;gap:65px;margin-top:34px}.stats small{display:block;font-size:14px;max-width:180px;margin-top:10px;color:#555555}.sub{color:#606770;font-size:15px;max-width:950px}.bar{display:flex;align-items:center;gap:14px;margin:20px 0;font-size:21px}.bar span{width:65px}.bar i{height:22px;background:#2780e3}.bar b{font-weight:500}table{border-collapse:collapse;width:100%;font-size:20px}td,th{text-align:left;border-bottom:1px solid #dee2e6;padding:12px 0}td:last-child,th:last-child{text-align:right}th{font-size:13px;color:#606770;font-weight:400}.takeaway{font-size:26px;border-left:3px solid #c76b16;padding-left:22px;max-width:830px}.notes{display:none;background:#f2f6fa;padding:20px;margin-top:22px;font-size:17px;color:#333333}.show-notes .notes{display:block}.foot{position:absolute;bottom:24px;font-size:12px;color:#606770}.legend{font-size:13px;color:#606770}svg{width:100%;max-height:65vh}.present header nav a{display:none}.present section{height:100vh;min-height:100vh;overflow:auto}.present h1{font-size:clamp(44px,6vw,80px)}footer{padding:35px 7vw;font-size:14px}.source{max-width:1000px}.links{display:flex;gap:20px;flex-wrap:wrap;margin-top:30px}@media(max-width:800px){.split{grid-template-columns:1fr;gap:20px}header nav a{display:none}section{padding:100px 6vw 65px}.stats{gap:25px}.number{font-size:45px}svg{max-height:none}.lede{font-size:21px}}@media print{header,button,.notes{display:none!important}section{break-after:page;min-height:0;height:95vh;padding:30px}body{print-color-adjust:exact}footer{break-before:page}}</style>
<header><a style="font-size:21px;text-decoration:none;color:inherit" href="https://strokeofluck.github.io/sean-data-portfolio/">Sean Ryan</a><nav><a href="#question">Question</a><a href="#data">Data</a><a href="#results">Results</a><a href="#meaning">Meaning</a><button id="notes">Speaker notes</button><button id="present">Present</button></nav></header>
<main><section id="question"><div class="eyebrow">Data journalism · Social network analysis</div><h1>Congressional Stock Network</h1><p class="lede">Who bought the same stocks?</p><p class="lede">Shared stock purchases among U.S. House disclosure filers in 2025.</p><p class="sub">Sean Ryan · DSA 295 (003) · November 23, 2026</p><p>Which stocks connect the most politicians?<br>How does shared purchasing connect the filers to one another?</p><div class="notes">0:00–0:35. My data-wrangling project turns congressional transaction disclosures into searchable records. For SNA, I use those records to ask which stocks connect the most politicians and how much their reported purchasing overlaps. This is a network of disclosed purchases across 2025, rather than evidence that people traded together.</div><div class="foot">01 / 05 · Research question</div></section>
<section id="data"><div class="eyebrow">The data and network</div><h2>One link connects a filer<br>to a stock they purchased</h2><div class="split"><div><p>House Periodic Transaction Reports supply the transaction records. Repeated purchases count once when measuring distinct stock connections.</p><div class="stats"><div><div class="number">3,179</div><small>accepted public-stock purchase records</small></div><div><div class="number">ALLP</div><small>distinct politician names in the extract</small></div></div><p class="sub">2025 transaction dates. Purchases only. The opening graph retains tickers purchased by at least two distinct politicians.</p></div><div>NETWORK<div class="legend">Cyan circles: filers. Orange squares: stocks.<br>Illustrative slice: the three most widely shared tickers and all their buyers.</div></div></div><div class="notes">0:35–1:20. The frozen extract contains 3,179 accepted purchase records. The two node types are politicians and stock tickers. A link means that a disclosure reports at least one purchase of that ticker. A spouse or dependent transaction can appear under the filer. The graph slice shows the most widely shared stocks, while the metrics use the full eligible graph.</div><div class="foot">02 / 05 · Two-mode network</div></section>
<section id="results"><div class="eyebrow">Degree centrality</div><h2>TOPSTOCK connects the most filers</h2><div class="split"><div><h3>Stocks ranked by distinct buyers</h3>BARS<p class="sub">Stock degree = number of distinct politicians linked to the ticker. Counts measure buyers in this extract.</p></div><div><h3>Filers ranked by distinct shared stocks</h3><table><thead><tr><th>Filer</th><th>Stock degree</th></tr></thead><tbody>LEADERS</tbody></table><p class="sub">Politician degree uses the shared-stock graph. It measures purchasing breadth, with no weighting by trade value or repeated purchases.</p></div></div><div class="notes">1:20–2:10. TOPSTOCK has the highest stock degree, linking TOPN filers. The table on the right answers a different question: which filers bought the broadest set of stocks that at least one other politician also bought. Degree here is a count of distinct neighbors. It does not measure investment returns, influence, or wrongdoing.</div><div class="foot">03 / 05 · Calculated from the frozen extract</div></section>
<section id="projection"><div class="eyebrow">One-mode projection</div><h2>Shared stocks connect PROJP<br>pairs of filers</h2><p class="lede">Connect two politicians when their disclosures include at least one common ticker. The tie weight counts distinct shared tickers.</p><div class="stats"><div><div class="number">POLN</div><small>filers in the shared-stock graph</small></div><div><div class="number">TICKN</div><small>tickers with at least two buyers</small></div><div><div class="number">LARGEST</div><small>filers in the largest connected component</small></div></div><p class="takeaway">DENSITY of possible filer pairs share at least one stock in this graph.</p><p class="sub">The projection uses PROJT distinct politician–ticker ties. Shared ticker purchases can occur months apart.</p><div class="notes">2:10–3:00. The projection keeps only politicians. A tie joins any pair with a shared purchased stock. Its weight is the number of distinct common tickers. There are PROJP such pairs among POLN filers. The largest connected component contains LARGEST filers. Popular stocks can create many projected ties, so connectivity by itself should not be interpreted as a personal relationship.</div><div class="foot">04 / 05 · Shared-stock projection</div></section>
<section id="meaning"><div class="eyebrow">Interpretation</div><h2>Disclosures reveal overlap<br>in reported purchasing</h2><p class="takeaway">The network makes common stock choices visible and identifies the tickers that connect the widest group of filers.</p><p class="lede">Overlap alone cannot establish coordination, privileged information, or investment performance.</p><p class="sub">This extract excludes sales, other asset types, and unresolved tickers. Disclosures can include spouse or dependent transactions. Dollar amounts are reported in ranges. Missing records and ticker resolution can change the network.</p><div class="links"><a href="https://strokeofluck.github.io/congressional-stock-network-2025/" target="_blank" rel="noopener">Open original interactive project ↗</a><a href="#sources">Data and calculation notes ↓</a></div><div class="notes">3:00–3:40. The useful finding is descriptive: we can see which tickers connect the widest group of filers and how those purchases form an overlapping network. That creates a starting point for further reporting. A stronger investigation would compare purchase timing, household ownership, market popularity, and committee context before making claims about why any overlap occurs.</div><div class="foot">05 / 05 · Takeaway and limitations</div></section></main>
<footer id="sources" class="source"><h3>Sources and calculation notes</h3><p><a href="https://github.com/Strokeofluck/congressional-stock-network-sna">GitHub repository</a> · <a href="https://github.com/Strokeofluck/congressional-stock-network-sna/blob/main/METHODS.md">Full methods and findings</a> · <a href="https://github.com/Strokeofluck/congressional-stock-network-sna/blob/main/DATA_PROVENANCE.md">Data provenance</a></p><p>Adapted from Sean Ryan’s existing congressional stock-network project. Frozen source: <a href="https://github.com/Strokeofluck/congressional-stock-network-2025/blob/main/PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv">2025 accepted purchase extract</a>. Original records: <a href="https://disclosures-clerk.house.gov/">House financial disclosures</a>. Prepared November 8, 2026. This presentation reanalyzes the existing snapshot rather than refreshing the underlying scrape.</p><p>Filters: transaction_type=P, asset_type=ST, ticker_parse_status=accepted, transaction year=2025, nonempty ticker. Strip Hon./Honorable from names and uppercase tickers, matching the original project. Unique politician–ticker pairs define unweighted two-mode ties. Retain tickers with at least two buyers. The undirected politician projection joins filers sharing a retained ticker. Density = observed projected ties / all possible filer pairs. Committee links are outside the metrics shown here.</p><p><a href="analysis.json">Calculated results</a> · <a href="purchase-data.csv">Source extract</a></p></footer>
<script>(() => {
const slides = [...document.querySelectorAll('main > section'),document.querySelector('footer#sources')].filter(Boolean);
const present = document.querySelector('#present'), notes = document.querySelector('#notes');
const style = document.createElement('style');
style.textContent = `
.deck-controls{position:fixed;z-index:5;inset:auto 0 0;display:flex;align-items:center;justify-content:center;gap:18px;padding:12px 4vw calc(12px + env(safe-area-inset-bottom));background:#f8f9fa;border-top:1px solid #dee2e6}
.deck-controls button{min-height:42px;min-width:100px;background:white}.deck-controls button:last-child{background:#2780e3;color:white}.deck-controls button:disabled{opacity:.4;cursor:default}.deck-status{font-size:14px;text-align:center;min-width:180px}body{padding-bottom:85px}body.slide-deck{overflow:hidden}
.slide-deck main > section,.slide-deck footer#sources{display:none}
.slide-deck main > section.active-slide,.slide-deck footer#sources.active-slide{display:flex;flex-direction:column;justify-content:flex-start;position:fixed;inset:var(--deck-header,75px) 0 var(--deck-controls,80px);height:auto;min-height:0;margin:0;overflow:auto;overscroll-behavior:contain;padding:28px max(6vw,calc((100vw - 1180px)/2)) 36px;border:0;scroll-behavior:auto}
.slide-deck #question.active-slide{justify-content:center}.active-slide h1:focus,.active-slide h2:focus,.active-slide h3:focus{outline:none}header nav button{white-space:nowrap}
@media(max-width:650px){header{gap:10px}header nav{gap:8px}.deck-controls{gap:10px}.deck-status{min-width:0;flex:1;font-size:12px}.deck-controls button{min-width:80px}.slide-deck main > section.active-slide,.slide-deck footer#sources.active-slide{padding:22px 6vw 30px}.slide-deck #question.active-slide{justify-content:flex-start}}
@media print{body.slide-deck{overflow:visible;padding:0}.deck-controls{display:none!important}.slide-deck main > section,.slide-deck main > section.active-slide,.slide-deck footer#sources,.slide-deck footer#sources.active-slide{display:block!important;position:static;height:auto;min-height:0;overflow:visible;break-after:page;padding:30px}}
`;
document.head.append(style);
const controls=document.createElement('nav');
controls.className='deck-controls';controls.setAttribute('aria-label','Slide navigation');
controls.innerHTML='<button type="button" id="slide-prev">← Previous</button><span class="deck-status" role="status" aria-live="polite"></span><button type="button" id="slide-next">Next →</button>';
document.body.append(controls);
const prev=controls.querySelector('#slide-prev'),next=controls.querySelector('#slide-next'),status=controls.querySelector('.deck-status');
const labels={question:'Introduction','source-records':'Source records','source-code':'Extraction walkthrough','network-demo':'Interactive network',data:'Data and ties',results:'Degree centrality',projection:'Shared-stock projection',meaning:'Interpretation',sources:'Sources'};
let current=0;
function resize(){document.documentElement.style.setProperty('--deck-header',document.querySelector('header').getBoundingClientRect().height+'px');document.documentElement.style.setProperty('--deck-controls',controls.getBoundingClientRect().height+'px');}
function targetIndex(target){return slides.findIndex(slide=>slide===target||(target&&slide.contains(target)));}
function show(index,updateHash=true,focus=false){
 current=Math.max(0,Math.min(slides.length-1,index));
 slides.forEach((slide,i)=>slide.classList.toggle('active-slide',i===current));
 prev.disabled=current===0;next.disabled=current===slides.length-1;
 status.textContent=(current+1)+' / '+slides.length+' · '+(labels[slides[current].id]||'Slide');
 if(updateHash)history.replaceState(null,'','#'+slides[current].id);
 if(document.body.classList.contains('slide-deck')){
  slides[current].scrollTop=0;
  if(focus){const heading=slides[current].querySelector('h1,h2,h3');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}}
 }else if(updateHash)slides[current].scrollIntoView({behavior:'instant'});
 resize();
}
function setDeck(enabled){document.body.classList.toggle('slide-deck',enabled);present.textContent=enabled?'Scroll view':'Present';present.setAttribute('aria-pressed',String(enabled));show(current,false);if(!enabled)slides[current].scrollIntoView({behavior:'instant'});}
prev.onclick=()=>show(current-1,true,true);next.onclick=()=>show(current+1,true,true);
present.onclick=()=>setDeck(!document.body.classList.contains('slide-deck'));
notes.onclick=()=>notes.setAttribute('aria-pressed',String(document.body.classList.toggle('show-notes')));
document.addEventListener('click',event=>{const link=event.target.closest('a[href^="#"]');if(!link)return;const index=targetIndex(document.getElementById(link.getAttribute('href').slice(1)));if(index>=0){event.preventDefault();show(index,true,true);}});
document.addEventListener('keydown',event=>{
 if(event.defaultPrevented||event.altKey||event.ctrlKey||event.metaKey||event.target.closest('input,textarea,select,button,a,summary,[contenteditable="true"],[role="slider"]'))return;
 if(['ArrowRight','PageDown','ArrowLeft','PageUp','Home','End'].includes(event.key)){event.preventDefault();show(event.key==='Home'?0:event.key==='End'?slides.length-1:current+(['ArrowRight','PageDown'].includes(event.key)?1:-1),true,true);}
 if(event.key.toLowerCase()==='n')notes.click();if(event.key==='Escape')setDeck(false);
});
window.addEventListener('hashchange',()=>{const index=targetIndex(document.getElementById(location.hash.slice(1)));if(index>=0)show(index,false);});
window.addEventListener('resize',resize);
if(typeof ResizeObserver!=='undefined'){const observer=new ResizeObserver(resize);observer.observe(document.querySelector('header'));observer.observe(controls);}
window.addEventListener('scroll',()=>{
 if(document.body.classList.contains('slide-deck'))return;
 const offset=document.querySelector('header').getBoundingClientRect().height;
 let nearest=0;slides.forEach((slide,i)=>{if(Math.abs(slide.getBoundingClientRect().top-offset)<Math.abs(slides[nearest].getBoundingClientRect().top-offset))nearest=i;});
 current=nearest;prev.disabled=current===0;next.disabled=current===slides.length-1;status.textContent=(current+1)+' / '+slides.length+' · '+(labels[slides[current].id]||'Slide');
},{passive:true});
const initial=targetIndex(document.getElementById(location.hash.slice(1)));if(initial>=0)current=initial;
setDeck(true);
})();</script></html>'''
replace={'ALLP':str(metrics['all_politicians']),'NETWORK':network,'TOPSTOCK':top[0][0],'TOPN':str(top[0][1]),'BARS':bars,'LEADERS':leaders,'PROJP':f"{P.number_of_edges():,}",'POLN':str(len(pols)),'TICKN':str(len(shared)),'LARGEST':str(len(connected[0])),'DENSITY':f'{nx.density(P):.1%}','PROJT':f'{G.number_of_edges():,}'}
for a,b in replace.items():page=page.replace(a,b)
(out/'index.html').write_text(page,encoding='utf-8')
(out/'purchase-data.csv').write_bytes((root/'data/PTR_transactions_2025_ACCEPTED_STOCK_PURCHASES.csv').read_bytes())
assert G.number_of_edges()==sum(1 for p,t in pairs if t in shared)
assert sum(d for n,d in G.degree() if n.startswith('t:'))==G.number_of_edges()
assert P.number_of_edges()==len({tuple(sorted((a,b))) for t in shared for a in buyers[t] for b in buyers[t] if a!=b})

