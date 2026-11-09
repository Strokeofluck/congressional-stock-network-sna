from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'site/index.html'
s=p.read_text(encoding='utf-8')
sections=(root/'showcase-sections.html').read_text(encoding='utf-8')
s=s.replace('<section id="data">',sections+'<section id="data">',1)
s=s.replace('</style>','.record{max-height:780px;overflow:auto;border:1px solid #dee2e6;background:#f8f9fa}.demo{display:block;width:100%;height:780px;border:1px solid #dee2e6;background:white}.inspector{height:900px}.network{height:850px}section{scroll-margin-top:65px}.foot{display:none}nav{flex-wrap:wrap}@media(max-width:700px){.demo{height:650px}}@media print{iframe{display:none}}'+'</style>')
s=s.replace('<a href="#question">Question</a><a href="#data">Data</a><a href="#results">Results</a><a href="#meaning">Meaning</a>','<a href="#house-source">House PTR</a><a href="#senate-source">Senate</a><a href="#source-code">P3 inspector</a><a href="#network-demo">Network</a><a href="#results">SNA results</a>')
s=s.replace('Which stocks connect the most politicians?','The records, the extraction, and the network in one scrolling walkthrough.<br><br>Which stocks connect the most politicians?')
p.write_text(s,encoding='utf-8')
