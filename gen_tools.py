"""Regenerate the learner lab tools: bench panel + bench module, question registry regenerated from the
spec (existing scenario questions + bench questions). SRC may be a v1.2 package (no bench) or a v2.0+ package
(bench present) — a v2.0 source is stripped back to its scenario first, so the rebuild is idempotent."""
import re, json, os, sys, html
sys.path.insert(0, os.path.dirname(__file__))
import spec
from ui_layer import UI_CSS, UI_JS
from spec import LABS, LAB_META, LAB_ORDER, tool_file, tool_files_label, BENCH_REGISTER, VERSION, SRC_ID, subst

SRC = os.environ.get("SRC")
OUT = os.environ.get("OUT")
C128 = open(os.path.join(os.path.dirname(__file__), "c128table.js")).read()

def esc(s): return html.escape(str(s), quote=True)

def r640(s):
    s = s.replace("R630", "R640")
    s = s.replace("24 kg", "22 kg")           # R640 plate weight (team lift unchanged)
    # v2.1: no crusher on site — destruction is a vendor hand-over (scenario wording aligned)
    s = s.replace("A small locked room, a crusher, sealed bags on a shelf", "A small locked room, a DBD cage, sealed bags on a shelf")
    s = s.replace("e.g. DBD cage -> crusher; hazardous stream", "e.g. DBD cage -> destruction vendor; hazardous stream")
    return s

# ------------------------------------------------------------------ bench HTML
def field_html(f, prefix, lid):
    fid = prefix + f["id"]
    t = f["type"]; lab = ("<span class=\"gatetag\">GATE</span> " if f.get("gate_el") else "") + esc(f["label"]); hint = f.get("hint")
    h = ""
    if t in ("scan", "lookup"):
        h = f'<div><label for="{fid}">{lab}</label><input type="text" id="{fid}" class="scanin" autocomplete="off" spellcheck="false" data-b="{esc(json.dumps(f, separators=(",",":"), ensure_ascii=False))}"> <span id="{fid}_st" role="status" style="font-size:12px"></span></div>'
    elif t == "check":
        h = f'<div class="chk"><input type="checkbox" id="{fid}"><label for="{fid}">{lab}</label></div>'
    elif t == "sel":
        opts = "".join(f"<option>{esc(o)}</option>" for o in f["opts"])
        gate = (f' data-gate="{esc(json.dumps(f["gate"], separators=(",",":")))}"' if f.get("gate") else "") + (f' data-want="{esc(f["want"])}"' if f.get("want") else "")
        h = f'<div><label for="{fid}">{lab}</label><select id="{fid}"{gate}><option value="">&mdash; choose &mdash;</option>{opts}</select></div>'
    elif t == "text":
        ph = f' placeholder="{esc(f["ph"])}"' if f.get("ph") else ""
        h = f'<div><label for="{fid}">{lab}</label><input type="text" id="{fid}" size="22"{ph}></div>'
    elif t == "num":
        h = f'<div><label for="{fid}">{lab}</label><input type="number" id="{fid}" step="0.01" min="0" data-cmp="{esc(f.get("compare",""))}" data-tol="{f.get("tol",0)}"> <span id="{fid}_st" role="status" style="font-size:12px"></span></div>'
    elif t == "fixed":
        h = f'<div><label>{lab}</label><div class="mono" id="{fid}" style="padding:8px 0">{{VBS:{f["id"]}}}</div></div>'
    elif t == "issued":
        h = (f'<div><label>{lab}</label><div class="mono" id="{fid}" style="padding:8px 0">{{VBS:{f["id"]}}}</div>'
             + (f'<button class="small" type="button" onclick="benchPrint(\'{fid}\')">Print label</button>' if f.get("print") else "") + '</div>')
    elif t == "seq":
        h = (f'<div style="flex:1 1 100%"><label for="{fid}">{lab}</label>'
             f'<input type="text" id="{fid}" class="seqin" autocomplete="off" spellcheck="false" data-b="{esc(json.dumps(f, separators=(",",":"), ensure_ascii=False))}" placeholder="click here, then scan"> '
             f'<button class="small" type="button" onclick="benchSeqReset(\'{fid}\')">{"Restart count" if f.get("lock") else "Restart sequence"}</button> '
             + (f'<button class="small" type="button" id="{fid}_lock" onclick="benchSeqLock(\'{fid}\')">Lock count</button> ' if f.get("lock") else "")
             + f'<div id="{fid}_list" class="hint" style="margin-top:6px"></div><span id="{fid}_st" role="status" style="font-size:12px"></span></div>')
    if hint: h = h.replace("</div>", f'<div class="hint">{esc(hint)}</div></div>', 1) if t not in ("check",) else h
    return h

