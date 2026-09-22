"""4_Lab_Tools/531_Builder.html — self-contained, browser-based build console for the bench parts.
Carries the learner-safe spec (no keys, no seeds); rebuilds any/all lab tools from the same spec logic
as gen_tools.py (byte-identical output); exports handout bench text, label sheet and kit summary as HTML.
Hostable on GitHub Pages; linkable from Canvas."""
import os, sys, json, html, re
sys.path.insert(0, os.path.dirname(__file__))
import spec, gen_tools
from ui_layer import UI_CSS, UI_JS
from spec import *
OUT = os.environ["OUT"]

# learner-safe spec: strip keys, station seeds, rubric text
SAFE = {}
for lid in LAB_ORDER:
    L = dict(LABS[lid]); L.pop("key", None); L.pop("station", None); L.pop("rubric", None); SAFE[lid] = L
SPEC = {
 "VERSION": VERSION, "VDATE": VDATE, "COURSE": COURSE,
 "LAB_ORDER": LAB_ORDER, "LAB_META": LAB_META, "LABS": SAFE,
 "KIT": KIT, "BENCH_REGISTER": BENCH_REGISTER, "KIT_CARDS": KIT_CARDS, "LC_STAGES": LC_STAGES, "LC_CODES": LC_CODES, "DBD_TAGS": DBD_TAGS,
 "KIT_SHORT": {"SCAN":"DS2208 scanner","PRN":"ZD621 label printer","ESD":"ESD mat + wrist strap","R640":"R640 server","FRU":"R640 FRU set","RACK":"rack accessories","CART":"platform cart","RCV":"receiving props (pallet, bin, scale)","PPE":"PPE set","PKG":"packaging kit","HDD":"scrap drives (mock DBDs)","ASB":"anti-static bags","SEC":"serialized security bags","COC":"custody logbook","SW":"Snipe-IT demo"},
}
SPEC_JSON = json.dumps(SPEC, ensure_ascii=False, indent=1)
PRE = gen_tools.BENCH_PRE; POST = gen_tools.BENCH_POST

# Escape for embedding inside a <script> block
def js_str(s): return json.dumps(s, ensure_ascii=False).replace("</script", "<\\/script")

