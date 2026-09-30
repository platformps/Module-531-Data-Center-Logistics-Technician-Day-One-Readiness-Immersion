"""v2.5 — a wrong answer says so, and says why: big WRONG, the reason, and a short buzzer.

    python3 wrong_signal_patch.py TOOLS_DIR

Patches the lab tools in place; a second run changes nothing. Run it after any regeneration.

Only tools that already check an answer are touched: every Module 531 tool, and GLAB 524.2.1 Power Path Tracing.
Nothing is graded that was not graded before and no answer key is added. The block watches for the tool's own
red rejection message (531: a `badmark` outside the record sheets; 524.2.1: the `msgbar stop` line), and when
one appears in answer to something the learner just did it shows WRONG in big letters, says which field or panel
it was in, gives the reason as a full sentence ("Why: ..."; the WHY table rewrites the tools' short statuses), and
plays a buzzer. Prompts and incomplete records ("All fields are required", "3 item(s) incomplete") are
left as they are: only the messages matched by RE below count as wrong. A Sound on/off switch sits bottom-left
and is remembered in the browser. The block does not print.
"""
import glob, os, re, sys

TARGET = re.compile(r"^(531-\d-\d|524-2-1)[-_]")
BLOCK = re.compile(r"<!-- WRONG_SIGNAL[\s\S]*?<!-- /WRONG_SIGNAL -->\n?")
HTML = """<!-- WRONG_SIGNAL v2.5: big WRONG + buzzer when the tool's own check rejects an answer; rebuilt by wrong_signal_patch.py -->
<style id="wrongCss">
#wrongBox{position:fixed;left:50%;top:20%;transform:translateX(-50%);z-index:9999;display:none;box-sizing:border-box;width:max-content;max-width:min(92vw,760px);padding:18px 36px 22px;border-radius:12px;background:#b42318;color:#fff;text-align:center;box-shadow:0 12px 44px rgba(0,0,0,.4);cursor:pointer}
#wrongBox.on{display:block}
#wrongBox .wbig{display:block;color:#fff;font-size:clamp(64px,12vw,120px);line-height:1;font-weight:900;letter-spacing:4px}
#wrongBox .wwhere{display:block;margin-top:12px;color:#fff;font-size:14px;line-height:1.3;font-weight:600;letter-spacing:.4px}
#wrongBox .wwhere:empty{display:none}
#wrongBox .wwhy{display:block;margin-top:8px;color:#fff;font-size:19px;line-height:1.4;font-weight:600}
#wrongBox .wwhy b{font-weight:900}
#wrongSound{position:fixed;left:12px;bottom:12px;z-index:9998;min-height:0;padding:6px 14px;border:1px solid #8fa8bf;border-radius:16px;background:#fff;color:#14212b;font-size:13px;font-weight:600;cursor:pointer}
@media print{#wrongBox,#wrongSound{display:none!important}}
</style>
<div id="wrongBox" role="alert" title="Closes on your next click or key"><span class="wbig">WRONG</span><span class="wwhere"></span><span class="wwhy"></span></div>
<button type="button" id="wrongSound" title="Turn the wrong-answer buzzer on or off">Sound on</button>
<script id="wrongJs">(function(){
var RE=/^(CHECK|SCAN FAIL|Out of order|No record|No entitlement|Tag already)|rejected|not connected|Start at a source|already on your path/;
/* why it is wrong, in a full sentence: the tool's own short status is rewritten; anything not listed is shown as the tool wrote it */
var WHY=[
 [/^CHECK — '(.+)' is not the code this field expects.*$/,"“$1” is not the code this field expects. Scan the card or tag named in the field's label, not a different one."],
 [/^CHECK — read (.+), expected (.+)$/,"The field read $1, but it expects $2. Scan the label this field names."],
 [/^CHECK — not in the bench register.*$/,"That code is not in the bench register. This field takes an ATL-009xx asset tag from an item on the bench."],
 [/^CHECK — '(.+)' is already recorded in another row$/,"“$1” is already recorded in another row. Each item is recorded once."],
 [/^CHECK — bin (.+) does not match the path (.+)$/,"Bin $1 is not the bin for the path you chose ($2). The bin card has to match the path."],
 [/^CHECK — /,""],
 [/^SCAN FAIL — check: (.+)$/,"The tag does not pass the scan check. Missing or not matching the asset plate: $1. Compare each one with the plate line and correct it."],
 [/^SCAN FAIL — tag matches plate but the placement violates the standard$/,"The serial and model match the plate, but the placement you chose breaks the tag placement standard."],
 [/^Out of order at position (\d+).*$/,"The card scanned at position $1 is not the one that belongs there. Restart the sequence and scan the cards in order."],
 [/^(.+) is already in the list.*$/,"$1 is already in the list. Each item is scanned once."],
 [/^No record with that tag\.$/,"No record in the system has the tag you entered. Check it character by character."],
 [/^Tag already exists\.$/,"A record with that tag already exists. One tag identifies one asset."]];
var box=document.getElementById("wrongBox"),why=box.querySelector(".wwhy"),whr=box.querySelector(".wwhere"),btn=document.getElementById("wrongSound"),used=0,fired=0,typed=0,ev="",said="",ctx,off=false;
try{off=localStorage.getItem("labSoundOff")==="1"}catch(e){}
function label(){btn.textContent=off?"Sound off":"Sound on";btn.setAttribute("aria-pressed",String(!off))}
label();
btn.onclick=function(){off=!off;try{localStorage.setItem("labSoundOff",off?"1":"0")}catch(e){}label()};
["pointerdown","keydown","change"].forEach(function(t){document.addEventListener(t,function(){used=Date.now();ev=t;if(t!=="change")box.className=""},true)});   /* the next click or key clears the box */
document.addEventListener("input",function(){typed=Date.now()},true);
function buzz(){if(off)return;try{var A=window.AudioContext||window.webkitAudioContext;ctx=ctx||new A();if(ctx.resume)ctx.resume();
 var o=ctx.createOscillator(),g=ctx.createGain();o.type="sawtooth";o.frequency.value=180;g.gain.value=.2;o.connect(g);g.connect(ctx.destination);o.start();o.stop(ctx.currentTime+.4)}catch(e){}}
function where(e){var s=e.closest('[id$="_st"]'),l=s&&document.querySelector('label[for="'+s.id.slice(0,-3)+'"]');   /* the field's label, else the panel's heading */
 if(!l){var c=e.closest(".card,.panel");l=c&&c.querySelector("h2,h3,h4")}
 return l?l.textContent.replace(/\s+/g," ").trim():""}
function fire(text,e){fired=Date.now();said=text;var w=text;
 for(var i=0;i<WHY.length;i++)if(WHY[i][0].test(w)){w=w.replace(WHY[i][0],WHY[i][1]);break}
 if(!/[.!?]$/.test(w))w+=".";
 why.textContent="";var b=document.createElement("b");b.textContent="Why: ";why.appendChild(b);why.appendChild(document.createTextNode(w));   /* text nodes only: the reason can quote what the learner typed */
 whr.textContent=where(e);box.className="on";buzz()}   /* stays up until the learner's next click or key, so the reason gets read */
function bad(n){return n&&n.nodeType===1?(n.matches(".badmark,.msgbar.stop")?n:n.querySelector(".badmark,.msgbar.stop")):null}
new MutationObserver(function(ms){
 if(Date.now()-used>2000||fired>=used)return;      /* only in answer to something the learner just did, once per action — never on load */
 for(var i=0;i<ms.length;i++){
  var m=ms[i],c=[bad(m.target.nodeType===1?m.target.closest(".badmark,.msgbar.stop"):m.target.parentNode)];
  for(var j=0;j<m.addedNodes.length;j++)c.push(bad(m.addedNodes[j]));
  for(var k=0;k<c.length;k++){var e=c[k];if(!e||e.closest(".sheet"))continue;   /* record sheets list what is missing; that is not a wrong answer */
   var t=e.textContent.replace(/\\s+/g," ").trim();
   if(t===said&&ev==="change"&&typed<fired)continue;      /* leaving a field re-checks it: same answer, not a new mistake */
   if(RE.test(t)){fire(t,e);return}}
 }
}).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});
})();</script>
<!-- /WRONG_SIGNAL -->
"""

def patch(path):
    t = BLOCK.sub("", open(path, encoding="utf-8").read())
    i = t.rfind("</body>")
    assert i > 0, (path, "no </body>")
    open(path, "w", encoding="utf-8").write(t[:i] + HTML + t[i:])

def main(tools):
    n = 0
    for f in sorted(glob.glob(os.path.join(tools, "5*.html"))):
        if TARGET.match(os.path.basename(f)): patch(f); n += 1
    print(f"{n} tools patched")

if __name__ == "__main__":
    main(sys.argv[1])