def bench_html(lid, setl):
    L = LABS[lid]
    parts = []; loose = []
    def flush():
        if loose: parts.append('<div class="frow">' + "".join(loose) + '</div>'); loose.clear()
    for f in L["fields"]:
        if f["type"] == "rows":
            flush()
            for r in range(1, f["n"] + 1):
                opt = f.get("optional_from") and r >= f["optional_from"]
                inner = "".join(field_html(sf, f"b_{f['id']}_{r}_", lid) for sf in f["fields"])
                da = ' data-opt="1"' if opt else ""; sfx = (" — " + f.get("opt_label", "leave blank if unused")) if opt else ""
                parts.append(f'<div class="card"{da}><h4>{esc(f["label"])} {r}{sfx}</h4><div class="frow">{inner}</div></div>')
        elif f["type"] in ("seq",):
            flush(); parts.append(f'<div class="card"><h4>{esc(f["label"].split(" — ")[0])}</h4><div class="frow">' + field_html(f, "b_", lid) + '</div></div>')
        else:
            loose.append(field_html(f, "b_", lid))
    flush()
    body = "".join(parts)
    # substitute set values
    def sub(m):
        fid = m.group(1)
        for f in L["fields"]:
            if f["id"] == fid: return esc(f["value_by_set"].get(setl or "A", f["value_by_set"].get("A")))
        return ""
    body = re.sub(r"\{VBS:([a-z0-9]+)\}", sub, body)
    part = esc(L["part"])
    gatebox = ('<div class="card gatebox"><h4>What fails the gate</h4><ul>' + "".join(f"<li>{esc(x)}</li>" for x in L["gate_fail"]) + '</ul><p class="hint">Fields marked GATE are the ones the gate reads. Everything else is scored on the rubric.</p></div>') if L.get("gate_fail") else ""
    return (f'<section class="panel" id="benchPanel"><h2>Bench panel &mdash; {part}</h2>'
            f'<p class="hint">Your hands-on work at the station, recorded here. Click into a scan field and scan &mdash; the scanner types the code and presses Enter for you. '
            f'Green means the tool read what it expected and moves you to the next field; red tells you what to check &mdash; fix it, then scan again. At your station: {esc(kit_line(lid))}.</p>{gatebox}{body}'
            f'<p><button class="primary" type="button" onclick="buildBench()">Build bench record</button> '
            f'<span id="benchStatus" role="status" style="font-size:12px"></span></p><div id="benchOut" aria-live="polite"></div></section>')

def kit_line(lid):
    names = {k[0]: k[1] for k in spec.KIT}
    short = {"SCAN":"DS2208 scanner","PRN":"ZD621 label printer","ESD":"ESD mat + wrist strap","R640":"R640 server","FRU":"R640 FRU set","RACK":"rack accessories","CART":"platform cart","RCV":"receiving props (pallet, bin, scale)","PPE":"PPE set","PKG":"packaging kit","HDD":"scrap drives (mock DBDs)","ASB":"anti-static bags","SEC":"serialized security bags","COC":"custody logbook","SW":"Snipe-IT demo"}
    return ", ".join(short[k] for k in LABS[lid]["kit"])