BUILDER_JS = r"""
var SPEC=__SPEC__;
var BENCH_PRE=__PRE__, BENCH_POST=__POST__, UI_CSS=__UICSS__, UI_JS=__UIJS__;
var esc=function(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;")};
function toolFile(lid,s){var m=SPEC.LAB_META[lid];return "531-"+lid+(s?"-"+s:"")+"_"+m[2]+".html"}
function kitLine(lid){return SPEC.LABS[lid].kit.map(function(k){return SPEC.KIT_SHORT[k]}).join(", ")}
function fieldHtml(f,prefix){
 var fid=prefix+f.id,t=f.type,lab=(f.gate_el?'<span class="gatetag">GATE</span> ':"")+esc(f.label),hint=f.hint,h="";
 var db=esc(JSON.stringify(f));
 if(t==="scan"||t==="lookup")h='<div><label for="'+fid+'">'+lab+'</label><input type="text" id="'+fid+'" class="scanin" autocomplete="off" spellcheck="false" data-b="'+db+'"> <span id="'+fid+'_st" role="status" style="font-size:12px"></span></div>';
 else if(t==="check")h='<div class="chk"><input type="checkbox" id="'+fid+'"><label for="'+fid+'">'+lab+'</label></div>';
 else if(t==="sel")h='<div><label for="'+fid+'">'+lab+'</label><select id="'+fid+'"'+(f.gate?' data-gate="'+esc(JSON.stringify(f.gate))+'"':"")+(f.want?' data-want="'+esc(f.want)+'"':"")+'><option value="">&mdash; choose &mdash;</option>'+f.opts.map(function(o){return "<option>"+esc(o)+"</option>"}).join("")+'</select></div>';
 else if(t==="text")h='<div><label for="'+fid+'">'+lab+'</label><input type="text" id="'+fid+'" size="22"'+(f.ph?' placeholder="'+esc(f.ph)+'"':"")+'></div>';
 else if(t==="num")h='<div><label for="'+fid+'">'+lab+'</label><input type="number" id="'+fid+'" step="0.01" min="0" data-cmp="'+esc(f.compare||"")+'" data-tol="'+(f.tol||0)+'"> <span id="'+fid+'_st" role="status" style="font-size:12px"></span></div>';
 else if(t==="fixed")h='<div><label>'+lab+'</label><div class="mono" id="'+fid+'" style="padding:8px 0">{VBS:'+f.id+'}</div></div>';
 else if(t==="issued")h='<div><label>'+lab+'</label><div class="mono" id="'+fid+'" style="padding:8px 0">{VBS:'+f.id+'}</div>'+(f.print?'<button class="small" type="button" onclick="benchPrint(\''+fid+'\')">Print label</button>':"")+'</div>';
 else if(t==="seq")h='<div style="flex:1 1 100%"><label for="'+fid+'">'+lab+'</label><input type="text" id="'+fid+'" class="seqin" autocomplete="off" spellcheck="false" data-b="'+db+'" placeholder="click here, then scan"> <button class="small" type="button" onclick="benchSeqReset(\''+fid+'\')">'+(f.lock?"Restart count":"Restart sequence")+'</button> '+(f.lock?'<button class="small" type="button" id="'+fid+'_lock" onclick="benchSeqLock(\''+fid+'\')">Lock count</button> ':"")+'<div id="'+fid+'_list" class="hint" style="margin-top:6px"></div><span id="'+fid+'_st" role="status" style="font-size:12px"></span></div>';
 if(hint&&t!=="check")h=h.replace("</div>",'<div class="hint">'+esc(hint)+'</div></div>');
 return h;
}
function benchHtml(lid,setl){
 var L=SPEC.LABS[lid],parts=[],loose=[];
 function flush(){if(loose.length){parts.push('<div class="frow">'+loose.join("")+'</div>');loose=[]}}
 L.fields.forEach(function(f){
  if(f.type==="rows"){flush();for(var r=1;r<=f.n;r++){var opt=!!(f.optional_from&&r>=f.optional_from);
    var inner=f.fields.map(function(sf){return fieldHtml(sf,"b_"+f.id+"_"+r+"_")}).join("");
    parts.push('<div class="card"'+(opt?' data-opt="1"':"")+'><h4>'+esc(f.label)+' '+r+(opt?" — "+(f.opt_label||"leave blank if unused"):"")+'</h4><div class="frow">'+inner+'</div></div>')}}
  else if(f.type==="seq"){flush();parts.push('<div class="card"><h4>'+esc(f.label.split(" — ")[0])+'</h4><div class="frow">'+fieldHtml(f,"b_")+'</div></div>')}
  else loose.push(fieldHtml(f,"b_"));
 });flush();
 var gatebox=L.gate_fail?'<div class="card gatebox"><h4>What fails the gate</h4><ul>'+L.gate_fail.map(function(x){return "<li>"+esc(x)+"</li>"}).join("")+'</ul><p class="hint">Fields marked GATE are the ones the gate reads. Everything else is scored on the rubric.</p></div>':"";
 var body=parts.join("").replace(/\{VBS:([a-z0-9]+)\}/g,function(m,fid){var v="";L.fields.forEach(function(f){if(f.id===fid)v=f.value_by_set[setl||"A"]||f.value_by_set["A"]});return esc(v)});
 return '<section class="panel" id="benchPanel"><h2>Bench panel &mdash; '+esc(L.part)+'</h2><p class="hint">Your hands-on work at the station, recorded here. Click into a scan field and scan &mdash; the scanner types the code and presses Enter for you. Green means the tool read what it expected and moves you to the next field; red tells you what to check &mdash; fix it, then scan again. At your station: '+esc(kitLine(lid))+'.</p>'+gatebox+body+'<p><button class="primary" type="button" onclick="buildBench()">Build bench record</button> <span id="benchStatus" role="status" style="font-size:12px"></span></p><div id="benchOut" aria-live="polite"></div></section>';
}
function benchJs(){
 var kk={};SPEC.KIT_CARDS.forEach(function(c){kk[c[0].split("-")[1]]=[c[2],c[3]]});
 var br=SPEC.BENCH_REGISTER.map(function(r){return {tag:r[0],item:r[1],model:r[2],loc:r[3],status:r[4],cust:r[5]}});
 return BENCH_PRE+"\nvar KITKEY="+JSON.stringify(kk)+";\nvar BREG="+JSON.stringify(br)+";"+BENCH_POST;
}
function rebuild(src,lid,setl){
 var L=SPEC.LABS[lid],meta=SPEC.LAB_META[lid],g=meta[0];
 var m=src.match(/<script id="lqData">var LQ=([\s\S]*?);\s*<\/script>/);if(!m)throw new Error("no LQ registry");
 var lq=JSON.parse(m[1]);if(lq.set==="-"||lq.set==="—"||lq.set==="–")lq.set="";var items=lq.items.filter(function(i){return !i.b});
 L.steps.forEach(function(st){if(st.cap==="text"||st.cap==="image")items.push({s:L.part,k:st.cap,p:st.t,b:1})});
 var lq2=Object.assign({},lq);lq2.items=items;
 src=src.slice(0,m.index)+'<script id="lqData">var LQ='+JSON.stringify(lq2)+';</script>'+src.slice(m.index+m[0].length);
 src=src.replace(/<span class="tag">~\d+ min<\/span>(<span class="tag">includes bench work<\/span>)?/,'<span class="tag">~'+L.minutes+' min</span><span class="tag">includes bench work</span>');
 if(src.indexOf("The <b>bench panel</b> near the bottom")<0)src=src.replace("<p>The simulator keeps its own record.",'<p>The <b>bench panel</b> near the bottom records the physical part of this lab at your station &mdash; scanner reads, ESD and PPE checks, labels you print, serials you seal. Press <b>Build bench record</b> when that part is done; it goes into the same PDF.</p><p>The simulator keeps its own record.');
 src=src.replace(/<!-- BENCH:START -->[\s\S]*?<!-- BENCH:END -->\n?/,"");
 var bh="<!-- BENCH:START -->"+benchHtml(lid,setl)+"<!-- BENCH:END -->\n</main>";src=src.replace("</main>",function(){return bh});
 src=src.replace(/<script id="benchScript">[\s\S]*?<\/script>\n?/,"");
 var marker="<!-- ===== Module 531 · Submission module";if(src.indexOf(marker)<0)throw new Error("no submission module");
 var bs='<script id="benchScript">var BENCH='+JSON.stringify({lab:g,set:setl,part:L.part})+';'+benchJs()+'</script>\n'+marker;src=src.replace(marker,function(){return bs});
 /* UI layer: simulator-record section ahead of the bench panel; style + progress script */
 var sw=src.match(/<section class="panel" id="sheetWrap">[\s\S]*?<\/section>\n?/);var bi=src.indexOf("<!-- BENCH:START -->");
 if(sw&&bi>0&&sw.index>bi){var sec=sw[0].replace(/\n$/,"")+"\n";src=src.slice(0,sw.index)+src.slice(sw.index+sw[0].length);src=src.replace("<!-- BENCH:START -->",function(){return sec+"<!-- BENCH:START -->"})}
 var he=src.indexOf('<script id="lqData">');src=src.slice(0,he).replace(/<h4>(.*?)<\/h4>/g,'<h3 class="h4">$1</h3>')+src.slice(he);
 src=src.replace(/<style id="uiLayer">[\s\S]*?<\/style>\n?/,"");var st='<style id="uiLayer">'+UI_CSS+'</style>\n</head>';src=src.replace("</head>",function(){return st});
 src=src.replace(/<script id="uiScript">[\s\S]*?<\/script>\n?/,"");var us='<script id="uiScript">'+UI_JS+'</script>\n'+marker;src=src.replace(marker,function(){return us});
 if(src.indexOf("<!-- Module 531 v")<0)src=src.replace("<head>","<head>\n<!-- Module 531 v"+SPEC.VERSION+" -->");
 return src;
}
/* ---- sources: fetch siblings (GitHub Pages / any server) or file picker (file://) ---- */
var SRC={};
function allFiles(){var out=[];SPEC.LAB_ORDER.forEach(function(lid){SPEC.LAB_META[lid][3].forEach(function(s){out.push([lid,s,toolFile(lid,s)])})});return out}
function log(msg,ok){var el=document.getElementById("log");var d=document.createElement("div");d.textContent=msg;if(ok===false)d.style.color="var(--bad)";if(ok===true)d.style.color="var(--ok)";el.appendChild(d);el.scrollTop=el.scrollHeight}
function fetchAll(){var fs=allFiles(),n=0;log("Fetching "+fs.length+" tools from this folder…");
 return Promise.all(fs.map(function(f){return fetch(f[2]).then(function(r){if(!r.ok)throw new Error(r.status);return r.text()}).then(function(t){SRC[f[2]]=t;n++}).catch(function(e){log("  "+f[2]+": not reachable ("+e.message+") — use the file picker if this page is open from disk",false)})})).then(function(){log(n+" of "+fs.length+" loaded.",n===fs.length);refresh()})}
function pickFiles(ev){var files=ev.target.files,n=0;Array.prototype.forEach.call(files,function(f){var rd=new FileReader();rd.onload=function(){SRC[f.name]=rd.result;n++;if(n===files.length){log(n+" file(s) loaded from disk.",true);refresh()}};rd.readAsText(f)})}
function refresh(){var fs=allFiles();var tb=document.getElementById("tools");tb.innerHTML=fs.map(function(f){var have=!!SRC[f[2]];return '<tr><td class="mono">'+f[2]+'</td><td>'+SPEC.LAB_META[f[0]][0]+'</td><td>'+(f[1]||"single")+'</td><td>'+(have?'<span class="ok">loaded</span>':'<span class="dim">—</span>')+'</td><td>'+(have?'<button class="small" onclick="buildOne(\''+f[0]+'\',\''+f[1]+'\')">Rebuild &amp; download</button> <button class="small" onclick="previewOne(\''+f[0]+'\',\''+f[1]+'\')">Preview</button>':"")+'</td></tr>'}).join("")}
var BUILT={};
function buildOne(lid,s){var fn=toolFile(lid,s);try{var out=rebuild(SRC[fn],lid,s);BUILT[fn]=out;download(fn,out);log("Built "+fn+" ("+out.length+" bytes)",true)}catch(e){log(fn+": "+e.message,false)}}
function previewOne(lid,s){var fn=toolFile(lid,s);try{var out=rebuild(SRC[fn],lid,s);var w=window.open("","_blank");w.document.write(out);w.document.close()}catch(e){log(fn+": "+e.message,false)}}
function buildAll(){var fs=allFiles(),ok=0;BUILT={};if(!Object.keys(SRC).length){log("No tools loaded yet — press Choose Files (section 1) and select the 29 tool files from this folder, or Load from this folder when the page is opened from the course website.",false);return 0}fs.forEach(function(f){if(!SRC[f[2]])return;try{BUILT[f[2]]=rebuild(SRC[f[2]],f[0],f[1]);ok++}catch(e){log(f[2]+": "+e.message,false)}});log("Rebuilt "+ok+" tool(s). Download the zip or individual files.",ok>0);return ok}
function download(name,text,type){var b=new Blob([text],{type:type||"text/html;charset=utf-8"});var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
/* store-only zip writer (no library) */
var CRC=(function(){var t=[];for(var n=0;n<256;n++){var c=n;for(var k=0;k<8;k++)c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0}return t})();
function crc32(u8){var c=0xFFFFFFFF;for(var i=0;i<u8.length;i++)c=CRC[(c^u8[i])&0xFF]^(c>>>8);return (c^0xFFFFFFFF)>>>0}
function zipFiles(entries){var enc=new TextEncoder(),parts=[],central=[],off=0;var now=new Date();var dt=((now.getHours()<<11)|(now.getMinutes()<<5)|(now.getSeconds()>>1))&0xFFFF,dd=(((now.getFullYear()-1980)<<9)|((now.getMonth()+1)<<5)|now.getDate())&0xFFFF;
 function u16(v){return [v&255,(v>>8)&255]}function u32(v){return [v&255,(v>>8)&255,(v>>16)&255,(v>>>24)&255]}
 entries.forEach(function(e){var name=enc.encode(e.name),data=enc.encode(e.text),crc=crc32(data);
  var lh=[].concat(u32(0x04034b50),u16(20),u16(0x0800),u16(0),u16(dt),u16(dd),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0));
  parts.push(new Uint8Array(lh),name,data);
  central.push([].concat(u32(0x02014b50),u16(20),u16(20),u16(0x0800),u16(0),u16(dt),u16(dd),u32(crc),u32(data.length),u32(data.length),u16(name.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(off)),name);
  off+=lh.length+name.length+data.length});
 var cstart=off,csize=0;central.forEach(function(c,i){if(i%2===0){parts.push(new Uint8Array(c));csize+=c.length}else{parts.push(c);csize+=c.length}});
 parts.push(new Uint8Array([].concat(u32(0x06054b50),u16(0),u16(0),u16(entries.length),u16(entries.length),u32(csize),u32(cstart),u16(0))));
 return new Blob(parts,{type:"application/zip"})}
function downloadZip(){if(!buildAll())return;var entries=Object.keys(BUILT).sort().map(function(k){return {name:"4_Lab_Tools/"+k,text:BUILT[k]}});var b=zipFiles(entries);var a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="Module531_lab_tools_v"+SPEC.VERSION+".zip";document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)}
/* ---- spec editor: a form bound to the definitions by path (LABS.1-2.steps.0.t)---- */
var SHIPPED=JSON.parse(JSON.stringify({LABS:SPEC.LABS,KIT:SPEC.KIT,BENCH_REGISTER:SPEC.BENCH_REGISTER,KIT_CARDS:SPEC.KIT_CARDS}));
var FTYPES={scan:"Scan (code pattern)",lookup:"Scan (bench register)",check:"Tick box",sel:"Choice list",text:"Text",num:"Number",fixed:"Printed value",issued:"Printed value + label",seq:"Scan sequence / count",rows:"Repeating rows"};
function inp(path,val,kind,extra){var v=val==null?"":val;extra=extra||"";
 if(kind==="num")return '<input type="number" data-path="'+path+'" data-kind="num" value="'+esc(v)+'" style="width:90px"'+extra+'>';
 if(kind==="lines")return '<textarea data-path="'+path+'" data-kind="lines" rows="'+Math.max(2,(v||[]).length)+'" style="min-height:0"'+extra+'>'+esc((v||[]).join("\n"))+'</textarea>';
 if(kind==="long")return '<textarea data-path="'+path+'" data-kind="text" rows="3" style="min-height:0"'+extra+'>'+esc(v)+'</textarea>';
 if(kind==="bool")return '<input type="checkbox" data-path="'+path+'" data-kind="bool"'+(v?" checked":"")+extra+'>';
 return '<input type="text" data-path="'+path+'" data-kind="text" value="'+esc(v)+'"'+extra+'>'}
function fieldForm(f,path){var h='<div class="fcard"><div class="frow"><div><label>Field id</label><span class="mono">'+esc(f.id)+'</span></div><div><label>Type</label><span>'+esc(FTYPES[f.type]||f.type)+'</span></div>'
 +'<div style="flex:2 1 260px"><label>Label the learner sees</label>'+inp(path+".label",f.label)+'</div>'
 +'<div style="flex:2 1 220px"><label>Hint under the field</label>'+inp(path+".hint",f.hint)+'</div>';
 if(f.type==="scan")h+='<div><label>Accepted code pattern</label>'+inp(path+".expect",f.expect,"text",' class="mono"')+'</div>';
 if(f.type==="text")h+='<div><label>Placeholder</label>'+inp(path+".ph",f.ph)+'</div>';
 if(f.type==="sel"){h+='<div style="flex:1 1 220px"><label>Choices (one per line)</label>'+inp(path+".opts",f.opts,"lines")+'</div>';if(f.want!=null)h+='<div><label>Expected choice</label>'+inp(path+".want",f.want)+'</div>';if(f.gate)h+='<div style="flex:1 1 220px"><label>Choices that fail the gate (one per line)</label>'+inp(path+".gate",f.gate,"lines")+'</div>'}
 if(f.type==="seq"){if(f.expect_qty!=null)h+='<div><label>Register quantity</label>'+inp(path+".expect_qty",f.expect_qty,"num")+'</div>';if(f.expect_order)h+='<div style="flex:1 1 220px"><label>Expected order (one code per line)</label>'+inp(path+".expect_order",f.expect_order,"lines")+'</div>'}
 if(f.type==="num")h+='<div><label>Tolerance</label>'+inp(path+".tol",f.tol,"num",' step="0.01"')+'</div>';
 if(f.type==="fixed"||f.type==="issued")h+=Object.keys(f.value_by_set||{}).map(function(k){return '<div><label>Value, set '+esc(k)+'</label>'+inp(path+".value_by_set."+k,f.value_by_set[k],"text",' class="mono"')+'</div>'}).join("");
 if(f.gate_el!=null)h+='<div><label>GATE badge</label>'+inp(path+".gate_el",f.gate_el,"bool")+'</div>';
 h+='</div>';
 if(f.type==="rows"){h+='<div class="frow"><div><label>Number of rows</label>'+inp(path+".n",f.n,"num")+'</div>'+(f.optional_from!=null?'<div><label>Rows optional from</label>'+inp(path+".optional_from",f.optional_from,"num")+'</div><div style="flex:1 1 220px"><label>Optional-row wording</label>'+inp(path+".opt_label",f.opt_label)+'</div>':"")+'</div><div class="sub">'+f.fields.map(function(sf,i){return fieldForm(sf,path+".fields."+i)}).join("")+'</div>'}
 return h+'</div>'}
function labForm(lid){var L=SPEC.LABS[lid],m=SPEC.LAB_META[lid],p="LABS."+lid;
 var h='<details data-lab="'+lid+'"><summary><b>'+esc(m[0])+'</b> — '+esc(m[1])+' <span class="dim">· '+L.minutes+' min, '+L.bench_min+' at the bench · '+L.steps.length+' bench steps · '+L.fields.length+' bench fields'+(L.gate?' · GATE':'')+'</span></summary><div class="labbody">'
 +'<div class="frow"><div><label>Lab minutes</label>'+inp(p+".minutes",L.minutes,"num")+'</div><div><label>Of which at the bench</label>'+inp(p+".bench_min",L.bench_min,"num")+'</div>'
 +'<div style="flex:2 1 300px"><label>Bench part heading</label>'+inp(p+".part",L.part)+'</div></div>'
 +'<div class="frow"><div style="flex:1 1 100%"><label>Kit at the station</label><div class="chks">'+SPEC.KIT.map(function(k){return '<label class="chk"><input type="checkbox" data-path="'+p+'.kit" data-kind="set" value="'+esc(k[0])+'"'+(L.kit.indexOf(k[0])>=0?" checked":"")+'> '+esc(k[0])+' <span class="dim">'+esc(SPEC.KIT_SHORT[k[0]]||"")+'</span></label>'}).join("")+'</div></div></div>'
 +'<div class="frow"><div style="flex:1 1 100%"><label>Bench introduction (handout and tool)</label>'+inp(p+".intro",L.intro,"long")+'</div></div>'
 +'<h4>Bench steps <span class="dim">— numbering continues the handout; "Question" steps become numbered questions</span></h4>'
 +L.steps.map(function(st,i){return '<div class="frow step"><div style="flex:1 1 520px"><label>Step '+(i+1)+' of the bench part</label>'+inp(p+".steps."+i+".t",st.t,"long")+'</div><div><label>Kind</label><select data-path="'+p+'.steps.'+i+'.cap" data-kind="text"><option value="rec"'+(st.cap==="rec"?" selected":"")+'>Recorded by the panel</option><option value="text"'+(st.cap==="text"?" selected":"")+'>Question (text)</option><option value="image"'+(st.cap==="image"?" selected":"")+'>Question (photo)</option></select></div></div>'}).join("")
 +'<h4>Bench fields</h4>'+L.fields.map(function(f,i){return fieldForm(f,p+".fields."+i)}).join("")
 +(L.gate_fail?'<div class="frow"><div style="flex:1 1 100%"><label>What fails the gate (one line each)</label>'+inp(p+".gate_fail",L.gate_fail,"lines")+'</div></div>':"")
 +'</div></details>';return h}
function tableForm(key,heads){var rows=SPEC[key];return '<details data-table="'+key+'"><summary><b>'+esc(heads[0])+'</b> <span class="dim">· '+rows.length+' rows</span></summary><table><thead><tr>'+heads[1].map(function(x){return "<th>"+esc(x)+"</th>"}).join("")+'</tr></thead><tbody>'
 +rows.map(function(r,i){return "<tr>"+r.map(function(c,j){return "<td>"+inp(key+"."+i+"."+j,c,"text",j===0?' class="mono"':"")+"</td>"}).join("")+"</tr>"}).join("")+'</tbody></table></details>'}
function renderSpecForm(){var open={};Array.prototype.forEach.call(document.querySelectorAll("#specForm details[open]"),function(d){open[d.getAttribute("data-lab")||d.getAttribute("data-table")]=1});
 document.getElementById("specForm").innerHTML=SPEC.LAB_ORDER.map(labForm).join("")
 +tableForm("KIT",["Kit list",["Code","Item","Quantity","Source","Used in"]])+tableForm("BENCH_REGISTER",["Bench register",["Tag","Item","Model","Location","Status","Custody"]])+tableForm("KIT_CARDS",["Kit cards (1.1 key: classification / handling)",["Card","Item","Classification","Handling"]]);
 Array.prototype.forEach.call(document.querySelectorAll("#specForm details"),function(d){if(open[d.getAttribute("data-lab")||d.getAttribute("data-table")])d.open=true});
}
function setPath(o,path,v){var ks=path.split(".");for(var i=0;i<ks.length-1;i++){o=o[ks[i]]}o[ks[ks.length-1]]=v}
function readForm(){var o=JSON.parse(JSON.stringify({LABS:SPEC.LABS,KIT:SPEC.KIT,BENCH_REGISTER:SPEC.BENCH_REGISTER,KIT_CARDS:SPEC.KIT_CARDS}));var sets={};
 Array.prototype.forEach.call(document.querySelectorAll("#specForm [data-path]"),function(e){var k=e.getAttribute("data-kind"),p=e.getAttribute("data-path"),v;
  if(k==="set"){sets[p]=sets[p]||[];if(e.checked)sets[p].push(e.value);return}
  if(k==="num"){v=e.value===""?null:+e.value;if(v==null)return}
  else if(k==="bool")v=e.checked;
  else if(k==="lines")v=e.value.split("\n").map(function(x){return x.trim()}).filter(Boolean);
  else v=e.value;
  if(k==="text"&&v===""&&/\.(hint|ph)$/.test(p))return;
  setPath(o,p,v)});
 Object.keys(sets).forEach(function(p){var old=(function(){var ks=p.split("."),x=o;ks.forEach(function(k){x=x&&x[k]});return x||[]})();setPath(o,p,old.filter(function(k){return sets[p].indexOf(k)>=0}).concat(sets[p].filter(function(k){return old.indexOf(k)<0})))});return o}
function specToEditor(){["LABS","KIT","BENCH_REGISTER","KIT_CARDS"].forEach(function(k){SPEC[k]=JSON.parse(JSON.stringify(SHIPPED[k]))});renderSpecForm();var o=document.getElementById("specOut");if(o){o.textContent="Editor reset to the shipped definitions (nothing applied yet).";o.style.color=""}}
function applySpec(){try{var o=readForm();["LABS","KIT","BENCH_REGISTER","KIT_CARDS"].forEach(function(k){if(o[k])SPEC[k]=o[k]});
 // step-number lockstep check: bench steps must continue the handout numbering — verified against the tool's registry at rebuild; here check contiguity
 SPEC.LAB_ORDER.forEach(function(lid){var L=SPEC.LABS[lid];var n=null;L.steps.forEach(function(st){var m=st.t.match(/^Step (\d+)\./);if(!m)throw new Error(lid+": every bench step starts 'Step N.'");if(n!==null&&+m[1]!==n+1)throw new Error(lid+": step numbers must be contiguous");n=+m[1]})});
 renderSpecForm();say("Applied. Now press Rebuild all (section 1), then export the handout bench parts (section 3) so the question numbering stays matched.",true);renderExports()}catch(e){say("Not applied: "+e.message,false)}}
function say(msg,ok){var o=document.getElementById("specOut");if(o){o.textContent=msg;o.style.color=ok?"var(--ok)":"var(--bad)"}log(msg,ok)}
/* ---- exports: handout bench parts, label sheet, kit summary ---- */
function qStart(lid){var fn=toolFile(lid,SPEC.LAB_META[lid][3][0]);var src=SRC[fn];if(!src)return null;var m=src.match(/<script id="lqData">var LQ=([\s\S]*?);\s*<\/script>/);var lq=JSON.parse(m[1]);return lq.items.filter(function(i){return !i.b}).length}
function handoutHtml(lid){var L=SPEC.LABS[lid],meta=SPEC.LAB_META[lid];var files=meta[3][0]===""?toolFile(lid,""):"531-"+lid+"-"+meta[3].join(" / ")+"_"+meta[2]+".html";var q=qStart(lid);var h='<h2>'+esc(meta[0]+" — "+meta[1])+'</h2><h3>'+esc(L.part)+'</h3><p>'+esc(L.intro)+'</p>';
 L.steps.forEach(function(st){h+='<p>'+esc(st.t)+'</p>';if(st.cap==="rec")h+='<p class="arrow">→ Recorded in the lab tool as you work.</p>';else{q=q===null?null:q+1;h+='<p class="arrow">→ '+(st.cap==="image"?"Attach your image as Q":"Answer this as Q")+(q===null?"?":q)+' in the lab tool ('+esc(files)+').</p>'}});
 if(q===null)h+='<p class="dim">(Load the tools to number the questions — numbering continues the tool registry.)</p>';return h}
function renderExports(){document.getElementById("handouts").innerHTML=SPEC.LAB_ORDER.map(handoutHtml).join("");
 var kit='<table><tr><th>ID</th><th>Item</th><th>Qty</th><th>Provided by</th><th>Used in</th></tr>'+SPEC.KIT.map(function(k){return '<tr>'+k.map(function(c){return '<td>'+esc(c)+'</td>'}).join("")+'</tr>'}).join("")+'</table>';
 kit+='<h3>Bench register</h3><table><tr><th>Tag</th><th>Item</th><th>Model</th><th>Register location</th><th>Status</th><th>Custody</th></tr>'+SPEC.BENCH_REGISTER.map(function(r){return '<tr>'+r.map(function(c){return '<td>'+esc(c)+'</td>'}).join("")+'</tr>'}).join("")+'</table>';
 kit+='<h3>Kit per lab</h3><table><tr><th>Lab</th><th>Bench part</th><th>Bench min</th><th>Kit</th></tr>'+SPEC.LAB_ORDER.map(function(lid){var L=SPEC.LABS[lid];return '<tr><td>'+SPEC.LAB_META[lid][0]+'</td><td>'+esc(L.part)+'</td><td>'+L.bench_min+'</td><td>'+esc(kitLine(lid))+'</td></tr>'}).join("")+'</table>';
 document.getElementById("kit").innerHTML=kit;}
function printSection(id,title){var w=window.open("","_blank");w.document.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>'+esc(title)+'</title><style>body{font-family:Calibri,Arial,sans-serif;color:#1A2B38;max-width:800px;margin:30px auto;line-height:1.45}h2{color:#1A2B38;font-size:18px;margin-top:28px}h3{color:#0079C0;font-size:14px}.arrow{color:#0079C0;font-style:italic;margin-left:18px;font-size:13px}table{border-collapse:collapse;font-size:12px;width:100%}td,th{border:1px solid #999;padding:4px 6px;text-align:left}th{background:#eaf2f8}</style></head><body>'+document.getElementById(id).innerHTML+'</body></html>');w.document.close()}
/* label sheet (Code 128 from the same table as the tools) */
function c128bits(text){var vals=[104];for(var i=0;i<text.length;i++){var c=text[i];if(!(c in C128B))c=" ";vals.push(C128B[c])}var sum=vals[0];for(var j=1;j<vals.length;j++)sum+=vals[j]*j;vals.push(sum%103);var bits="";vals.forEach(function(v){bits+=C128P[v]});return bits+C128P[106]+"11"}
function lblSvg(text){var bits=c128bits(text),w=2,h=44,W=bits.length*w+12,r="";for(var i=0;i<bits.length;i++)if(bits[i]==="1")r+='<rect x="'+(6+i*w)+'" y="0" width="'+w+'" height="'+h+'"/>';return '<svg viewBox="0 0 '+W+' '+h+'" preserveAspectRatio="xMidYMid meet" fill="#000">'+r+'</svg>'}
function lbl(code,l1,l2){return '<div class="lbl"><div class="t">'+esc(l1)+'</div>'+lblSvg(code)+'<div class="c">'+esc(code)+'</div>'+(l2?'<div class="s">'+esc(l2)+'</div>':"")+'</div>'}
function labelSheet(){var S=[];function sec(t,ls){S.push([t,ls])}var k=[];
 sec("§1 Station cards",Array.from({length:10},function(_,i){var n=("0"+(i+1)).slice(-2);return lbl("STN-"+n,"STATION CARD","Station "+(i+1))}));
 [["R640",4,"R640 server (cover model name)"],["PSU",4,"hot-swap PSU"],["FAN",4,"fan module"],["DRV",4,"drive carrier"],["RAIL",2,"rail kit"],["CAGE",4,"cage nuts + blanking panel"]].forEach(function(x){for(var n=1;n<=x[1];n++)k.push(lbl("KIT-"+x[0]+"-"+("0"+n).slice(-2),"KIT CARD · blind",x[2]))});
 for(var n=1;n<=10;n++)k.push(lbl("KIT-SCAN-"+("0"+n).slice(-2),"SCANNER","DS2208 · station "+n));for(n=1;n<=2;n++)k.push(lbl("KIT-CART-0"+n,"KIT CARD","platform cart "+n));sec("§2 Kit cards",k);
 sec("§3 Lifecycle cards",SPEC.LC_CODES.map(function(c,i){return lbl(c,"LIFECYCLE STAGE",SPEC.LC_STAGES[i])}));
 sec("§4 Bench register tags",SPEC.BENCH_REGISTER.map(function(r){return lbl(r[0],"MODULE 531 · ASSET TAG",r[1]+" · "+r[3])}));
 sec("§5 Drive tags",SPEC.DBD_TAGS.map(function(t){return lbl(t,"DATA-BEARING DEVICE","custody required · bag before moving")}));
 var b=[lbl("BIN-REDEPLOY","DISPOSITION BIN","Redeploy"),lbl("BIN-SCRAP","DISPOSITION BIN","Scrap"),lbl("BIN-DISPOSE","DISPOSITION BIN","Dispose")];for(n=1;n<=5;n++)b.push(lbl("ITEM-RAIL-0"+n,"SCRAP ACCESSORY","bent rail"));for(n=1;n<=5;n++)b.push(lbl("ITEM-PANEL-0"+n,"SCRAP ACCESSORY","damaged blanking panel"));sec("§6 Bin and scrap-accessory cards",b);
 var u=[];for(n=10;n<=30;n++)u.push(lbl("U-"+n,"RACK MIR-1","U"+n));sec("§7 Rack U labels",u);
 sec("§8 Pick cards",[lbl("INC0701","PICK CARD","1 × issued"),lbl("INC0702","PICK CARD","1 × issued")]);
 sec("§9 Spare learner-issue tags",[0,1,2].map(function(n){return lbl("ATL-0079"+n,"MODULE 531 · ASSET TAG","issued by the lab tool")}));
 var css="body{font-family:Arial,sans-serif;margin:0;color:#111}h2.sec{font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#0079C0;margin:0;padding:8px 0.19in 4px;page-break-before:always}.grid{display:grid;grid-template-columns:repeat(3,2.625in);column-gap:0.125in;padding:0 0.1875in}.lbl{width:2.625in;height:1in;box-sizing:border-box;padding:0.05in 0.1in;display:flex;flex-direction:column;align-items:center;justify-content:center;border:1px dashed #bbb;overflow:hidden}.lbl .t{font-size:7pt;letter-spacing:1px;color:#333;white-space:nowrap}.lbl svg{width:2.3in;height:0.36in;margin:2px 0}.lbl .c{font-family:Consolas,monospace;font-size:10.5pt;font-weight:700}.lbl .s{font-size:7.5pt;color:#333;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:2.4in}@page{size:letter;margin:0.5in 0 0.5in 0}@media print{.lbl{border-color:transparent}h2.sec{color:#999;font-size:9px;padding-top:0}}";
 var w=window.open("","_blank");w.document.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Module 531 — Bench label sheet</title><style>'+css+'</style></head><body>'+S.map(function(s){return '<h2 class="sec">'+esc(s[0])+'</h2><div class="grid">'+s[1].join("")+'</div>'}).join("")+'</body></html>');w.document.close()}
document.addEventListener("DOMContentLoaded",function(){renderSpecForm();refresh();renderExports();document.getElementById("picker").addEventListener("change",pickFiles);
 if(location.protocol!=="file:")fetchAll();else log("Opened from your computer: use Choose Files and select the {NT} tool files from this folder.")});
"""

