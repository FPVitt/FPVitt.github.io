def modes():
    X0,PX=150,44.17
    x=lambda t:X0+t*PX
    rows=[("Armed",30,[(2,8)],"var(--mut)"),("Radio switch",64,[(4,10)],"var(--mut)"),
          ("When armed",126,[(2,8)],"var(--acc)"),("From a switch",160,[(4,10)],"var(--acc)"),
          ("Armed OR switch",194,[(2,10)],"var(--acc)"),("Armed AND switch",228,[(4,8)],"var(--acc)")]
    s='<div class="diagram"><svg viewBox="0 0 700 290" role="img" aria-label="Recording modes over time">'
    s+='<text x="10" y="14" class="m t9 b" style="letter-spacing:.08em">INPUTS</text><text x="10" y="108" class="m t9 b" style="letter-spacing:.08em">RECORDING MODE → CAMERA RECORDS</text>'
    for t,l in ((2,"arm"),(4,"switch on"),(8,"disarm"),(10,"switch off")):
        s+=f'<path d="M{x(t):.1f} 22 V262" stroke="var(--line)" stroke-width="1" stroke-dasharray="3 4"/><text x="{x(t):.1f}" y="278" text-anchor="middle" class="m t9">{l}</text>'
    for name,y,segs,col in rows:
        s+=f'<text x="10" y="{y+12}" class="t10">{name}</text>'
        s+=f'<path d="M{X0} {y+16} H{x(12):.1f}" stroke="var(--line)" stroke-width="1.2"/>'
        for a,b in segs:
            if col=="var(--acc)": s+=f'<rect x="{x(a):.1f}" y="{y}" width="{x(b)-x(a):.1f}" height="16" rx="3" fill="var(--acc)"/>'
            else: s+=f'<path d="M{x(a):.1f} {y+16} V{y+2} H{x(b):.1f} V{y+16}" fill="none" stroke="var(--fg)" stroke-width="2"/>'
    s+='</svg><p class="cap">Example: the drone arms at 2, the switch goes on at 4, the drone disarms at 8 and the switch goes off at 10. Start and stop delays are left out.</p></div>'
    return s
def zones():
    X=lambda us:40+(us-900)/1200*620
    s='<div class="diagram"><svg viewBox="0 0 700 250" role="img" aria-label="Zones on a radio switch">'
    cols=["var(--zone-1)","var(--zone-2)","var(--zone-3)"]
    edges=[900,1300,1700,2100]
    for i in range(3):
        s+=f'<rect x="{X(edges[i]):.1f}" y="38" width="{X(edges[i+1])-X(edges[i]):.1f}" height="22" fill="{cols[i]}" fill-opacity=".85" rx="{0}"/>'
    s+=f'<rect x="40" y="38" width="620" height="22" rx="6" fill="none" stroke="var(--line)" stroke-width="1.3"/>'
    for us in (1300,1700):
        s+=f'<rect x="{X(us)-8:.1f}" y="32" width="16" height="34" rx="5" fill="var(--fg)" stroke="var(--bg)" stroke-width="1.5"/><text x="{X(us):.1f}" y="24" text-anchor="middle" class="t10 b">{us}</text>'
    for us in (1000,1500,2000):
        s+=f'<path d="M{X(us):.1f} 70 V78" stroke="var(--line)" stroke-width="1.2"/><text x="{X(us):.1f}" y="90" text-anchor="middle" class="m t9">{us} µs</text>'
    s+=f'<path d="M{X(1500):.1f} 28 V70" stroke="var(--warn)" stroke-width="2"/><text x="{X(1500)+6:.1f}" y="21" class="t9" style="fill:var(--warn)">stick</text>'
    cards=[("Zone 1","4K · 60 fps","Lens: Wide","HyperSmooth: High","Protune on"),
           ("Zone 2","2.7K · 120 fps","Lens: Linear","HyperSmooth: Low","Protune on"),
           ("Zone 3","1080 · 240 fps","Lens: Wide","HyperSmooth: Off","")]
    for i,c in enumerate(cards):
        x0=40+i*212; col=cols[i]
        s+=f'<rect x="{x0}" y="112" width="196" height="108" rx="10" fill="var(--bg)" stroke="{col}" stroke-width="2"/>'
        s+=f'<text x="{x0+14}" y="134" class="b t12">{c[0]}</text>'
        for j,t in enumerate(c[1:]):
            if t: s+=f'<text x="{x0+14}" y="{154+j*17}" class="t10{" b" if j==0 else ""}">{t}</text>'
        cx=(X(edges[i])+X(edges[i+1]))/2
        s+=f'<path d="M{cx:.1f} 66 V112" stroke="{col}" stroke-width="1.6" stroke-dasharray="4 3" fill="none"/>'
    s+='<text x="350" y="242" text-anchor="middle" class="m t9">Example settings for a GoPro. The zone applies once the stick has rested in it for the hold time (400 ms).</text>'
    s+='</svg><p class="cap">A three-position switch split into three zones. The bar spans 900 to 2100 µs.</p></div>'
    return s
