# Mock RecLink portal backend: serves the real www/ assets and fakes /api/* so the
# configurator can be screenshotted. Scenario switched via GET /mock/set?name=...
import json, copy, os, sys, time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import os
# The portal front-end lives in the firmware repo; point RECLINK_WWW at its components/portal/www.
WWW = os.environ.get("RECLINK_WWW") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "components", "portal", "www")
CAM = {"brand":"gopro","name":"GoPro HERO11 Black","addr":"D4:5E:1A:7C:02:9B"}
CAM2 = {"brand":"dji","name":"DJI Osmo Action 5","addr":"F0:8C:3E:41:A7:60"}

def V(v, valid=True): return {"v": v, "valid": valid}

CONFIG = {
 "camera":{"brand":"gopro","bonded":True,"addr":CAM["addr"],"name":CAM["name"],"dji_device_id":0},
 "record":{"mode":1,"arm_delay_ms":300,"stop_delay_ms":1500,"verify_timeout_ms":800,"retry_count":3,
           "switch":{"channel":5,"threshold_us":1700,"mode":0}},
 "preset":{"enabled":True,"channel":6,"dwell_ms":400,"allow_during_record":False,"n_zones":3,"gp_mode":0,
   "bands":[
     {"max_us":1300,"id":0,"gp":{"2":1,"3":5,"121":0,"135":2,"114":1,"145":0}},
     {"max_us":1700,"id":1,"gp":{"2":4,"3":1,"121":4,"135":1,"114":1,"145":8}},
     {"max_us":2100,"id":2,"gp":{"2":9,"3":0,"121":0,"135":0}}]},
 "osd":{"refresh_hz":4,"type":1,"corner":1,"lines":["%st %et","%bi%bt %wr","%rs%fp %ln","SD %sd"],
        "fields_mask":8388607,"warn":{"batt_pct":15,"sd_low_min":3,"blink":True,"show_on_lost":True},"units":0},
 "clock":{"enabled":True,"require_gps":True,"min_sats":6,"threshold_s":10,"utc_offset_min":0,"dst":False,
          "check_period_min":5,"resync_period_min":60,"retry_count":2},
 "gps_push":{"enabled":False,"rate_hz":1},
 "hilight":{"channel":7},
 "msp":{"baud":115200,"swap_pins":0},
 "wifi":{"ssid":"","password":"","channel":0,"portal_trigger":1,"portal_timeout_min":15},
 "led_brightness":128,"ui_flags":3,
 "radio":{"wifi_power":2,"ble_power":2},
 "rid":{"enabled":False,"mode":0,"ble_duty":1,"stale_s":5,"min_sats":6,
        "warn":{"enabled":True,"notice_m":1000,"warn_m":300,"alert_m":100,"blink":True,"takeover_level":3,"bearing":0,"ground":False},
        "ignore":["","","",""]},
}
RID_AC = [
 {"id":"1581F4XYZ7GH2K9LM3P0","n":1,"type":2,"status":2,"dist_m":240,"brg":47,"vert":"above","dv_m":38,"src":"ble","rssi":-71,"age_ms":900,"level":"warn","ignored":False},
 {"id":"1581F5ABC1DE4F8GH2J6","n":2,"type":2,"status":2,"dist_m":820,"brg":212,"vert":"level","dv_m":4,"src":"ble","rssi":-84,"age_ms":1400,"level":"notice","ignored":False}]
RID_TEST = {"state":"done","ac":[dict(RID_AC[0],age_ms=1200),dict(RID_AC[1],age_ms=3100)]}
CAPS = {"2":[100,1,4,6,9,18],"3":[0,1,5,6,8,9,10],"121":[0,2,4,7,8,3],"135":[0,1,2,3,4],"114":[0,1],
        "13":[0,1,2,3,4,7,8,9],"102":[0,1,2,3,4,7,8,9],"145":[0,3,4,5,6,7,8,11,12,13,16,17],"115":[0,2,3,4,5,7],
        "116":[1,2,100],"117":[0,1,2],"118":[0,1,2,3,4,5,6,7,8],"174":[0,1]}