# ------------------------------------------------------------------ bench JS
BENCH_PRE = r"""
/* ===== Module 531 v2.0 · Bench module ===================================================
   Records the physical work at the station: scanner input (DS2208 keyboard-wedge), ESD/PPE
   checkpoints, scale readings, sequences and per-item rows. Validates against the bench
   register and the expected code formats; prints labels for the ZD621 (Code 128); builds a
   .sheet record that the submission module harvests into the PDF. No network calls.
   ========================================================================================= */
""" + C128
KITKEY_JSON = json.dumps({c.split("-")[1]: [cls, hd] for c, what, cls, hd in spec.KIT_CARDS}, separators=(",",":"), ensure_ascii=False)
BREG_JSON = json.dumps([dict(tag=t,item=i,model=m,loc=l,status=s,cust=c) for t,i,m,l,s,c in BENCH_REGISTER], separators=(",",":"), ensure_ascii=False)
BENCH_POST = r"""
function bEsc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}
function bSet(k,v){SIM["b:"+k]=v;simSave()}
function bGet(k){return SIM["b:"+k]}
function bMark(el,ok,msg){var st=$(el.id+"_st");if(!st)return;st.innerHTML=ok===null?'':(ok==="warn"?'<span class="warnmark">FLAG &mdash; '+bEsc(msg)+'</span>':(ok?'<span class="okmark">OK &mdash; '+bEsc(msg)+'</span>':'<span class="badmark">CHECK &mdash; '+bEsc(msg)+'</span>'));bSet("ok:"+el.id,ok)}
function bRowOf(id){var m=id.match(/^b_([a-z]+)_(\d+)_/);return m?{grp:m[1],row:m[2]}:null}
function benchValidate(el){
 var cfg={};try{cfg=JSON.parse(el.getAttribute("data-b")||"{}")}catch(e){}
 var v=(el.value||"").trim();
 if(!v){bMark(el,null,"");return}
 if(cfg.type==="lookup"){
  var rec=null;for(var i=0;i<BREG.length;i++)if(BREG[i].tag.toUpperCase()===v.toUpperCase())rec=BREG[i];
  if(rec){el.value=rec.tag;bMark(el,true,rec.item+" · "+rec.model+" · register location "+rec.loc+" · "+rec.status+" · custody "+rec.cust)}
  else bMark(el,false,"not in the bench register (ATL-009xx tags only)");
  return;
 }
 if(cfg.expect_field){var ref=$("b_"+cfg.expect_field);var want=ref?ref.textContent.trim():"";
  bMark(el,v.toUpperCase()===want.toUpperCase(),v.toUpperCase()===want.toUpperCase()?"reads "+want:"read "+v+", expected "+want);return}
 var ok=true,msg="format accepted";
 if(cfg.expect){try{ok=new RegExp(cfg.expect,"i").test(v)}catch(e){ok=true}if(ok&&/^[A-Z][A-Z0-9-]*$/i.test(v)&&v!==v.toUpperCase()){el.value=v.toUpperCase();v=el.value}if(!ok)msg="'"+v+"' is not the code this field expects — scan the card or tag named in the label, not another one"}
 if(ok&&cfg.unique){var r=bRowOf(el.id);var sub=el.id.replace(/^b_[a-z]+_\d+_/,"");
  var all=document.querySelectorAll('input[id^="b_'+(r?r.grp:"")+'_"][id$="_'+sub+'"]');
  Array.prototype.forEach.call(all,function(o){if(o!==el&&(o.value||"").trim().toUpperCase()===v.toUpperCase()){ok=false;msg="'"+v+"' is already recorded in another row"}})}
 if(ok&&cfg.kitkey){var rk=bRowOf(el.id);var pre=(v.toUpperCase().split("-")[1]||"");var key=KITKEY[pre];var cs=$("b_"+rk.grp+"_"+rk.row+"_cls"),hs=$("b_"+rk.grp+"_"+rk.row+"_hd");
  if(key){if(!cs.value||!hs.value){ok="warn";msg="card read — now classify the item and set its handling"}
   else{msg="card read, classification and handling recorded — checked when you build the bench record"}}}
 if(ok&&cfg.match_path){var r2=bRowOf(el.id);var p=$("b_"+r2.grp+"_"+r2.row+"_path");var pv=p?p.value:"";
  if(pv){var want2="BIN-"+pv.toUpperCase();if(v.toUpperCase()!==want2){ok=false;msg="bin "+v+" does not match the path "+pv}else msg="bin matches the path "+pv}}
 bMark(el,ok,msg);
}
function benchNum(el){var cmp=el.getAttribute("data-cmp"),tol=parseFloat(el.getAttribute("data-tol")||"0");var ref=$("b_"+cmp);if(!ref)return;
 var d=parseFloat(ref.textContent),v=parseFloat(el.value);if(isNaN(v)){bMark(el,null,"");return}
 var diff=Math.round((v-d)*100)/100;var ok=Math.abs(diff)<=tol;bMark(el,ok?true:"warn",ok?"within "+tol+" kg of the declared weight":"differs from declared by "+diff+" kg — open and count before anything else")}
/* sequences */
function bSeqKey(id){return "seq:"+id}
function benchSeqRender(id){var el=$(id);var cfg={};try{cfg=JSON.parse(el.getAttribute("data-b")||"{}")}catch(e){}
 var st=bGet(bSeqKey(id))||{list:[],attempts:1,locked:false};
 var list=$(id+"_list");list.innerHTML=(st.list.length?st.list.map(function(c,i){return (i+1)+". <span class='mono'>"+bEsc(c)+"</span>"}).join(" &nbsp;·&nbsp; "):"<i>nothing scanned yet</i>")+" &nbsp;(attempt "+st.attempts+(st.locked?", locked":"")+")";
 var s=$(id+"_st");
 if(cfg.expect_order){var want=cfg.expect_order;var n=st.list.length;var okSoFar=true;for(var i=0;i<n;i++)if(st.list[i]!==want[i])okSoFar=false;
  if(n===0)s.innerHTML="";else if(!okSoFar)s.innerHTML='<span class="badmark">Out of order at position '+(st.list.findIndex(function(c,i){return c!==want[i]})+1)+' &mdash; restart the sequence.</span>';
  else if(n===want.length)s.innerHTML='<span class="okmark">Sequence complete and correct.</span>';else s.innerHTML='<span class="warnmark">'+n+' of '+want.length+' in order so far.</span>';
  bSet("ok:"+id,okSoFar&&n===want.length)}
 if(cfg.expect_qty!=null){if(st.locked){var v=st.list.length-cfg.expect_qty;s.innerHTML='Counted <b>'+st.list.length+'</b> · register quantity <b>'+cfg.expect_qty+'</b> · variance <b>'+(v>0?"+":"")+v+'</b>'+(v?' <span class="warnmark">&mdash; investigate.</span>':' <span class="okmark">&mdash; agrees.</span>');
   var lk=$(id+"_lock");if(lk)lk.disabled=true;el.disabled=true;bSet("ok:"+id,true)}else{s.innerHTML='<span class="hint">'+st.list.length+' scanned. Lock the count to reveal the register quantity.</span>';bSet("ok:"+id,false)}}
}
function benchSeqAdd(el){var id=el.id;var v=(el.value||"").trim();el.value="";if(!v)return;var st=bGet(bSeqKey(id))||{list:[],attempts:1,locked:false};
 if(st.locked){$(id+"_st").innerHTML='<span class="badmark">Count is locked &mdash; press Restart count to count again.</span>';return}
 var cfgA={};try{cfgA=JSON.parse(el.getAttribute("data-b")||"{}")}catch(e){}
 if(cfgA.expect_order&&st.list.length>=cfgA.expect_order.length){$(id+"_st").innerHTML='<span class="okmark">Sequence already complete &mdash; extra scan ignored.</span>';return}
 if(st.list.indexOf(v.toUpperCase())>=0){$(id+"_st").innerHTML='<span class="badmark">'+bEsc(v)+' is already in the list &mdash; duplicate scan rejected.</span>';return}
 st.list.push(v.toUpperCase());bSet(bSeqKey(id),st);benchSeqRender(id)}
function benchSeqReset(id){var st=bGet(bSeqKey(id))||{list:[],attempts:0,locked:false};st={list:[],attempts:(st.attempts||0)+1,locked:false};bSet(bSeqKey(id),st);var el=$(id);el.disabled=false;var lk=$(id+"_lock");if(lk)lk.disabled=false;benchSeqRender(id)}
function benchSeqLock(id){var st=bGet(bSeqKey(id))||{list:[],attempts:1,locked:false};if(!st.list.length){$(id+"_st").innerHTML='<span class="badmark">Scan every item before locking.</span>';return}st.locked=true;bSet(bSeqKey(id),st);benchSeqRender(id)}
/* Code 128 (subset B) label printing for the ZD621 */
function c128svg(text,h){var vals=[104];for(var i=0;i<text.length;i++){var c=text[i];if(!(c in C128B))c=" ";vals.push(C128B[c])}
 var sum=vals[0];for(var j=1;j<vals.length;j++)sum+=vals[j]*j;vals.push(sum%103);
 var bits="";vals.forEach(function(v){bits+=C128P[v]});bits+=C128P[106]+"11";
 var x=0,w=2,out='<svg xmlns="http://www.w3.org/2000/svg" width="'+(bits.length*w+20)+'" height="'+h+'" viewBox="0 0 '+(bits.length*w+20)+' '+h+'">';
 for(var k=0;k<bits.length;k++){if(bits[k]==="1")out+='<rect x="'+(10+x)+'" y="0" width="'+w+'" height="'+h+'" fill="#000"/>';x+=w}
 return out+"</svg>"}
function benchPrint(fid){var el=$(fid);if(!el)return;var code=el.textContent.trim();var lab=el.parentNode.querySelector("label");var title=lab?lab.textContent:"";
 var w=window.open("","_blank","width=520,height=320");if(!w){var bs0=$("benchStatus");if(bs0){bs0.textContent="The label window was blocked. Allow pop-ups for this file (the icon at the right end of the address bar), then press Print label again.";bs0.style.color="var(--bad)"}return}
 w.document.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>'+bEsc(code)+'</title><style>@page{size:2in 1in;margin:0.05in}body{margin:0;font-family:Arial,sans-serif;text-align:center}.lbl{width:1.9in;height:0.9in;display:flex;flex-direction:column;justify-content:center;align-items:center}.t{font-size:7pt;letter-spacing:0.5px}.c{font-size:11pt;font-weight:700;font-family:Consolas,monospace}svg{width:1.8in;height:0.42in}.np{font-size:9pt;margin:8px}@media print{.np{display:none}}</style></head><body><div class="lbl"><div class="t">MODULE 531 · '+bEsc(title.toUpperCase().slice(0,38))+'</div>'+c128svg(code,60)+'<div class="c">'+bEsc(code)+'</div></div><div class="np">Print to the Zebra ZD621 (2 x 1 in label) or any printer. <button onclick="window.print()">Print</button></div></body></html>');
 w.document.close();bSet("printed:"+fid,(bGet("printed:"+fid)||0)+1)}
/* record */
function benchLabel(id){var l=document.querySelector('label[for="'+id+'"]');if(l)return l.textContent;var el=$(id);var p=el&&el.parentNode.querySelector("label");return p?p.textContent:id}
function benchNext(el){var all=document.querySelectorAll("#benchPanel input.scanin,#benchPanel input.seqin");var seen=false;for(var i=0;i<all.length;i++){if(all[i]===el){seen=true;continue}if(seen&&!all[i].disabled&&!(all[i].value||"").trim()){all[i].focus();return}}}
function benchTouched(){var t=false;Array.prototype.forEach.call(document.querySelectorAll("#benchPanel input,#benchPanel select"),function(e){if(e.type==="checkbox"?e.checked:(e.value||"").trim())t=true});Object.keys(SIM).forEach(function(k){if(k.indexOf("b:seq:")===0&&SIM[k]&&SIM[k].list&&SIM[k].list.length)t=true});return t}
function buildBench(){
 var rows=[],miss=0,gate=0;var items=[];
 var els=document.querySelectorAll("#benchPanel input[id], #benchPanel select[id], #benchPanel div.mono[id]");
 Array.prototype.forEach.call(els,function(e){
  if(e.classList&&e.classList.contains("seqin")){var st=bGet(bSeqKey(e.id))||{list:[],attempts:1,locked:false};var cfg={};try{cfg=JSON.parse(e.getAttribute("data-b")||"{}")}catch(x){}
   var ok=bGet("ok:"+e.id);var txt=st.list.join(" → ")+" (attempt "+st.attempts+(st.locked?", locked":"")+")";
   if(cfg.expect_qty!=null&&st.locked)txt+=" · counted "+st.list.length+" vs register "+cfg.expect_qty;
   if(!st.list.length||ok===false)miss++;
   items.push([benchLabel(e.id),st.list.length?bEsc(txt):'<span style="color:var(--bad)">— not recorded —</span>',ok===true?'<span class="okmark">OK</span>':(ok===false?'<span class="badmark">check</span>':'')]);return}
  var v=e.tagName==="DIV"?e.textContent.trim():(e.type==="checkbox"?(e.checked?"yes":""):(e.value||"").trim());
  var r=bRowOf(e.id);var optional=false;
  var card=r?e.closest(".card"):null,head=card?card.querySelector("h4,.h4"):null;
  if(r){optional=!!(card&&card.getAttribute("data-opt"))&&!Array.prototype.some.call(card.querySelectorAll("input[type=text],select"),function(x){return (x.value||"").trim()})}
  var ok2=bGet("ok:"+e.id);
  var g=e.getAttribute?e.getAttribute("data-gate"):null;if(g&&v){try{if(JSON.parse(g).indexOf(v)>=0){ok2=false;gate++}}catch(x){}}
  var want=e.getAttribute?e.getAttribute("data-want"):null;var note="";if(want&&v&&v!==want){ok2=false;note=" — expected "+want}
  var cfgb={};try{cfgb=JSON.parse(e.getAttribute("data-b")||"{}")}catch(x){}
  if(cfgb.kitkey&&v&&ok2!==false){var rk=bRowOf(e.id);var key=KITKEY[(v.toUpperCase().split("-")[1]||"")];var cs=$("b_"+rk.grp+"_"+rk.row+"_cls"),hs=$("b_"+rk.grp+"_"+rk.row+"_hd");
   if(key&&cs&&hs&&cs.value&&hs.value&&(cs.value!==key[0]||hs.value!==key[1])){ok2=false;note=" — "+(cs.value!==key[0]?"classification does not fit this item":"")+(cs.value!==key[0]&&hs.value!==key[1]?"; ":"")+(hs.value!==key[1]?"handling requirement does not fit this item":"")}}
  if(cfgb.same&&v){var rs=bRowOf(e.id);var sub2=e.id.replace(/^b_[a-z]+_\d+_/,"");var vals=[];Array.prototype.forEach.call(document.querySelectorAll('input[id^="b_'+rs.grp+'_"][id$="_'+sub2+'"]'),function(o){var ov=(o.value||"").trim().toUpperCase();if(ov&&vals.indexOf(ov)<0)vals.push(ov)});if(vals.length>1){ok2=false;note=" — the same tag must be on every row"}}
  if(!v&&!optional)miss++;if(ok2===false)miss++;
  var lbl=(head?(head.textContent.replace(/\s*—\s*(only if|leave blank).*$/,"")+" — "):"")+benchLabel(e.id);
  items.push([bEsc(lbl),v?bEsc(v)+bEsc(note):(optional?'<i>(not used)</i>':'<span style="color:var(--bad)">— not recorded —</span>'),ok2===true?'<span class="okmark">OK</span>':(ok2===false?'<span class="badmark">check</span>':(ok2==="warn"?'<span class="warnmark">flagged</span>':''))]);
 });
 var printed=Object.keys(SIM).filter(function(k){return k.indexOf("b:printed:")===0}).map(function(k){return k.replace("b:printed:b_","")+" ×"+SIM[k]}).join(", ");
 $("benchOut").innerHTML='<section class="sheet"><h3>Bench record &mdash; '+bEsc(BENCH.part)+(BENCH.set?' (Set '+bEsc(BENCH.set)+')':'')+'</h3>'+tbl(["Field","Recorded","Check"],items)+(printed?'<p class="hint">Labels printed: '+bEsc(printed)+'</p>':'')+(gate?'<p class="badmark">A choice above fails the gate: the gate passes only a sealed bag whose serial was recorded at sealing. Fix it at the bench, then build the record again.</p>':'')+(miss?'<p class="badmark">'+miss+' bench item(s) missing or failing their check.</p>':'<p class="okmark">Bench record complete.</p>')+'</section>';
 var bs=$("benchStatus");if(bs){bs.textContent=miss?miss+" incomplete.":"Bench record built.";bs.style.color=miss?"var(--bad)":"var(--ok)"}
}
document.addEventListener("DOMContentLoaded",function(){
 var p=$("benchPanel");if(!p)return;
 Array.prototype.forEach.call(p.querySelectorAll("input.scanin"),function(e){e.addEventListener("change",function(){benchValidate(e)});e.addEventListener("keydown",function(ev){if(ev.key==="Enter"){ev.preventDefault();benchValidate(e);if(bGet("ok:"+e.id)!==false)benchNext(e)}});if(e.value)benchValidate(e)});
 Array.prototype.forEach.call(p.querySelectorAll("input.seqin"),function(e){e.addEventListener("keydown",function(ev){if(ev.key==="Enter"){ev.preventDefault();benchSeqAdd(e)}});e.addEventListener("change",function(){benchSeqAdd(e)});benchSeqRender(e.id)});
 Array.prototype.forEach.call(p.querySelectorAll("input[type=number]"),function(e){e.addEventListener("input",function(){benchNum(e)});if(e.value)benchNum(e)});
 Array.prototype.forEach.call(p.querySelectorAll("select"),function(e){e.addEventListener("change",function(){var r=bRowOf(e.id);if(r){var b=$("b_"+r.grp+"_"+r.row+"_bin");if(b&&b.value)benchValidate(b);var c=$("b_"+r.grp+"_"+r.row+"_code");if(c&&c.value)benchValidate(c)}})});
 var _bs=window.buildSheet;if(typeof _bs==="function")window.buildSheet=function(){_bs();if(benchTouched())buildBench()};
});
"""