def led():
    X0,PX=250,73  # 6 s window
    rows=[("Booting","solid"),("Config portal open","double"),("Camera recording","solid"),
          ("No flight controller","fc"),("Camera lost","fast"),("Searching for camera","breathe"),
          ("Camera ready, idle","idle"),("Watchdog recovery (once)","fault"),("Identify (3 s)","ident")]
    s=f'<div class="diagram"><svg viewBox="0 0 700 {len(rows)*28+36}" role="img" aria-label="LED patterns">'
    for k in range(0,7):
        s+=f'<path d="M{X0+k*PX} 8 V{len(rows)*28+10}" stroke="var(--line)" stroke-width="1" stroke-dasharray="2 4"/><text x="{X0+k*PX}" y="{len(rows)*28+26}" text-anchor="middle" class="m t8">{k} s</text>'
    def on(t0,t1,y,op=1): return f'<rect x="{X0+t0*PX:.1f}" y="{y}" width="{(t1-t0)*PX:.1f}" height="12" rx="2" fill="var(--acc)" fill-opacity="{op}"/>'
    for i,(name,kind) in enumerate(rows):
        y=14+i*28
        s+=f'<text x="10" y="{y+10}" class="t10">{name}</text><rect x="{X0}" y="{y}" width="{6*PX}" height="12" rx="2" fill="var(--well)" stroke="var(--line)" stroke-width=".8"/>'
        if kind=="solid": s+=on(0,6,y)
        elif kind=="double":
            for k in range(6): s+=on(k+0.0,k+0.12,y)+on(k+0.24,k+0.36,y)
        elif kind=="fc":
            for k in (0,2,4): s+=on(k,k+0.12,y)+on(k+0.3,k+0.42,y)
        elif kind=="fast":
            t=0
            while t<6: s+=on(t,t+0.15,y); t+=0.3
        elif kind=="breathe":
            import math
            pts=[]
            for n in range(0,261):
                t=n/260*6; ph=(t%2.6)/2.6; v=0.5-0.5*math.cos(2*math.pi*ph)
                pts.append((X0+t*PX,y+12-12*v))
            d="M"+" L".join(f"{a:.1f} {b:.1f}" for a,b in pts)+f" L{X0+6*PX} {y+12} L{X0} {y+12} Z"
            s+=f'<path d="{d}" fill="var(--acc)" fill-opacity=".85"/>'
        elif kind=="idle":
            for k in (0,3): s+=on(k,k+0.12,y)
        elif kind=="fault":
            t=0
            for n in range(5): s+=on(t,t+0.15,y); t+=0.3
        elif kind=="ident":
            t=0
            while t<3: s+=on(t,t+0.2,y); t+=0.4
    s+='</svg><p class="cap">What a single-colour LED does over a six-second window.</p></div>'
    return s

