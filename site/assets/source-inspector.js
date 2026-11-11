(() => {
const repo='https://github.com/Strokeofluck/Data-Wrangling-and-Web-Scraping-P3/blob/main/';
const entries={
 House:{
 image:'demos/p3/source/20016861.webp',alt:'Captured House PTR filed by John McGuire on May 16, 2025',
 caption:'House Clerk PDF · John McGuire · Filing 20016861',
 fields:{
 ticker:{label:'Asset & ticker',title:'Carry the resolved ticker into a common schema',why:'The House PDF reports the asset and ticker together. P3 carries the cleaned ticker and asset name into separate fields, then restricts the comparison to accepted ticker records.',code:"'ticker':src.ticker_v8_2_cleaned,\n'asset_name':src.asset_v8_2_cleaned,\n...\nscope_ok=df.asset_type.eq('ST') & df.ticker_status.eq('accepted')",file:'scripts/integration.py'},
 date:{label:'Transaction date',title:'Use the transaction date to derive the month',why:'The comparison uses when the transaction happened, rather than the filing or notification date. An invalid or missing date stops the comparison.',code:"parsed=pd.to_datetime(df.transaction_date,\n    format='%Y-%m-%d',errors='coerce')\nassert parsed.notna().all()\ndf['month']=parsed.dt.strftime('%Y-%m')",file:'scripts/integration.py'},
 owner:{label:'Owner',title:'Preserve who the disclosure says owned the asset',why:'An SP code can identify a spouse transaction. Preserve the owner field; the filer name alone does not establish that the filer personally made the purchase.',code:"'owner':src.owner,\n'politician':src.politician,",file:'scripts/integration.py'},
 amount:{label:'Amount',title:'Keep the reported bracket',why:'The source reports an amount range. P3 retains the original text and numeric bounds; it does not turn this range into an exact investment total.',code:"'amount_raw':src.amount_raw,\n'amount_min':pd.to_numeric(src.amount_min,errors='coerce'),\n'amount_max':pd.to_numeric(src.amount_max,errors='coerce'),",file:'scripts/integration.py'}
 }},
 Senate:{
 image:'assets/senate-original-chrome.jpg',alt:'Captured official Senate report for David McCormick dated December 26, 2025',
 caption:'Senate eFD HTML · David McCormick · Filed December 26, 2025',
 fields:{
 ticker:{label:'Table & ticker',title:'Check the HTML table before reading its cells',why:'The Senate provides a separate ticker cell. P3 matches the expected nine headers, then reads the columns in that order. Changed or missing headers raise an error.',code:"headers=[re.sub(r'\\s+',' ',cell.get_text(' ',strip=True))\n    for cell in table.select('thead th')]\nif headers == HEADERS: return table\n...\nitem,date,owner,ticker,asset,asset_type,kind,amount,comment=values",file:'scripts/senate.py'},
 date:{label:'Transaction date',title:'Parse the date explicitly',why:'The parser expects month/day/year and saves an ISO date. A date that does not match raises an error instead of silently guessing a format.',code:"date=datetime.strptime(date,'%m/%d/%Y').date().isoformat()\n...\n 'transaction_date':date,",file:'scripts/senate.py'},
 owner:{label:'Owner',title:'Keep the reported owner separate from the filer',why:'The owner cell is preserved, while the filer name comes from the archived filing index. These represent different facts.',code:"'politician':filing['filer_name'],\n'owner':owner,",file:'scripts/senate.py'},
 amount:{label:'Amount',title:'Keep bounds and the original amount text',why:'P3 reads numeric bounds from the reported amount range. An open-ended range keeps its upper bound missing.',code:"nums=[int(x.replace(',',''))\n    for x in re.findall(r'\\$\\s*([0-9][0-9,]*)',amount)]\nlow=nums[0]\nhigh=None if re.search(r'over|more than',amount,re.I) else nums[-1]\n...\n'amount_raw':amount,'amount_min':low,'amount_max':high,",file:'scripts/senate.py'}
 }}
};
const escape=text=>text.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
document.querySelectorAll('.source-inspector').forEach(host=>{
 let chamber='House',field='ticker';
 function render(){
 const data=entries[chamber],item=data.fields[field];
 host.innerHTML='<div class="si-toolbar" role="group" aria-label="Source chamber">'+Object.keys(entries).map(name=>'<button type="button" data-chamber="'+name+'" aria-pressed="'+(name===chamber)+'">'+name+' · '+(name==='House'?'PDF':'HTML')+'</button>').join('')+'</div><div class="si-grid"><figure class="si-document"><img src="'+data.image+'" alt="'+data.alt+'"><figcaption>'+data.caption+'</figcaption></figure><div class="si-detail"><div class="si-fields" role="group" aria-label="Source fields">'+Object.entries(data.fields).map(([key,value])=>'<button type="button" data-field="'+key+'" aria-pressed="'+(key===field)+'">'+value.label+'</button>').join('')+'</div><div aria-live="polite"><span class="si-kicker">Source → code → reason</span><h3>'+item.title+'</h3><p>'+item.why+'</p><pre><code>'+escape(item.code)+'</code></pre><a href="'+repo+item.file+'" target="_blank" rel="noopener">Read the source code ↗</a><p style="font-size:12px;color:#606770;margin-top:12px">Selected excerpts from the project code; … marks omitted lines.</p></div></div></div>';
 host.querySelectorAll('[data-chamber]').forEach(button=>button.onclick=()=>{chamber=button.dataset.chamber;render();host.querySelector('[data-chamber="'+chamber+'"]').focus();});
 host.querySelectorAll('[data-field]').forEach(button=>button.onclick=()=>{field=button.dataset.field;render();host.querySelector('[data-field="'+field+'"]').focus();});
 }
 render();
});
})();