BENCH_JS = BENCH_PRE + "\nvar KITKEY=" + KITKEY_JSON + ";\nvar BREG=" + BREG_JSON + ";" + BENCH_POST

def build_lq(lq, lid, setl):
    L = LABS[lid]
    items = [dict(i) for i in lq["items"]]
    for st in L["steps"]:
        if st["cap"] in ("text", "image"):
            items.append({"s": L["part"], "k": st["cap"], "p": st["t"], "b": 1})
    lq = dict(lq); lq["items"] = items
    for k in ("title", "handout"): lq[k] = r640(lq[k])
    return lq

def apply_ui_layer(s):
    m = re.search(r'<section class="panel" id="sheetWrap">.*?</section>\n?', s, re.S)
    if m and s.find("<!-- BENCH:START -->") > 0 and m.start() > s.find("<!-- BENCH:START -->"):
        sec = m.group(0).rstrip("\n") + "\n"
        s = s[:m.start()] + s[m.end():]
        s = s.replace("<!-- BENCH:START -->", sec + "<!-- BENCH:START -->", 1)
    head_end = s.find("<script id=\"lqData\">")
    body_html = re.sub(r'<h4>(.*?)</h4>', r'<h3 class="h4">\1</h3>', s[:head_end])
    s = body_html + s[head_end:]
    s = re.sub(r'<style id="uiLayer">.*?</style>\n?', "", s, flags=re.S)
    s = s.replace("</head>", '<style id="uiLayer">' + UI_CSS + '</style>\n</head>', 1)
    s = re.sub(r'<script id="uiScript">.*?</script>\n?', "", s, flags=re.S)
    marker = "<!-- ===== Module 531 · Submission module"
    s = s.replace(marker, '<script id="uiScript">' + UI_JS + '</script>\n' + marker, 1)
    return s