# ---------------------------------------------------------------- Remote ID (planned feature)
def _arr(x,y,rot=0,sz=1.0,col="var(--fg)"):
    """An OSD-style direction arrow glyph pointing 'up' at rot=0 (clockwise degrees)."""
    return f'<path transform="translate({x} {y}) rotate({rot}) scale({sz})" d="M0,-12 L9,6 L0,1 L-9,6 Z" fill="{col}"/>'
def _head(i):
    return f'<defs><marker id="{i}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--mut)"/></marker></defs>'
def rid_overview():
    s='<div class="diagram"><svg viewBox="0 0 700 262" role="img" aria-label="How Remote ID reception works">'+_head("ro1")
    s+='<rect x="10" y="34" width="150" height="96" rx="10" fill="var(--well)" stroke="var(--line)" stroke-width="1.3"/>'
    s+='<text x="85" y="72" text-anchor="middle" class="b t14">Other drones</text><text x="85" y="94" text-anchor="middle" class="m t11">send Remote ID</text><text x="85" y="110" text-anchor="middle" class="m t11">with a position</text>'
    s+='<g class="ln"><path d="M164 66 H334" marker-end="url(#ro1)"/><path d="M164 104 H334" marker-end="url(#ro1)"/></g>'
    s+='<text x="249" y="58" text-anchor="middle" class="t12">Bluetooth</text><text x="249" y="124" text-anchor="middle" class="t12">Wi-Fi, armed only</text>'
    s+='<rect x="338" y="22" width="150" height="120" rx="10" fill="var(--card)" stroke="var(--acc)" stroke-width="2.4"/>'
    s+='<text x="413" y="62" text-anchor="middle" class="b t14">RecLink</text><text x="413" y="86" text-anchor="middle" class="t12">listens only</text><text x="413" y="106" text-anchor="middle" class="t12">never transmits</text>'
    s+='<rect x="298" y="192" width="230" height="46" rx="10" fill="var(--well)" stroke="var(--line)" stroke-width="1.3"/><text x="413" y="212" text-anchor="middle" class="t12">Your flight controller</text><text x="413" y="228" text-anchor="middle" class="m t11">GPS position and heading</text>'
    s+='<g class="ln"><path d="M413 190 V146" marker-end="url(#ro1)"/></g>'
    s+='<g class="ln"><path d="M492 82 H540" marker-end="url(#ro1)"/></g>'
    s+='<rect x="544" y="34" width="146" height="96" rx="10" fill="var(--osd-bg)" stroke="var(--line)" stroke-width="1.3"/>'
    s+='<text x="560" y="78" class="b" font-family="var(--font-mono)" font-size="16" fill="var(--warn)">!RID1 240M</text>'+_arr(662,74,45,0.9,"var(--warn)")
    s+='<text x="617" y="152" text-anchor="middle" class="m t11">Your goggles</text>'
    s+='<text x="35" y="236" class="m t11">Distance and direction come from the</text><text x="35" y="252" class="m t11">other drones and your own GPS.</text>'
    s+='</svg><p class="cap">What happens: RecLink hears other drones, compares their position with yours and shows one short warning line.</p></div>'
    return s