AUX = [1500,1500,1000,1500] + [1000]*14
AUX[9] = 1500   # aux6 knob mid
def status(sc):
    ready = sc not in ("nocam","lost","pairing","fcdown")
    rec = sc in ("recording",)
    armed = sc in ("recording_armed",)
    aux = list(AUX)
    if sc == "recording": aux[3+5] = 1900
    dji = sc == "dji"      # the DJI camera is the connected one (firmware 0.3.2+: Apply button on DJI zones)
    cams = [] if sc in ("nocam","pairing") else [
        {**CAM, "model":CAM["name"], "active":not dji, "connected":ready and not dji, "poll_ds":10},
        {**CAM2,"model":CAM2["name"],"active":dji,"connected":dji,"poll_ds":10}]
    camera = {"brand":"dji" if dji else "gopro","link":"READY" if ready else ("LOST" if sc=="lost" else "IDLE"),
      "name":CAM["name"] if ready else "", "addr":CAM["addr"], "rssi":-52 if ready else 0,
      "bonded": sc not in ("nocam","pairing"), "last_rx_ms":120, "count":len(cams), "cameras":cams}
    if sc == "pairing":
        camera["found"] = ([{"name":"OsmoAction6-3E4F","addr":"F0:8C:3E:41:A7:60","rssi":-46}] if STATE.get("pairbrand")=="dji" else
                           [{"name":"GoPro 4912","addr":"D4:5E:1A:7C:02:9B","rssi":-48},
                            {"name":"GoPro 8130","addr":"D4:5E:1A:21:90:C4","rssi":-71}])
    cs = {"recording":"true" if rec else "false",
      "battery_pct":V(78 if ready else 0, ready),"sd_remaining_kb":V(41200000,ready),"rec_remaining_s":V(5160,ready),
      "resolution":V("4K",ready),"fps":V("60",ready),"aspect":V("16:9",ready),"profile":V("STD",ready),
      "mode":V("VID",ready),"bit_depth":V(8,ready),
      "iso_max":V("1600",ready),"iso_min":V("100",ready),"shutter":V("1/120",ready),"protune":V("ON",ready),
      "wb":V("Auto",ready),"color":V("Natural",ready),"sharpness":V("Medium",ready),"ev":V("0.0",ready),
      "tune_10bit":V("Off",ready),
      "gp_set":{"2":1,"3":5,"121":0,"135":2,"114":1,"145":0,"13":1,"102":8,"115":0,"116":2,"117":1,"118":4,"174":0} if ready else {},
      "zone_apply":{"zone":1,"state":"ok","fail":[]} if ready else {"zone":0,"state":"none","fail":[]},
      "model":"HERO11 Black" if ready else "","caps_gen":1 if ready else 0,"sd_missing":False,"sd_full":False,"hot":False}
    if ready: cs["preset_id"]=65537        # GoPro status 97 (firmware 0.3.3): the camera's active preset
    if rec: cs["elapsed_s"]=754
    rid_on = STATE.get("rid",False)
    rid = {"enabled":rid_on,"available":True,"no_osd_line":False,"reboot_required":False,"active":rid_on,"inactive_reason":"" if rid_on else "disabled",
           "mode":"ble","min_sats":6,"hdg":"gps","hdg_aligned":True,"mag_present":False,
           "ble":{"scan":"on" if rid_on else "off","rx":812 if rid_on else 0,"drops":0},
           "wifi":{"state":"off","ch":6,"rx":0,"drops":0,"frames_30s":0,"beacon":0,"nan":0},
           "count":2 if rid_on else 0,"decoded":640 if rid_on else 0,"jump_rejects":0,"range_rejects":0,"evict_drops":0,
           "fault":{"subsystem":False,"ble":False,"wifi":False},
           "test":{"state":STATE.get("rtest","idle"),"wifi":False,"aborted":False,"secs_left":18 if STATE.get("rtest")=="run" else 0,
                   "ble_frames":214 if STATE.get("rtest")=="done" else 0,"wifi_frames":0,"beacon":0,"nan":0,"aircraft":2 if STATE.get("rtest")=="done" else 0}}
    if rid_on: rid["nearest"]={"dist_m":240,"level":"warn"}
    return {"fw":"0.3.3","reclink_board":STATE.get("board",False),"rid":rid,"uptime_s":412,"flags":["FC_OFFLINE"] if sc=="fcdown" else (["REPAIR_NEEDED"] if sc=="repair" else []),
      "msp":{"connected":sc!="fcdown","api":"1.47","variant":"BTFL","armed":armed,"canvas":"30x16",
             "aux":aux,"gps":{"present":True,"fix":3,"sats":14,"good":True},"fc_utc":1793560000,"last_rx_ms":18,
             "debug":{"rc_period_ms":100,"rc_hz":10.0,"rc_age_ms":42,"rc_channels":18,"status_period_ms":50,"status_hz":20.0,
                      "rc_nominal_hz":10,"status_nominal_hz":20,"arm_bit":0,"arm_bit_resolved":True,"arm_disable_flags":0,
                      "armed_raw":armed,"link_up_first_ms":1180,"osd_first_ms":1730}},
      "clock":{"enabled":True,"readable":True,"cam_utc":1793560001,"delta_s":-1,"last_sync":{"age_s":186,"result":"OK"}},
      "camera":camera,
      "record":{"mode":1,"sw_mode":0,"raw_active":rec,"sw_active":rec,"desired":rec,"phase":"IDLE","last_cmd":"START" if rec else "NONE"},
      "ble":{"link":camera["link"],"state_age_s":96,"scan":"off","rssi":camera["rssi"],"last_rx_ms":120,"mtu":247,"poll_ms":1500,
             "cfg_bonds":len(cams),"stack_bonds":len(cams),"notify_drops":0,"repair_needed":sc=="repair"},
      "cam_state":cs,
      "wifi":{"portal":True,"default_pw":sc=="nag","pw_nag_off":sc!="nag"},
      "errors":["reconnects:2","msp_crc:0","wdt_recov:0","ble_notify_drops:0","heap_free:41280","heap_min:35120"]}

