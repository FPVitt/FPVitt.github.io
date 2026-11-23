import urllib.request, json, os
from playwright.sync_api import sync_playwright
B="http://127.0.0.1:8099"
def mock(path): urllib.request.urlopen(B+path).read()
NOSTICKY="nav#tabs{position:static!important} footer{position:static!important} .modal{position:fixed}"
# Merge into the existing annotations (other scripts add their own entries) and, with ONLY="a,b", re-shoot just those shots.
ANN=json.load(open("shots/annot.json")) if os.path.exists("shots/annot.json") else {}
ONLY=set(filter(None,os.environ.get("ONLY","").split(",")))
def want(n): return not ONLY or n in ONLY
JS="""(a)=>{const r=(e)=>{const b=e.getBoundingClientRect();return [b.left+scrollX,b.top+scrollY,b.width,b.height]};
 return {c:a.c?r(document.querySelector(a.c)):[scrollX,scrollY,innerWidth,innerHeight],
         m:a.m.map(s=>{const e=document.querySelector(s);return e?r(e):null})}}"""
with sync_playwright() as p:
    br=p.chromium.launch(channel="chrome")
    def page(sc="ready", adv=False, tab=None, rec=1, nosticky=True, w=400, h=860, wait=900, sel=True):
        mock(f"/mock/set?name={sc}"); mock(f"/mock/adv?on={1 if adv else 0}"); mock(f"/mock/rec?mode={rec}")
        ctx=br.new_context(viewport={"width":w,"height":h},device_scale_factor=2,is_mobile=True,has_touch=True,locale="en-US")
        if sel: ctx.add_init_script("try{localStorage.setItem('camsel','d45e1a7c029b')}catch(e){}")   # the camera pages stay grayed out until a camera is chosen
        pg=ctx.new_page(); pg.goto(B+"/"); pg.wait_for_timeout(wait)
        if tab: pg.click(f'nav#tabs button[data-t="{tab}"]'); pg.wait_for_timeout(700)
        if nosticky: pg.add_style_tag(content=NOSTICKY)
        return pg
    def cap(pg,name,container=None,marks=()):
        if not want(name): return
        # container: a selector, or a list of two selectors = the area from the first one's top to the last one's bottom
        rng=None
        if isinstance(container,(list,tuple)):
            rng=pg.evaluate("""(a)=>{const r=a.map(s=>document.querySelector(s).getBoundingClientRect());
              const x=Math.min(...r.map(b=>b.left))+scrollX, y=r[0].top+scrollY, x2=Math.max(...r.map(b=>b.right))+scrollX, y2=r[r.length-1].bottom+scrollY;
              return [x,y,x2-x,y2-y]}""",list(container)); container=None
        info=pg.evaluate(JS,{"c":container,"m":[m[1] for m in marks]})
        cx,cy,cw,ch=rng or info["c"]
        ANN[name]={"w":cw,"h":ch,"marks":[{"n":m[0],"box":[b[0]-cx,b[1]-cy,b[2],b[3]]} for m,b in zip(marks,info["m"]) if b]}
        ANN[name]['marks']=[m for m in ANN[name]['marks']]
        if rng: pg.screenshot(path=f"shots/{name}.png",clip={"x":rng[0],"y":rng[1],"width":rng[2],"height":rng[3]})
        elif container: pg.locator(container).first.screenshot(path=f"shots/{name}.png")
        else: pg.screenshot(path=f"shots/{name}.png")
    def done(pg): pg.context.close()

    HT=["#hero",".tiles"]   # the verdict banner and the two tiles (firmware 0.3.3 Status tab)
    pg=page(nosticky=False); cap(pg,"first_screen",None,[(1,".logo"),(2,"nav#tabs"),(3,"#hero"),(4,"#fw")]); done(pg)
    pg=page()
    cap(pg,"status_now",HT,[(1,"#hero"),(2,"#t-ac"),(3,"#t-cam"),(4,"#sig")])
    pg.evaluate("document.querySelector('#stat-more').open=true"); pg.wait_for_timeout(300)
    cap(pg,"status_details","#c-cam",[(1,"#c-cam .stats"),(2,"#stat-more summary"),(3,"#rectest"),(4,"#camrefresh")]); done(pg)
    pg=page("recording"); cap(pg,"status_rec",HT); done(pg)
    pg=page("fcdown")
    cap(pg,"status_fcdown","main",[(1,"#flags")])
    if want("offline_banner"): pg.screenshot(path="shots/offline_banner.png",clip={"x":0,"y":0,"width":400,"height":240})
    done(pg)
    pg=page("ready",adv=True); cap(pg,"status_diag","#status .card.adv-only"); done(pg)
    pg=page("repair"); cap(pg,"status_repair",HT,[(1,"#hero-t"),(2,"#flags")]); done(pg)
    # Cam control
    pg=page(tab="cam-control",rec=2)
    cap(pg,"cc_record","#cam-control .card",[(1,"[name='record.mode']"),(2,"[name='record.switch.mode']"),(3,"[name='record.switch.channel']"),(4,"[data-aux-for='record.switch.channel']"),(5,"#rb-record"),(6,"[name='record.switch.threshold_us']")])
    cap(pg,"cc_preset","#preset-card",[(1,"[name='preset.enabled']"),(2,"[name='preset.channel']"),(3,"#rb-preset"),(5,"#zone-add"),(6,"#gp-zt"),(7,"#gp-live"),(8,"#gp-rows"),(9,"#gp-capture"),("a_zoneend","#zone-add"),("a_gp","#gp-builder"),("a_prot","#gp-rows h4:nth-of-type(2)")])
    done(pg)
    # firmware 0.3.3: GoPro zones in "simple" style (the zone is one of the camera's own presets)
    mock("/mock/gpmode?on=1")
    pg=page(tab="cam-control",rec=2)
    cap(pg,"cc_gp_simple","#preset-card",[(1,"[name='preset.gp_mode']"),(2,"#zone-ids .pz:nth-of-type(1) input"),(3,"#zone-ids .pz:nth-of-type(1) .zcap"),(4,"#zone-ids .pz:nth-of-type(1) .zapply")]); done(pg)
    mock("/mock/gpmode?on=0")
    pg=page(tab="cam-control",rec=1); cap(pg,"cc_record_armed","#cam-control .card"); done(pg)
    pg=page(tab="cam-control",adv=True,rec=3)
    cap(pg,"cc_adv_rec","#cam-control .card","[]" and [(1,"details.adv.adv-only")])
    cap(pg,"cc_hilight","#hilight-card"); done(pg)
    # OSD
    pg=page("recording",tab="osd")
    cap(pg,"osd_preview","#osdprev",[(1,"#osdscreen"),(2,"#osdsim")])
    cap(pg,"osd_editor","#osdedit",[(1,"#palette"),(2,".oline"),(3,".chip"),("a_l2","[data-i='1']")])
    cap(pg,"osd_settings","#osd",[]); done(pg)
    pg=page("ready",tab="osd"); pg.fill("#osdsim","") if False else None; cap(pg,"osd_lost","#osdprev"); done(pg)
    # Binding
    pg=page(tab="camera"); cap(pg,"binding","#camera",[(1,"#camlist"),(2,"#pairrow"),(3,"#camtest"),(4,".forget")]); done(pg)
    pg=page("nocam",tab="camera"); cap(pg,"binding_empty","#camera"); 
    pg.click('button[data-pair="gopro"]'); pg.wait_for_timeout(2500)
    cap(pg,"pair_modal","#pair .modal-card",[(1,"#pair .steps"),(2,"#pair .qrbox"),(3,"#pair-list"),(4,"#pair-go")]); done(pg)
    # firmware 0.3.3: DJI uses the same guided popup (Scan now, camera list)
    pg=page("nocam",tab="camera"); pg.click('button[data-pair="dji"]'); pg.wait_for_timeout(500); pg.click("#pair-go"); pg.wait_for_timeout(3000)
    cap(pg,"pair_modal_dji","#pair .modal-card",[(1,"#pair .steps"),(2,"#pair-list"),(3,"#pair-go")]); done(pg)
    # Network / System / Clock
    pg=page(tab="network"); cap(pg,"network","#network",[(1,"[name='wifi.ssid']"),(2,"[name='wifi.password']"),(3,"[name='wifi.portal_trigger']"),(4,"#mspscan")]); done(pg)
    pg=page(adv=True,tab="network"); cap(pg,"network_adv","#network",[(1,"[name='msp.baud']"),(2,"[name='msp.swap_pins']"),(3,"[name='radio.ble_power']"),("a_radio","[name='radio.wifi_power']"),("a_mspend","[name='msp.swap_pins']")]); done(pg)
    pg=page(tab="system"); cap(pg,"system","#system",[(1,"#advmode"),(2,"#identify"),(3,"#factory"),(4,"#otafile")]); done(pg)
    pg=page(adv=True,tab="clock"); cap(pg,"clock","#clock",[(1,"[name='clock.enabled']"),(2,"[name='clock.min_sats']"),(3,"#syncnow")]); done(pg)
    pg=page("nag",nosticky=False); pg.wait_for_timeout(900); cap(pg,"pw_modal","#setup .modal-card"); done(pg)
    # per-camera settings, camera names, no-camera message (firmware 0.3.1)
    # 0.3.3: the list picks a camera by itself. Two cameras paired, none connected and none chosen before: it stays on "Select a camera"
    pg=page("lost",tab="osd",sel=False); pg.wait_for_timeout(1500); cap(pg,"camsel_locked","#camsel"); done(pg)
    pg=page(tab="osd",sel=False); pg.wait_for_timeout(1500); cap(pg,"camsel","#camsel"); done(pg)
    pg=page(tab="camera"); pg.evaluate("nickOpen(camList()[0], true)"); pg.wait_for_timeout(300); cap(pg,"nick_modal","#nick .modal-card",[(1,"#nick-in"),(2,"#nick-save")]); done(pg)
    pg=page("nocam",tab="osd"); pg.wait_for_timeout(1500); cap(pg,"nocam","#nocam",[(1,"#nocam-go")]); done(pg)
    # Remote ID tab (firmware 0.3.0)
    mock("/mock/rid?on=1&test=done")
    pg=page(tab="rid")
    cap(pg,"rid_receiver","#rid-c-recv",[(1,"[name='rid.enabled']"),(2,"[name='rid.mode']"),(3,"[name='rid.ble_duty']"),(4,"[name='rid.min_sats']"),(5,"[name='rid.stale_s']")])
    cap(pg,"rid_warning","#rid-c-warn",[(1,"[name='rid.warn.enabled']"),(2,"[name='rid.warn.notice_m']"),(3,"[name='rid.warn.bearing']"),(4,"[name='rid.warn.blink']"),(5,"[name='rid.warn.ground']"),(6,"#rid-prev")])
    cap(pg,"rid_mine","#rid-c-mine",[(1,"[name='rid.ignore.0']")])
    pg.wait_for_timeout(1800)
    cap(pg,"rid_near","#rid .card:has(#rid-list)",[(1,"#rid-list"),(2,".ridrow button")])
    cap(pg,"rid_health","#rid .card:has(#rid-health)",[(1,"#rid-health")])
    cap(pg,"rid_test","#rid-c-test",[(1,"#rid-testbtn"),(2,"#rid-teststat"),(3,"#rid-tlist")]); done(pg)
    mock("/mock/rid?on=0&test=idle")
    pg=page(tab="rid"); pg.wait_for_timeout(1200); cap(pg,"rid_off","#rid-c-recv"); done(pg)
    mock("/mock/rid?on=1&test=idle&osd=1")
    pg=page("lost",tab="osd"); pg.check("#osdsim"); pg.wait_for_timeout(300)
    for _ in range(60):
        if "!RID" in (pg.inner_text("#osdscreen") or ""): break
        pg.wait_for_timeout(200)
    cap(pg,"osd_rid","#osdscreen"); done(pg)
    mock("/mock/rid?on=0&test=idle")
    # footer bar
    pg=page(tab="osd",nosticky=False); pg.fill("[name='osd.refresh_hz']","6"); pg.wait_for_timeout(400)
    if want("savebar_dirty"): pg.screenshot(path="shots/savebar_dirty.png",clip={"x":0,"y":770,"width":400,"height":90})
    done(pg)
    br.close()
json.dump(ANN,open("shots/annot.json","w"))
print("ok",len(ANN))