def rid_gate():
    X0,PX=190,12.0   # 40 s window
    x=lambda t:X0+t*PX
    s='<div class="diagram"><svg viewBox="0 0 700 256" role="img" aria-label="When Remote ID is active">'
    for t in (0,5,20,35):
        s+=f'<path d="M{x(t):.1f} 18 V176" stroke="var(--line)" stroke-width="1" stroke-dasharray="3 4"/>'
    rows=[("GPS fix and satellites",34),("Remote ID",78),("Warnings on the OSD",122)]
    for name,y in rows:
        s+=f'<text x="10" y="{y+17}" class="t12">{name}</text><rect x="{X0}" y="{y}" width="{40*PX}" height="24" rx="3" fill="var(--well)" stroke="var(--line)" stroke-width=".8"/>'
    s+=f'<rect x="{x(0)}" y="34" width="{20*PX}" height="24" rx="3" fill="var(--acc)"/><text x="{x(10):.0f}" y="51" text-anchor="middle" class="onacc b t11">good</text>'
    s+=f'<text x="{x(30):.0f}" y="51" text-anchor="middle" class="m t11">lost</text>'
    s+=f'<rect x="{x(0)}" y="78" width="{5*PX}" height="24" rx="3" fill="var(--mut)" fill-opacity=".5"/><text x="{x(2.5):.0f}" y="95" text-anchor="middle" class="t11">wait</text>'
    s+=f'<rect x="{x(5):.1f}" y="78" width="{15*PX}" height="24" rx="3" fill="var(--acc)"/><text x="{x(12.5):.0f}" y="95" text-anchor="middle" class="onacc b t11">active</text>'
    s+=f'<rect x="{x(20)}" y="78" width="{15*PX}" height="24" rx="3" fill="var(--warn)" fill-opacity=".85"/><text x="{x(27.5):.0f}" y="95" text-anchor="middle" class="b t11" style="fill:var(--warn-ink,#1a1200)">radios still on</text>'
    s+=f'<text x="{x(37.5):.0f}" y="95" text-anchor="middle" class="m t11">off</text>'
    s+=f'<rect x="{x(5):.1f}" y="122" width="{15*PX}" height="24" rx="3" fill="var(--acc)"/><text x="{x(12.5):.0f}" y="139" text-anchor="middle" class="onacc b t11">shown</text>'
    s+=f'<text x="{x(30):.0f}" y="139" text-anchor="middle" class="m t11">blank</text>'
    for t,l,y in ((0,"GPS good",196),(5,"+5 s: on",214),(20,"GPS lost",196),(35,"+15 s: off",214)):
        s+=f'<text x="{x(t):.0f}" y="{y}" text-anchor="middle" class="t11">{l}</text>'
    s+='<text x="350" y="244" text-anchor="middle" class="m t11">With no usable GPS the whole feature stays silent: no listening, no warnings, no failure text.</text>'
    s+='</svg><p class="cap">Remote ID switches on 5 seconds after the GPS is good, and off 15 seconds after it is lost.</p></div>'
    return s
def rid_radio():
    X0,PX=190,12.0   # 40 units
    x=lambda t:X0+t*PX
    s='<div class="diagram"><svg viewBox="0 0 700 290" role="img" aria-label="Which radio does what, disarmed and armed">'
    s+=f'<rect x="{x(12):.1f}" y="14" width="{18*PX}" height="206" fill="var(--acc)" fill-opacity=".07"/>'
    for t in (12,30):
        s+=f'<path d="M{x(t):.1f} 14 V220" stroke="var(--line)" stroke-width="1.2" stroke-dasharray="3 4"/>'
    s+=f'<text x="{x(6):.0f}" y="30" text-anchor="middle" class="b t12">Disarmed</text><text x="{x(21):.0f}" y="30" text-anchor="middle" class="b t12">Armed, in flight</text><text x="{x(35):.0f}" y="30" text-anchor="middle" class="b t12">Disarmed</text>'
    rows=[("Config network (Wi-Fi)",48),("Wi-Fi listening",92),("Bluetooth listening",136),("Camera link",180)]
    for name,y in rows:
        s+=f'<text x="10" y="{y+17}" class="t12">{name}</text><rect x="{X0}" y="{y}" width="{40*PX}" height="24" rx="3" fill="var(--well)" stroke="var(--line)" stroke-width=".8"/>'
    s+=f'<rect x="{x(0)}" y="48" width="{12*PX}" height="24" rx="3" fill="var(--zone-2)"/><text x="{x(6):.0f}" y="65" text-anchor="middle" class="onacc b t11">portal open</text>'
    s+=f'<rect x="{x(33):.1f}" y="48" width="{7*PX}" height="24" rx="3" fill="var(--zone-2)"/><text x="{x(36.5):.0f}" y="65" text-anchor="middle" class="onacc b t11">portal</text>'
    s+=f'<text x="{x(21):.0f}" y="65" text-anchor="middle" class="m t11">off in flight</text>'
    s+=f'<rect x="{x(14):.1f}" y="92" width="{19*PX}" height="24" rx="3" fill="var(--acc)"/><text x="{x(23.5):.0f}" y="109" text-anchor="middle" class="onacc b t11">listen only</text>'
    s+=f'<rect x="{x(0)}" y="136" width="{40*PX}" height="24" rx="3" fill="var(--acc)"/><text x="{x(20):.0f}" y="153" text-anchor="middle" class="onacc b t11">listen only, whenever Remote ID is active</text>'
    s+=f'<rect x="{x(0)}" y="180" width="{40*PX}" height="24" rx="3" fill="var(--mut)" fill-opacity=".45"/><text x="{x(20):.0f}" y="197" text-anchor="middle" class="t11">always on, never given up</text>'
    s+=f'<text x="{x(12):.0f}" y="240" text-anchor="middle" class="t11">arm: network off in 0.1 s</text><text x="{x(30):.0f}" y="240" text-anchor="middle" class="t11">disarm: network back after 3 s</text>'
    s+=f'<text x="{x(14):.0f}" y="262" text-anchor="middle" class="m t11">Wi-Fi listening starts about 2 s after arming</text>'
    s+='</svg><p class="cap">Wi-Fi listening is optional and runs only while armed. Bluetooth listening is the default.</p></div>'
    return s
