"""v2.1 UI layer shared by gen_tools.py (Python build) and 531_Builder.html (browser build)."""
BARCODE_ICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18' fill='%234fb3ef'%3E%3Crect x='1' y='3' width='2' height='12'/%3E%3Crect x='4' y='3' width='1' height='12'/%3E%3Crect x='6' y='3' width='2' height='12'/%3E%3Crect x='9' y='3' width='1' height='12'/%3E%3Crect x='11' y='3' width='3' height='12'/%3E%3Crect x='15' y='3' width='2' height='12'/%3E%3C/svg%3E"
UI_CSS = """
/* ===== Module 531 v2.1 · UI layer: wayfinding, themed browser surfaces, readable prompts ===== */
html{scroll-behavior:smooth;scroll-padding-top:64px}
::selection{background:#0079C0;color:#fff}
input,textarea,select{caret-color:var(--acc)}
*{scrollbar-color:#2c4a63 #0b1620;scrollbar-width:thin}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-track{background:#0b1620}::-webkit-scrollbar-thumb{background:#2c4a63;border-radius:8px;border:2px solid #0b1620}
:focus-visible{outline:2px solid #8fd0ff;outline-offset:2px;border-radius:4px}
button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid #8fd0ff;outline-offset:1px;border-color:var(--acc)}
input[type=text],input[type=number],select{min-height:38px}
textarea{min-height:64px}
input[type=checkbox],input[type=radio]{width:20px;height:20px;accent-color:#0079C0;margin:2px 8px 2px 0;flex:none}
.chk{min-height:32px;align-items:center}
.card h3.h4{margin:0 0 6px;font-size:13px;color:var(--ink);letter-spacing:0;text-transform:none}
button{min-height:36px;transition:background .15s ease-out,border-color .15s ease-out,transform .12s ease-out,box-shadow .2s ease-out}
button:active{transform:translateY(1px)}
button.primary:hover{box-shadow:0 6px 16px -6px rgba(0,121,192,.75)}
button.primary:disabled{box-shadow:none}
#lqCard .lqq .lqp{text-transform:none;letter-spacing:0;font-size:14px;font-weight:400;color:#dfeaf3;line-height:1.55}
#lqCard .lqq .lqp .qn{font-weight:700}
input.scanin{font-family:"SFMono-Regular",Consolas,monospace;padding-left:34px !important;background-image:url("__ICON__");background-repeat:no-repeat;background-position:10px center;background-size:18px 18px;min-width:220px}
.scanin:focus,.seqin:focus{background-color:#0f2233;box-shadow:inset 0 0 0 1px var(--acc)}
.seqin{font-family:"SFMono-Regular",Consolas,monospace;min-width:220px}
#benchPanel{border-color:#3a6a8f;background:linear-gradient(180deg,#152a3d 0%,#132433 120px)}
#benchPanel>h2{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
#benchPanel>h2::before{content:"Hands-on";font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:#0b1620;background:var(--acc);border-radius:12px;padding:2px 9px;font-weight:700}
#benchPanel .card h3.h4{color:var(--acc)}
::placeholder{color:var(--faint);opacity:1}
@media (pointer:coarse){button{min-height:44px}button.small{min-height:40px}input[type=text],input[type=number],select{min-height:44px}#pbar .pstep{min-height:44px}}
.okmark,.badmark,.warnmark{display:inline-flex;align-items:center;gap:5px}
.okmark::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--ok);flex:none}
.badmark::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--bad);flex:none}
.warnmark::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--warn);flex:none}
.sheet{animation:sheetIn .45s cubic-bezier(.16,1,.3,1) both}
@keyframes sheetIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.sheet{animation:none}html{scroll-behavior:auto}}
#pbar{position:sticky;top:0;z-index:50;background:rgba(11,22,32,.9);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line);margin:0 -20px 16px;padding:8px 20px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12px}
#pbar .plab{font-weight:700;color:var(--ink);margin-right:auto;white-space:nowrap}
#pbar .plab span{color:var(--faint);font-weight:400;margin-left:8px}
#pbar .pstep{display:inline-flex;align-items:center;gap:7px;color:var(--dim);text-decoration:none;padding:5px 11px;border:1px solid var(--line);border-radius:20px;transition:border-color .15s ease-out,color .15s ease-out,background .15s ease-out}
#pbar .pstep:hover{border-color:#3d6485;background:#16293a}
#pbar .pstep .dot{width:8px;height:8px;border-radius:50%;background:var(--line);flex:none;transition:background .2s ease-out}
.gatetag{display:inline-block;font-size:10px;letter-spacing:1px;font-weight:700;padding:1px 5px;border-radius:4px;background:rgba(245,166,35,.18);color:#f5a623;border:1px solid rgba(245,166,35,.5);vertical-align:middle}.gatebox{border-color:rgba(245,166,35,.5)}.gatebox ul{margin:6px 0 0 18px;padding:0}.gatebox li{margin:3px 0}#pbar .pstep.done{border-color:rgba(57,201,142,.55);color:var(--ok)}#pbar .pstep.done .dot{background:var(--ok)}
#pbar .pstep.part{border-color:rgba(232,182,76,.55);color:var(--warn)}#pbar .pstep.part .dot{background:var(--warn)}
#pbar .pstep b{font-weight:700}
@media (max-width:640px){.frow>div{flex-basis:auto !important;min-width:0}.scanin,.seqin{min-width:0;width:100%}#pbar{margin:0 -12px 14px;padding:6px 12px;gap:6px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}#pbar::-webkit-scrollbar{display:none}#pbar .plab{margin-right:4px}#pbar .plab span{display:none}#pbar .pstep{padding:4px 9px;white-space:nowrap;flex:none}}
@media print{#pbar{display:none}}
""".replace("__ICON__", BARCODE_ICON)