CSS = """
:root{--bg:#0b1620;--panel:#132433;--panel2:#0f1d29;--line:#2c4a63;--ink:#dfeaf3;--dim:#a8c0d3;--faint:#9db6c9;--acc:#4fb3ef;--ok:#39c98e;--warn:#e8b64c;--bad:#e8604c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:14px;line-height:1.5}
#app{max-width:1080px;margin:0 auto;padding:22px 20px 60px}header.top{border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:18px}
.eyebrow{font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--faint);font-weight:700;margin-bottom:6px}h1{font-size:20px;margin:0 0 8px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:16px 18px;margin-bottom:18px;overflow-x:auto}
.panel>h2{font-size:12px;letter-spacing:1.2px;text-transform:uppercase;color:var(--acc);margin:0 0 12px}
.hint{font-size:12px;color:var(--faint)}.dim{color:var(--faint)}.ok{color:var(--ok);font-weight:700}
button{font-family:inherit;font-size:13px;cursor:pointer;border-radius:5px;border:1px solid var(--line);background:var(--panel);color:var(--ink);padding:8px 14px}button:hover{background:#20384f}
button.primary{background:#0079C0;border-color:#0079C0;color:#fff;font-weight:600}button.small{font-size:12px;padding:4px 10px}
table{width:100%;border-collapse:collapse;font-size:12.5px}th{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--faint);text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}td{padding:6px 8px;border-bottom:1px solid #22384c;vertical-align:top}
.mono{font-family:Consolas,monospace;font-size:12px}textarea{width:100%;min-height:260px;background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:5px;font-family:Consolas,monospace;font-size:12px;padding:8px}
#log{background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:8px 10px;font-family:Consolas,monospace;font-size:12px;max-height:180px;overflow:auto}
::selection{background:#0079C0;color:#fff}:focus-visible{outline:2px solid #8fd0ff;outline-offset:2px;border-radius:4px}*{scrollbar-color:#2c4a63 #0b1620;scrollbar-width:thin}
#specForm details{border:1px solid var(--line);border-radius:7px;margin:8px 0;background:var(--panel2)}#specForm summary{cursor:pointer;padding:10px 12px;font-size:13px}#specForm .labbody{padding:4px 12px 12px}
#specForm label{display:block;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--faint);font-weight:700;margin:6px 0 3px}#specForm .chk{display:inline-flex;align-items:center;gap:5px;text-transform:none;letter-spacing:0;font-size:12px;font-weight:400;color:var(--ink);margin:2px 12px 2px 0}
#specForm .frow{display:flex;flex-wrap:wrap;gap:6px 16px;align-items:flex-start}#specForm .frow>div{flex:1 1 160px;min-width:0}#specForm input[type=text],#specForm input[type=number],#specForm select,#specForm textarea{width:100%;box-sizing:border-box;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:6px 8px;font-family:inherit;font-size:12.5px}
#specForm .fcard{border:1px solid #22384c;border-radius:6px;padding:6px 10px 10px;margin:8px 0}#specForm .sub{margin-left:14px;border-left:2px solid #22384c;padding-left:10px}#specForm h4{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--acc);margin:14px 0 4px}#specForm td{padding:3px 4px}
.banner{border-left:3px solid var(--warn);background:#1a2431;padding:10px 14px;border-radius:6px;font-size:13px;color:var(--dim);margin-bottom:18px}
#handouts h2{font-size:14px;margin:16px 0 4px}#handouts h3{font-size:13px;color:var(--acc);margin:4px 0}#handouts p{margin:6px 0;font-size:13px}#handouts .arrow{color:var(--acc);font-style:italic;margin-left:18px;font-size:12px}
details summary{cursor:pointer;color:var(--acc);font-weight:600;margin:6px 0}
"""