def rid_osd():
    s='<div class="diagram"><svg viewBox="0 0 700 232" role="img" aria-label="Anatomy of the Remote ID warning line">'
    s+='<rect x="120" y="12" width="460" height="74" rx="10" fill="var(--osd-bg)" stroke="var(--line)" stroke-width="1.3"/>'
    f='font-family="var(--font-mono)" font-weight="800" font-size="34" fill="var(--warn)"'
    parts=[(150,"!"),(184,"RID1"),(312,"240M")]
    for x,t in parts: s+=f'<text x="{x}" y="62" {f}>{t}</text>'
    s+=_arr(462,50,45,1.9,"var(--warn)")
    s+=f'<text x="500" y="62" {f}>+</text>'
    cols=[(160,"!",["Attention mark","Blinks faster as","it gets closer"]),
          (230,"RID1",["Drone number","1 to 9, stays the","same while tracked"]),
          (345,"240M",["Distance","M or KM, or FT","and MI if imperial"]),
          (462,"arrow",["Direction","Relative to your","nose, like home"]),
          (507,"+",["Height","+ above you","- below you"])]
    xs=[62,200,340,480,620]
    for i,(ax,_,lines) in enumerate(cols):
        cx=xs[i]
        s+=f'<path d="M{ax} 90 V{104}" stroke="var(--mut)" stroke-width="1.4"/><path d="M{ax} 104 H{cx} V120" stroke="var(--mut)" stroke-width="1.4" fill="none"/>'
        s+=f'<rect x="{cx-62}" y="124" width="124" height="92" rx="8" fill="var(--well)" stroke="var(--line)" stroke-width="1.1"/>'
        s+=f'<text x="{cx}" y="148" text-anchor="middle" class="b t12">{lines[0]}</text>'
        for j,l in enumerate(lines[1:]): s+=f'<text x="{cx}" y="{170+j*18}" text-anchor="middle" class="m t11">{l}</text>'
    s+='</svg><p class="cap">The warning is at most 16 characters, the size of one OSD custom message.</p></div>'
    return s