UI_JS = r"""
/* ===== Module 531 v2.1 · progress bar: where you are, what is left ===== */
(function(){
 function $(id){return document.getElementById(id)}
 function ready(fn){if(document.readyState!=="loading")fn();else document.addEventListener("DOMContentLoaded",fn)}
 ready(function(){
  var app=$("app"),head=document.querySelector("header.top");if(!app||!head||$("pbar"))return;
  var bar=document.createElement("nav");bar.id="pbar";bar.setAttribute("aria-label","Progress");
  var set=(window.LQ&&LQ.set)?" · Set "+LQ.set:"";
  bar.innerHTML='<div class="plab">'+(window.LQ?LQ.lab:"")+'<span>'+set+'</span></div>'
   +(function(){var n=0,h="";if($("sheetWrap")){h+='<a class="pstep" id="ps1" href="#sim"><span class="dot"></span><b>'+(++n)+'</b> Simulator</a><a class="pstep" id="ps2" href="#sheetWrap"><span class="dot"></span><b>'+(++n)+'</b> Simulator record</a>'}
    if($("benchPanel"))h+='<a class="pstep" id="ps3" href="#benchPanel"><span class="dot"></span><b>'+(++n)+'</b> Bench record</a>';
    h+='<a class="pstep" id="ps4" href="#lqCard"><span class="dot"></span><b>'+(++n)+'</b> Questions <span id="pqn"></span></a><a class="pstep" id="ps5" href="#lqBuild"><span class="dot"></span><b>'+(++n)+'</b> PDF</a>';return h})();
  app.insertBefore(bar,head);
  function mark(el,state){if(!el)return;el.classList.remove("done","part");if(state)el.classList.add(state)}
  function update(){
   var so=$("sheetOut"),sim=so&&so.querySelector(".sheet");mark($("ps2"),sim?(so.querySelector(".badmark")?"part":"done"):"");
   var bo=$("benchOut"),bs=bo&&bo.querySelector(".sheet");mark($("ps3"),bs?(bo.querySelector("p.badmark")?"part":"done"):"");
   var card=$("lqCard");if(card){var qs=card.querySelectorAll(".lqq"),n=0;
    Array.prototype.forEach.call(qs,function(q){var ok=false;Array.prototype.forEach.call(q.querySelectorAll("textarea"),function(t){if((t.value||"").trim())ok=true});var im=q.querySelector("img");if(im&&im.getAttribute("src")&&im.style.display!=="none")ok=true;if(ok)n++});
    var pq=$("pqn");if(pq)pq.textContent=qs.length?n+"/"+qs.length:"";mark($("ps4"),qs.length&&n===qs.length?"done":(n?"part":""));
    var out=$("lqOut");mark($("ps5"),out&&out.textContent.replace(/\s/g,"")?"done":"")}
   var simIn=document.querySelectorAll("#sim input, #sim select, #sim textarea"),f=0;Array.prototype.forEach.call(simIn,function(e){if(e.closest&&e.closest("#benchPanel"))return;var touched=e.tagName==="SELECT"?e.selectedIndex>0:(e.type==="checkbox"?e.checked!==e.defaultChecked:((e.value||"").trim()&&e.value!==e.defaultValue));if(touched)f++});
   mark($("ps1"),sim?(so.querySelector(".badmark")?"part":"done"):(f?"part":""));
  }
  var t;function later(){clearTimeout(t);t=setTimeout(update,120)}
  document.addEventListener("input",later,true);document.addEventListener("change",later,true);document.addEventListener("click",later,true);
  var mo=new MutationObserver(later);mo.observe(app,{childList:true,subtree:true});
  update();
 });
})();
"""