def build():
    NT = sum(len(spec.LAB_META[l][3]) for l in spec.LAB_ORDER)
    BUILDER_JS_FINAL = BUILDER_JS.replace("{NT}", str(NT)).replace("</script>", "<\\/script>").replace("__SPEC__", SPEC_JSON).replace("__PRE__", js_str(PRE)).replace("__POST__", js_str(POST)).replace("__UICSS__", js_str(UI_CSS)).replace("__UIJS__", js_str(UI_JS))
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Module 531 — Lab Tool Builder (instructor tool)</title>
<!-- Module 531 v{VERSION} · Lab Tool Builder (instructor tool). Self-contained; loads the sibling lab tools from this folder when served. Contains no answer keys. -->
<style>{CSS}</style>
</head>
<body>
<div id="app">
<header class="top"><div class="eyebrow">{html.escape(COURSE)} &middot; instructor tool</div>
<h1>Lab Tool Builder</h1>
<p class="hint">Version {VERSION} &middot; {VDATE}. For instructors and course maintainers &mdash; not part of any lab. This page rebuilds the {NT} lab tools from the course's bench definitions, right here in the browser, and exports the matching handout text, the bench label sheet and a kit summary. Open it from the course website and it loads the tools from this folder; open it from your computer and choose the tool files with the button below.</p></header>
<div class="banner"><b>One source for questions.</b> Each handout and its lab tool share one list of questions. If you change a bench step or question here, rebuild the tools <i>and</i> export the handout bench parts, then paste the exported part over the handout's bench part. Do not edit a tool or a handout by hand. Answer keys are not on this page; they stay with the instructor materials.</div>