def rid_levels():
    cx,cy=165,150
    s='<div class="diagram"><svg viewBox="0 0 700 316" role="img" aria-label="Warning levels by distance">'
    for r,op,col in ((136,.10,"var(--warn)"),(92,.20,"var(--warn)"),(48,.34,"var(--dng)")):
        s+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="1.6"/>'
    s+=f'<g stroke="var(--fg)" stroke-width="3" stroke-linecap="round"><path d="M{cx-9} {cy-9} L{cx+9} {cy+9} M{cx+9} {cy-9} L{cx-9} {cy+9}"/></g><circle cx="{cx}" cy="{cy}" r="4" fill="var(--bg)" stroke="var(--fg)" stroke-width="2"/>'
    s+=f'<text x="{cx}" y="{cy+22}" text-anchor="middle" class="b t12">You</text>'
    s+=f'<circle cx="{cx+62}" cy="{cy-46}" r="6" fill="var(--warn)"/><text x="{cx+72}" y="{cy-50}" class="b t12" font-family="var(--font-mono)">RID1</text>'
    s+=f'<text x="{cx}" y="{cy+158}" text-anchor="middle" class="m t11">Rings are not to scale</text>'
    rows=[("Notice","1000 m","steady !","!RID1 820M","var(--warn)",0.45),
          ("Warn","300 m","slow blinking !","!RID1 240M","var(--warn)",0.8),
          ("Alert","100 m","fast blinking !","!RID2 80M","var(--dng)",1)]
    for i,(nm,d,beh,sample,col,op) in enumerate(rows):
        y=18+i*98
        s+=f'<rect x="352" y="{y}" width="338" height="86" rx="10" fill="var(--well)" stroke="var(--line)" stroke-width="1.1"/>'
        s+=f'<circle cx="378" cy="{y+30}" r="11" fill="{col}" fill-opacity="{op}"/>'
        s+=f'<text x="400" y="{y+28}" class="b t14">{nm}</text><text x="400" y="{y+46}" class="m t11">within {d}</text><text x="400" y="{y+66}" class="t11">{beh}</text>'
        s+=f'<rect x="548" y="{y+14}" width="130" height="58" rx="6" fill="var(--osd-bg)"/><text x="558" y="{y+48}" font-family="var(--font-mono)" font-weight="800" font-size="14" fill="{"var(--dng)" if nm=="Alert" else "var(--warn)"}">{sample}</text>'
    s+='</svg><p class="cap">The default distances. You can change all three in the Remote ID tab.</p></div>'
    return s
def rid_heading():
    s='<div class="diagram"><svg viewBox="0 0 700 236" role="img" aria-label="When the direction arrow appears">'
    s+='<rect x="30" y="12" width="270" height="56" rx="8" fill="var(--osd-bg)" stroke="var(--line)" stroke-width="1.2"/><text x="50" y="48" font-family="var(--font-mono)" font-weight="800" font-size="20" fill="var(--warn)">!RID1 240M NE</text>'
    s+='<rect x="400" y="12" width="270" height="56" rx="8" fill="var(--osd-bg)" stroke="var(--line)" stroke-width="1.2"/><text x="420" y="48" font-family="var(--font-mono)" font-weight="800" font-size="20" fill="var(--warn)">!RID1 240M</text>'+_arr(582,40,45,1.0,"var(--warn)")
    s+='<rect x="30" y="92" width="320" height="26" rx="4" fill="var(--mut)" fill-opacity=".5"/><rect x="350" y="92" width="320" height="26" rx="4" fill="var(--acc)"/>'
    s+='<text x="190" y="110" text-anchor="middle" class="t12">Letters while the heading is unknown</text><text x="510" y="110" text-anchor="middle" class="onacc b t12">Arrow</text>'
    s+='<path d="M350 84 V126" stroke="var(--fg)" stroke-width="2.4"/>'
    s+='<text x="350" y="148" text-anchor="middle" class="b t12">Flying 5 m/s or faster for 5 s</text><text x="350" y="166" text-anchor="middle" class="t12">with 5 or more satellites</text>'
    s+='<text x="190" y="196" text-anchor="middle" class="m t11">On the pad, hovering, flying slowly or sideways</text><text x="510" y="196" text-anchor="middle" class="m t11">Works with or without a compass</text>'
    s+='<text x="350" y="224" text-anchor="middle" class="m t11">Losing the flight controller link starts the wait again.</text>'
    s+='</svg><p class="cap">A wrong arrow is worse than none, so RecLink shows compass letters until it is sure of your heading.</p></div>'
    return s

SVG={"modes":modes,"zones":zones,"led":led,"rid_overview":rid_overview,"rid_gate":rid_gate,"rid_radio":rid_radio,"rid_osd":rid_osd,"rid_levels":rid_levels,"rid_heading":rid_heading}