SUB_OLD = re.compile(r"var rec=LQ\.nosim\?null:toolRecord\(\);.*?records that sign-off\.</span></div>';\n    }", re.S)
SUB_NEW = """var bo=document.getElementById("benchOut");
    var rec=toolRecord();
    var simBuilt=!!LQ.nosim||Array.prototype.some.call(document.querySelectorAll(REC_SEL),function(x){return !card.contains(x)&&!(bo&&bo.contains(x))&&!!x.textContent.replace(/\\s/g,"")});
    if(rec){ h+='<h2>'+(LQ.nosim?'Bench record':'Simulator and bench record')+'</h2>'+rec; }
    if(!simBuilt){
      gaps.push("The simulator record — work through the lab tool above and press its own "
               +"“Build submission sheet” button before you build this PDF");
    }
    if(bo){
      if(!bo.querySelector(".sheet")) gaps.push("The bench record — press Build bench record in the bench panel");
      else{ var bm=bo.querySelector("p.badmark"); if(bm) gaps.push("Bench record: "+bm.textContent.trim().replace(/\\.$/,"")); }
    }
    var so=document.getElementById("sheetOut"); if(so){ var sm=so.querySelector("p.badmark"); if(sm) gaps.push("Simulator record: "+sm.textContent.trim().replace(/\\.$/,"")); }"""
