"""Firmware 0.3.2 screenshot: the DJI zone rows with their Apply buttons. Merges into shots/annot.json."""
import urllib.request, json
from playwright.sync_api import sync_playwright
B = "http://127.0.0.1:8099"
def mock(path): urllib.request.urlopen(B + path).read()
NOSTICKY = "nav#tabs{position:static!important} footer{position:static!important} .modal{position:fixed}"
JS = """(a)=>{const r=(e)=>{const b=e.getBoundingClientRect();return [b.left+scrollX,b.top+scrollY,b.width,b.height]};
 return {c:r(document.querySelector(a.c)), m:a.m.map(s=>{const e=document.querySelector(s);return e?r(e):null})}}"""
ann = json.load(open("shots/annot.json"))
with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome")
    mock("/mock/set?name=dji"); mock("/mock/adv?on=0"); mock("/mock/rec?mode=1")
    ctx = br.new_context(viewport={"width": 400, "height": 860}, device_scale_factor=2, is_mobile=True, has_touch=True, locale="en-US")
    ctx.add_init_script("try{localStorage.setItem('camsel','f08c3e41a760')}catch(e){}")   # the DJI camera on screen
    pg = ctx.new_page(); pg.goto(B + "/"); pg.wait_for_timeout(1200)
    pg.click('nav#tabs button[data-t="cam-control"]'); pg.wait_for_timeout(1500)
    pg.add_style_tag(content=NOSTICKY)
    marks = [(1, "#zone-ids .pz:nth-of-type(1) input"), (2, "#zone-ids .pz:nth-of-type(1) .zapply"), (3, "#zone-add")]
    info = pg.evaluate(JS, {"c": "#preset-card", "m": [m[1] for m in marks]})
    cx, cy, cw, ch = info["c"]
    ann["cc_dji_zones"] = {"w": cw, "h": ch, "marks": [{"n": m[0], "box": [b[0] - cx, b[1] - cy, b[2], b[3]]} for m, b in zip(marks, info["m"]) if b]}
    pg.locator("#preset-card").first.screenshot(path="shots/cc_dji_zones.png")
    print("apply disabled:", pg.evaluate("[...document.querySelectorAll('.zapply')].map(b=>b.disabled)"))
    br.close()
json.dump(ann, open("shots/annot.json", "w"))
print("ok")