STATE = {"sc":"ready","adv":False,"rid":False,"rtest":"idle","board":False}
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _j(self,obj,code=200):
        b=json.dumps(obj).encode(); self.send_response(code)
        self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u=urlparse(self.path); p=u.path
        if p=="/mock/adv": STATE["adv"]=parse_qs(u.query)["on"][0]=="1"; return self._j({"ok":True})
        if p=="/mock/rec": CONFIG["record"]["mode"]=int(parse_qs(u.query)["mode"][0]); return self._j({"ok":True})
        if p=="/mock/rid": q=parse_qs(u.query); STATE["rid"]=q["on"][0]=="1"; STATE["rtest"]=q.get("test",["idle"])[0]; CONFIG["rid"]["enabled"]=STATE["rid"]; CONFIG["osd"]["lines"][3]="SD %sd %rp" if q.get("osd",["0"])[0]=="1" else "SD %sd"; return self._j({"ok":True})
        if p=="/mock/gpmode":     # firmware 0.3.3: GoPro zones "simple" (the zone holds one of the camera's own presets)
            on=parse_qs(u.query)["on"][0]=="1"; CONFIG["preset"]["gp_mode"]=1 if on else 0
            for b,i,j in zip(CONFIG["preset"]["bands"],(65536,65537,65538),(0,1,2)):
                b["id"]=i if on else j
            return self._j({"ok":True})
        if p=="/mock/board": STATE["board"]=parse_qs(u.query)["on"][0]=="1"; return self._j({"ok":True})
        if p=="/api/rid": return self._j({"active":STATE["rid"],"hdg":"gps","ac":RID_AC if STATE["rid"] else []})
        if p=="/api/rid/test": return self._j(RID_TEST if STATE["rtest"]=="done" else {"state":STATE["rtest"],"ac":[]})
        if p=="/mock/set": STATE["sc"]=parse_qs(u.query)["name"][0]; return self._j({"ok":True})
        if p=="/api/status": return self._j(status(STATE["sc"]))
        if p=="/api/config": 
            c=copy.deepcopy(CONFIG)
            cam=parse_qs(u.query).get("cam",[""])[0].replace(":","").lower()
            if cam and cam!=CAM["addr"].replace(":","").lower():   # another paired camera: its own copy of the camera pages
                c["osd"]["lines"][0]="B %st %et"; c["record"]["mode"]=2; c["clock"]["min_sats"]=9
            if cam == CAM2["addr"].replace(":","").lower(): c["camera"]["brand"]="dji"      # DJI zones use a mode ID
            if STATE["sc"]=="nocam": c["camera"]["bonded"]=False
            c["ui_flags"]=(3 if STATE["adv"] else 2) if STATE["sc"]!="nag" else (1 if STATE["adv"] else 0)
            return self._j(c)
        if p=="/api/camera/caps":
            return self._j({"gen":1,"caps":CAPS} if STATE["sc"] not in ("nocam","lost","pairing") else {"gen":0,"caps":{}})
        if p=="/api/msp/scan": return self._j({"aux":[{"aux":i,"us":AUX[3+i]} for i in range(1,15)]})
        if p=="/api/logs":
            b=b"[00:06:52] msp: link up  API 1.47 BTFL\n[00:06:53] cam: READY HERO11 Black rssi -52\n[00:06:58] ctrl: zone 2 applied ok\n"
            self.send_response(200); self.send_header("Content-Type","text/plain"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b); return
        name={"/":"index.html","/index.html":"index.html"}.get(p,p.lstrip("/"))
        fp=os.path.join(WWW,name)
        if os.path.isfile(fp):
            b=open(fp,"rb").read(); ct={"html":"text/html","js":"application/javascript","css":"text/css"}.get(name.rsplit(".",1)[-1],"text/plain")
            self.send_response(200); self.send_header("Content-Type",ct+"; charset=utf-8"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b); return
        self.send_response(404); self.end_headers()
    def do_POST(self):
        n=int(self.headers.get("Content-Length") or 0); body=self.rfile.read(n)
        if self.path.startswith("/api/camera/pair"):
            try: STATE["pairbrand"]=json.loads(body or b"{}").get("brand","gopro")
            except Exception: pass
            STATE["sc"]="pairing"
        return self._j({"ok":True,"applied":True})
if __name__=="__main__":
    ThreadingHTTPServer(("127.0.0.1",8099),H).serve_forever()