def patch_submission(s):
    """v2.1 learner audit: every lab's PDF carries the bench record; bench misses are completeness gaps."""
    s = SUB_OLD.sub(lambda m: SUB_NEW, s, count=1)
    s = s.replace("and the simulator record is attached.", "and the record of your work is attached.")
    if "single build" not in s: s = s.replace("' · Set '+esc(setLetter())", "(setLetter()===\"—\"?' · single build':' · Set '+esc(setLetter()))")
    s = s.replace("if(card.contains(s)) return;", "if(card.contains(s)||s.closest(\"#lqPrint\")) return;")   # the hidden print copy is not a source
    return s.replace('<span class="v">'+"'+esc(setLetter())+'"+'</span>', '<span class="v">'+"'+(setLetter()===\"—\"?\"single build\":esc(setLetter()))+'"+'</span>')

def strip_v20(s):
    """Remove what a v2.0+ build added so the source reads like its v1.2 scenario tool."""
    s = re.sub(r"<!-- BENCH:START -->[\s\S]*?<!-- BENCH:END -->\n?", "", s)
    s = re.sub(r'<script id="benchScript">[\s\S]*?</script>\n?', "", s)
    s = s.replace('<p>The <b>bench panel</b> near the bottom records the physical part of this lab at your station &mdash; scanner reads, ESD and PPE checks, labels you print, serials you seal. Press <b>Build bench record</b> when that part is done; it goes into the same PDF.</p>', "", 1)
    s = re.sub(r"<head>\n<!-- Module 531 v[0-9.]+ -->", "<head>", s, count=1)
    return s

