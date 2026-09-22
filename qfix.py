"""Bench questions are numbered by their position in the tool registry, not by handout step number.
Spec/key text written as 'Q<step>' is translated to the real 'Q<n>' here, from the generated tools."""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from spec import LABS, LAB_META, LAB_ORDER, tool_file
OUT = os.environ["OUT"]
_maps = {}
def stepq(lid):
    if lid in _maps: return _maps[lid]
    s = LAB_META[lid][3][0]
    lq = json.loads(re.search(r'<script id="lqData">var LQ=(.*?);</script>', open(os.path.join(OUT, "4_Lab_Tools", tool_file(lid, s)), encoding="utf-8").read(), re.S).group(1))
    m = {}
    nb = sum(1 for st in LABS[lid]["steps"] if st["cap"] in ("text", "image"))
    for qi, it in enumerate(lq["items"], 1):
        if qi > len(lq["items"]) - nb:
            m[int(re.match(r"Step (\d+)\.", it["p"]).group(1))] = qi
    _maps[lid] = m; return m
def fixq(lid, text):
    m = stepq(lid)
    return re.sub(r"Q(\d+)", lambda x: "Q" + str(m.get(int(x.group(1)), int(x.group(1)))), text)
def apply_to_spec():
    for lid in LAB_ORDER:
        L = LABS[lid]
        if "key" in L: L["key"] = [fixq(lid, k) for k in L["key"]]
        if "rubric" in L: L["rubric"] = fixq(lid, L["rubric"])
if __name__ == "__main__":
    for lid in LAB_ORDER: print(lid, stepq(lid))