<section class="panel"><h2>1 &middot; Sources</h2>
<p class="hint">The {NT} lab tools from this folder. <input type="file" id="picker" multiple accept=".html"> <button class="small" onclick="fetchAll()">Load from this folder</button></p>
<table><thead><tr><th>File</th><th>Lab</th><th>Set</th><th>Source</th><th></th></tr></thead><tbody id="tools"></tbody></table>
<p><button class="primary" onclick="downloadZip()">Rebuild all &amp; download zip</button> <button onclick="buildAll()">Rebuild all (no download)</button></p>
<div id="log" aria-live="polite"></div></section>

<section class="panel"><h2>2 &middot; Bench definitions (steps, fields, kit, register)</h2>
<p class="hint">Open a lab, change what you need, press <b>Apply changes</b>, then <b>Rebuild all</b> in section 1. Field ids and types are fixed (they are what the answer keys and the handouts refer to); labels, hints, choices, code patterns, minutes, kit, introductions and step text are yours to edit. <span class="dim">Reference — field types: <code>scan</code> (<code>expect</code> = accepted code pattern, or <code>expect_field</code> = must match a printed value), <code>lookup</code> (bench register), <code>check</code>, <code>sel</code>, <code>text</code>, <code>num</code> (<code>compare</code> + <code>tol</code>), <code>fixed</code> / <code>issued</code> (<code>value_by_set</code>, <code>print</code>), <code>seq</code> (<code>expect_order</code> or <code>expect_qty</code> + <code>lock</code>), <code>rows</code> (<code>n</code>, <code>fields</code>, <code>optional_from</code>). Steps with <code>cap</code> "text" or "image" become numbered questions; "rec" steps are recorded by the panel.</span></p>
<div id="specForm"></div>
<p><button class="primary" onclick="applySpec()">Apply changes</button> <button onclick="specToEditor()">Reset to the shipped definitions</button> <span id="specOut" role="status" style="font-size:13px"></span></p></section>

<section class="panel"><h2>3 &middot; Exports</h2>
<p><button onclick="printSection('handouts','Module 531 — handout bench parts')">Open handout bench parts (print / copy)</button> <button onclick="labelSheet()">Open the bench label sheet</button> <button onclick="printSection('kit','Module 531 — kit summary')">Open the kit summary</button></p>
<details><summary>Handout bench parts (preview)</summary><div id="handouts"></div></details>
<details><summary>Kit summary (preview)</summary><div id="kit"></div></details></section>

<section class="panel"><h2>4 &middot; What this page does not cover</h2>
<p class="hint">Word, PowerPoint and Excel files (handouts, guide, rubrics, decks, quizzes) are produced by the course's full build, kept with the instructor materials. This page covers the learner tools and the HTML exports.</p></section>
</div>
<script>
{gen_tools.C128}
{BUILDER_JS_FINAL}
</script>
</body>
</html>"""
    open(os.path.join(OUT, "4_Lab_Tools", "531_Builder.html"), "w", encoding="utf-8").write(page)
    print("builder", len(page))

if __name__ == "__main__": build()