def process(lid, setl):
    g, title, slug, sets, les = LAB_META[lid]
    L = LABS[lid]
    fn = tool_file(lid, setl)
    src_fn = f"531-{SRC_ID.get(lid, lid)}{('-'+setl) if setl else ''}_{slug}.html"
    s = subst(strip_v20(open(os.path.join(SRC, "4_Lab_Tools", src_fn), encoding="utf-8").read()))
    m = re.search(r'<script id="lqData">var LQ=(.*?);\s*</script>', s, re.S)
    lq = json.loads(m.group(1))
    lq["items"] = [i for i in lq["items"] if not i.get("b")]      # drop bench items from a v2.0 source
    if lq.get("set") in ("-", "—", "–"): lq["set"] = ""            # single-build lab: no set letter anywhere (not "Set -")
    s = s.replace('var SETLETTER="-";', 'var SETLETTER="";').replace('var SETLETTER="—";', 'var SETLETTER="";')
    for k in ("title", "handout", "file", "lab"):
        if isinstance(lq.get(k), str): lq[k] = subst(lq[k])
    n_old = len(lq["items"])
    # step-number sanity: bench steps continue the handout numbering (checked in gen_handouts)
    lq2 = build_lq(lq, lid, setl)
    s = s[:m.start()] + '<script id="lqData">var LQ=' + json.dumps(lq2, separators=(",",":"), ensure_ascii=False) + ';</script>' + s[m.end():]
    # time tag + bench tag
    s = re.sub(r'<span class="tag">~\d+ min</span>(<span class="tag">includes bench work</span>)?', f'<span class="tag">~{L["minutes"]} min</span><span class="tag">includes bench work</span>', s, count=1)
    # brief
    s = s.replace('<p>The simulator keeps its own record.',
                  '<p>The <b>bench panel</b> near the bottom records the physical part of this lab at your station &mdash; scanner reads, ESD and PPE checks, labels you print, serials you seal. Press <b>Build bench record</b> when that part is done; it goes into the same PDF.</p><p>The simulator keeps its own record.', 1)
    # bench panel before </main>
    bh = bench_html(lid, setl)
    assert s.count("</main>") == 1, fn
    s = s.replace("</main>", "<!-- BENCH:START -->" + bh + "<!-- BENCH:END -->\n</main>", 1)
    # bench script before the submission module comment
    marker = "<!-- ===== Module 531 · Submission module"
    assert marker in s, fn
    bcfg = json.dumps({"lab": g, "set": setl, "part": L["part"]}, separators=(",",":"), ensure_ascii=False)
    s = s.replace(marker, f'<script id="benchScript">var BENCH={bcfg};{BENCH_JS}</script>\n' + marker, 1)
    # v2.1 UI layer: simulator-record section moves ahead of the bench panel; style + progress script
    s = apply_ui_layer(s)
    s = patch_submission(s)
    # R640 alignment + generator stamp
    s = r640(s)
    s = s.replace("<head>", "<head>\n<!-- Module 531 v" + VERSION + " -->", 1)
    out = os.path.join(OUT, "4_Lab_Tools", fn)
    open(out, "w", encoding="utf-8").write(s)
    return n_old, len(lq2["items"])

def main():
    os.makedirs(os.path.join(OUT, "4_Lab_Tools"), exist_ok=True)
    report = {}
    for lid in LAB_ORDER:
        for setl in LAB_META[lid][3]:
            report[tool_file(lid, setl)] = process(lid, setl)
    json.dump(report, open(os.path.join(OUT, "..", "tools_report.json"), "w"), indent=1)
    print("tools:", len(report))

if __name__ == "__main__": main()
