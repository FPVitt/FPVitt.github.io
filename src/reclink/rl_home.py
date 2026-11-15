"""Content + markup for the RecLink main page (RecLink/en|it/index.html).

Kept apart from build_web.py so the page copy can grow without touching the generator.
render(lang, ctx) returns the <main> HTML. ctx supplies shared bits from build_web:
    gh_url, gh_svg, mark, pre_tag, pre, home_sub, meta, pages (doc -> href), icons
"""
import html
import json

E = html.escape

# OSD layouts shown on the page: four templates each, written with the firmware's own %tokens
# (%st state, %et elapsed, %bt battery, %rs resolution, %fp frame rate, %ln lens, %sd/%sg SD space,
#  %md mode, %pr profile, %bd bit depth, %ar aspect, %cr link RSSI, %cn craft name, %gf/%gs FC GPS).
OSD_TPL = [
    ["%st %et  %bt", "%rs %fp %ln", "%sd %sg", "%md %pr"],
    ["", "%st %et", "", ""],
    ["%cn", "%st %et  %bt", "GPS %gf  %gs SAT", "%sg FREE"],
    ["%rs %fp %ln", "%pr %bd %ar", "%cr dBm  %bt", "%st %et"],
]
# values used for the no-JS fallback (the script below runs a live simulation instead)
OSD_STATIC = dict(st="REC", et="0:42", bt="87%", rs="5.3K", fp="60", ln="WIDE", sd="94m", sg="38.4G", md="VIDEO", pr="HLG",
                  bd="10b", ar="16:9", cr="-62", cn="MY CINEWHOOP", gf="3D", gs="14")


def expand(tpl):
    import re
    return re.sub(r"%([a-z]{2})", lambda m: OSD_STATIC.get(m.group(1), m.group(0)), tpl)[:16]


def _i(path, extra=""):
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}>{path}</svg>')


I = {
    "rec": _i('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.2" fill="currentColor" stroke="none"/>'),
    "zones": _i('<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01M12 7h.01M12 17h.01"/>'),
    "osd": _i('<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M7 9h6M7 13h10M8 21h8"/>'),
    "tag": _i('<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>'),
    "cams": _i('<rect x="3" y="7" width="12" height="10" rx="2"/><path d="M15 11l6-3v8l-6-3"/>'),
    "clock": _i('<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>'),
    "gps": _i('<path d="M12 21s-6.5-5.4-6.5-10.5a6.5 6.5 0 0 1 13 0C18.5 15.6 12 21 12 21z"/><circle cx="12" cy="10.5" r="2.3"/>'),
    "wifi": _i('<path d="M3 9a14 14 0 0 1 18 0M6 12.5a9.5 9.5 0 0 1 12 0M9 16a5 5 0 0 1 6 0"/><circle cx="12" cy="19" r=".8" fill="currentColor"/>'),
    "shield": _i('<path d="M12 3l8 3v6c0 4.5-3.2 7.8-8 9-4.8-1.2-8-4.5-8-9V6z"/><path d="M9 12l2.2 2.2L15.5 10"/>'),
    "fail": _i('<path d="M3 12h4l2-6 4 12 2-6h6"/>'),
    "eye": _i('<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="2.8"/>'),
    "mem": _i('<rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>'),
}

# status glyphs for the compatibility matrix
OK = '<span class="cm ok" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg><i>{t}</i></span>'
UN = '<span class="cm un" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2.4 2"/><path d="M5.4 8.3l1.9 1.9 3.4-3.7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg><i>{t}</i></span>'
PA = '<span class="cm pa" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 2a6 6 0 0 0 0 12z" fill="currentColor"/></svg><i>{t}</i></span>'
NO = '<span class="cm no" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 8h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><i>{t}</i></span>'

C = {
    "en": dict(
        cta_fw="Install the firmware", cta_qs="Quick start",
        stats=[("0.48 g", "board weight"), ("22", "OSD tokens"), ("4", "cameras paired"), ("2–6", "radio-switch zones"), ("0", "commands that touch flight")],
        act_h="See it in action", act_s="What RecLink does while you fly, and what you set up on the ground.",
        acts=[("rec", "Arm to record", "Recording starts the moment you arm, or from a radio switch, or both. Every command is checked against what the camera actually reports."),
              ("osd", "Status in your goggles", "Recording state, timers, battery, SD space and settings drawn on your Betaflight OSD, on four lines you design."),
              ("wifi", "Configure from your phone", "The board opens its own Wi-Fi while you are disarmed. No app, no cloud, no account. It switches off the instant you arm.")],
        osd_h="Your OSD, your layout", osd_cap="A simulated camera feeds it, with the same tokens you place in the configurator. You choose what goes on each of the four 16-character lines.",
        osd_sets=[("Full status", OSD_TPL[0]), ("Minimal", OSD_TPL[1]), ("Craft and GPS", OSD_TPL[2]), ("Camera settings", OSD_TPL[3])],
        osd_note="A value the camera has not confirmed is left blank, never shown as 0 or a guess.",
        feat_h="Everything it does", feat_s="One small board, nine jobs.",
        feats=[("rec", "Record that follows the aircraft", "Start and stop on arm, on a radio switch, arm OR switch, or arm AND switch. Each command is confirmed by the camera before RecLink moves on."),
               ("zones", "Switch zones", "A 2–6 position switch changes camera settings in flight. On a GoPro each zone sets resolution, frame rate, lens, HyperSmooth and Protune values; on a DJI each zone picks a mode."),
               ("osd", "22 OSD tokens", "State, elapsed and remaining time, battery, SD space in minutes or GB, resolution, frame rate, lens, colour profile, link strength and FC GPS."),
               ("tag", "Highlight tags", "Mark the best moment from a momentary switch: a HiLight tag on a GoPro, the Quick-Switch button on a DJI."),
               ("cams", "Up to 4 cameras", "Pair any mix of GoPro and DJI. At power-up RecLink joins whichever paired camera has the strongest signal."),
               ("clock", "Camera clock sync", "Sets the camera clock from the flight controller's GPS time, so your footage is timestamped correctly."),
               ("gps", "GPS position to DJI", "Optionally sends the aircraft's position and time to a DJI camera for its own telemetry overlay."),
               ("eye", "Analog and digital OSD", "Digital mode limits the output to the glyphs the DJI goggle OSD can draw, so nothing turns into a question mark."),
               ("wifi", "Web configurator and OTA", "Pair, build zones, edit the OSD and update the firmware from a captive web page. Wi-Fi is on only while disarmed.")],
        cam_h="Compatible cameras", cam_s="Two brands over Bluetooth LE. Here is what is verified and what is not.",
        cams=[("GoPro", "HERO 9 / 10 / 11 / 12 / 13", "Open GoPro BLE", "bench", "Bench-tested",
               "Record, OSD telemetry and settings-based zones are verified on a HERO11 Black. Other models of the same generation use the same API."),
              ("GoPro", "Mission 1 / Mission 1 Pro", "Open GoPro BLE", "unv", "Unverified",
               "Expected to work, but it may need setting ids this firmware does not use yet. Not tested."),
              ("DJI", "Osmo Action 4 / 5 Pro / 6, Osmo Nano, Osmo 360", "DUML over BLE", "exp", "Experimental",
               "Record, mode switch and status are implemented from DJI's open-source demo. No DJI camera has been tested yet."),
              ],
        cam_note="HERO8 and older have no Open GoPro Bluetooth API and are not supported.",
        mx_h="What each camera can do",
        mx_cols=("Feature", "GoPro", "DJI"),
        mx_rows=[("Connect and auto-reconnect", OK, UN, "", ""),
                 ("OSD telemetry (record, battery, SD, timers)", OK, UN, "", ""),
                 ("Resolution, frame rate and mode readout", OK, UN, "", ""),
                 ("Start / stop recording", OK, UN, "", ""),
                 ("Zones: camera settings", OK, NO, "", "Not available"),
                 ("Zones: camera mode", NO, UN, "Not available", ""),
                 ("Highlight tag", UN, PA, "", "Quick-Switch button instead"),
                 ("Clock sync from FC GPS", UN, PA, "", "Blind: no read-back"),
                 ("Aircraft GPS position to camera", NO, UN, "Not available", "")],
        mx_leg=[("ok", "Supported, bench-tested"), ("un", "Implemented, not confirmed on hardware"), ("pa", "Works with limits"), ("no", "Not available")],
        safe_h="Built to stay out of the way", safe_s="RecLink is a passenger. If it fails, the worst that happens is stale OSD text.",
        safes=[("shield", "Passenger, not pilot", "It only reads from the flight controller and writes OSD text. Arming, RC, PIDs and navigation are out of reach, and the code refuses those commands on its own."),
               ("fail", "Fail open, fail quiet", "Any fault leaves the aircraft fully flyable. After a fault the board reboots in about 300 ms and the camera reconnects by itself."),
               ("wifi", "Wi-Fi only on the ground", "The access point is down within 100 ms of arming. In flight only Bluetooth is active."),
               ("mem", "Never waits on the camera", "Every camera command is fire-and-forget and confirmed afterwards, and nothing in the flight path allocates memory.")],
        pt_h="The configurator", pt_s="Join the RECLINK Wi-Fi while disarmed and any page opens it. Six tabs cover everything.",
        pts=[("Status", "Live link state, camera telemetry and MSP diagnostics."),
             ("Cam control", "Record mode, arm and switch triggers with one-touch AUX detection, the zone builder."),
             ("OSD", "Pick analog or digital, drag tokens onto four lines, preview them live."),
             ("Binding", "Pair, list and forget cameras, with a guided GoPro pairing flow."),
             ("Network", "Wi-Fi credentials, MSP baud rate, TX/RX swap and radio power."),
             ("System", "LED brightness, firmware update over Wi-Fi, factory reset.")],
        go_h="From the box to recording", go_s="About fifteen minutes. The quick start walks through each step with pictures.",
        gos=[("Wire it", "Connect the board to a free UART on your flight controller."),
             ("Flash it", "Install the firmware from your browser over USB."),
             ("Pair the camera", "Open the configurator and pair your GoPro or DJI."),
             ("Set your switches", "Pick when to record, build your zones, lay out the OSD.")],
        need_h="What you need", need_s="Four things.",
        needs=[("A RecLink board", "The custom ESP32-C3 board, in development. Until then an ESP32-C3 or ESP32-S3 dev board runs the same firmware."),
               ("Betaflight 2025.12 or newer", "MSP API 1.47 or later, for custom OSD messages."),
               ("A supported camera", "GoPro HERO 9 or newer, or a DJI Osmo (experimental)."),
               ("A free UART", "One spare serial port on the flight controller.")],
        more_h="Keep exploring",
        end_h="Ready to try it?", end_s="Flash the pre-release, or read the guide first. Props off for the bench work.",
    ),
    "it": dict(
        cta_fw="Installa il firmware", cta_qs="Guida rapida",
        stats=[("0,48 g", "peso della scheda"), ("22", "token OSD"), ("4", "camere abbinate"), ("2–6", "zone sull'interruttore"), ("0", "comandi che toccano il volo")],
        act_h="Guardalo in azione", act_s="Cosa fa RecLink mentre voli, e cosa imposti a terra.",
        acts=[("rec", "Arma e registra", "La registrazione parte quando armi, da un interruttore della radio, o con entrambi. Ogni comando viene verificato su ciò che la camera riporta davvero."),
              ("osd", "Lo stato nei goggles", "Stato di registrazione, tempi, batteria, spazio SD e impostazioni sull'OSD di Betaflight, su quattro righe che disegni tu."),
              ("wifi", "Configura dal telefono", "La scheda apre un suo Wi-Fi finché sei disarmato. Nessuna app, nessun cloud, nessun account. Si spegne appena armi.")],
        osd_h="Il tuo OSD, a modo tuo", osd_cap="Lo alimenta una camera simulata, con gli stessi token che usi nel configuratore. Scegli tu cosa mettere su ognuna delle quattro righe da 16 caratteri.",
        osd_sets=[("Stato completo", OSD_TPL[0]), ("Minimale", OSD_TPL[1]), ("Nome e GPS", OSD_TPL[2]), ("Impostazioni camera", OSD_TPL[3])],
        osd_note="Un valore che la camera non ha confermato resta vuoto, mai 0 né un'ipotesi.",
        feat_h="Tutto quello che fa", feat_s="Una piccola scheda, nove compiti.",
        feats=[("rec", "Registra insieme al velivolo", "Avvio e stop all'arm, da un interruttore, arm OPPURE interruttore, o arm E interruttore. Ogni comando è confermato dalla camera prima di andare avanti."),
               ("zones", "Zone dell'interruttore", "Un interruttore a 2–6 posizioni cambia le impostazioni della camera in volo. Su GoPro ogni zona imposta risoluzione, frame rate, lente, HyperSmooth e Protune; su DJI ogni zona sceglie una modalità."),
               ("osd", "22 token OSD", "Stato, tempo trascorso e rimanente, batteria, spazio SD in minuti o GB, risoluzione, frame rate, lente, profilo colore, segnale e GPS del FC."),
               ("tag", "Tag di highlight", "Segna il momento migliore con un interruttore a impulso: un tag HiLight su GoPro, il tasto Quick-Switch su DJI."),
               ("cams", "Fino a 4 camere", "Abbina qualsiasi mix di GoPro e DJI. All'accensione RecLink si collega a quella abbinata con il segnale più forte."),
               ("clock", "Sincronizzazione orologio", "Imposta l'orologio della camera dall'ora GPS del flight controller, così i filmati hanno la data giusta."),
               ("gps", "Posizione GPS alla DJI", "In opzione invia posizione e ora del velivolo a una camera DJI per il suo overlay di telemetria."),
               ("eye", "OSD analogico e digitale", "La modalità digitale limita l'output ai glifi che l'OSD dei goggles DJI sa disegnare, così niente diventa un punto interrogativo."),
               ("wifi", "Configuratore web e OTA", "Abbina, crea le zone, modifica l'OSD e aggiorna il firmware da una pagina web. Il Wi-Fi è attivo solo da disarmati.")],
        cam_h="Camere compatibili", cam_s="Due marchi via Bluetooth LE. Ecco cosa è verificato e cosa no.",
        cams=[("GoPro", "HERO 9 / 10 / 11 / 12 / 13", "Open GoPro BLE", "bench", "Provata a banco",
               "Registrazione, telemetria OSD e zone basate sulle impostazioni sono verificate su una HERO11 Black. Gli altri modelli della stessa generazione usano la stessa API."),
              ("GoPro", "Mission 1 / Mission 1 Pro", "Open GoPro BLE", "unv", "Non verificata",
               "Dovrebbe funzionare, ma potrebbe richiedere id di impostazione che questo firmware non usa ancora. Non provata."),
              ("DJI", "Osmo Action 4 / 5 Pro / 6, Osmo Nano, Osmo 360", "DUML via BLE", "exp", "Sperimentale",
               "Registrazione, cambio modalità e stato sono implementati dalla demo open source di DJI. Nessuna camera DJI è stata ancora provata."),
              ],
        cam_note="HERO8 e precedenti non hanno l'API Bluetooth Open GoPro e non sono supportate.",
        mx_h="Cosa sa fare ogni camera",
        mx_cols=("Funzione", "GoPro", "DJI"),
        mx_rows=[("Connessione e riconnessione automatica", OK, UN, "", ""),
                 ("Telemetria OSD (rec, batteria, SD, tempi)", OK, UN, "", ""),
                 ("Lettura di risoluzione, frame rate e modalità", OK, UN, "", ""),
                 ("Avvio / stop registrazione", OK, UN, "", ""),
                 ("Zone: impostazioni della camera", OK, NO, "", "Non disponibile"),
                 ("Zone: modalità della camera", NO, UN, "Non disponibile", ""),
                 ("Tag di highlight", UN, PA, "", "Al suo posto il tasto Quick-Switch"),
                 ("Sincronizzazione orologio dal GPS", UN, PA, "", "Alla cieca: senza verifica"),
                 ("Posizione GPS del velivolo alla camera", NO, UN, "Non disponibile", "")],
        mx_leg=[("ok", "Supportato, provato a banco"), ("un", "Implementato, non confermato su hardware"), ("pa", "Funziona con limiti"), ("no", "Non disponibile")],
        safe_h="Fatto per non dare fastidio", safe_s="RecLink è un passeggero. Se si guasta, il peggio che succede è un testo OSD non aggiornato.",
        safes=[("shield", "Passeggero, non pilota", "Legge solo dal flight controller e scrive testo OSD. Arming, RC, PID e navigazione sono fuori portata, e il codice rifiuta quei comandi da solo."),
               ("fail", "Se si rompe, si spegne in silenzio", "Qualsiasi guasto lascia il velivolo perfettamente pilotabile. Dopo un guasto la scheda si riavvia in circa 300 ms e la camera si ricollega da sola."),
               ("wifi", "Wi-Fi solo a terra", "Il punto di accesso si spegne entro 100 ms dall'arm. In volo è attivo solo il Bluetooth."),
               ("mem", "Non aspetta mai la camera", "Ogni comando alla camera parte e viene confermato dopo, e nulla nel percorso di volo alloca memoria.")],
        pt_h="Il configuratore", pt_s="Collegati al Wi-Fi RECLINK da disarmato e qualsiasi pagina lo apre. Sei schede coprono tutto.",
        pts=[("Stato", "Stato del collegamento, telemetria della camera e diagnostica MSP in tempo reale."),
             ("Controllo cam", "Modalità di registrazione, trigger arm e interruttore con rilevamento AUX in un tocco, il costruttore di zone."),
             ("OSD", "Scegli analogico o digitale, trascina i token sulle quattro righe, anteprima dal vivo."),
             ("Abbinamento", "Abbina, elenca e dimentica le camere, con una procedura guidata per GoPro."),
             ("Rete", "Credenziali Wi-Fi, baud rate MSP, scambio TX/RX e potenza radio."),
             ("Sistema", "Luminosità LED, aggiornamento firmware via Wi-Fi, ripristino di fabbrica.")],
        go_h="Dalla scatola alla registrazione", go_s="Circa quindici minuti. La guida rapida descrive ogni passaggio con le immagini.",
        gos=[("Cablala", "Collega la scheda a una UART libera del flight controller."),
             ("Caricala", "Installa il firmware dal browser via USB."),
             ("Abbina la camera", "Apri il configuratore e abbina la GoPro o la DJI."),
             ("Imposta gli interruttori", "Scegli quando registrare, crea le zone, disegna l'OSD.")],
        need_h="Cosa ti serve", need_s="Quattro cose.",
        needs=[("Una scheda RecLink", "La scheda ESP32-C3 personalizzata, in sviluppo. Nel frattempo una scheda di sviluppo ESP32-C3 o ESP32-S3 esegue lo stesso firmware."),
               ("Betaflight 2025.12 o successivo", "MSP API 1.47 o superiore, per i messaggi OSD personalizzati."),
               ("Una camera supportata", "GoPro HERO 9 o successiva, oppure una DJI Osmo (sperimentale)."),
               ("Una UART libera", "Una porta seriale libera sul flight controller.")],
        more_h="Continua a esplorare",
        end_h="Pronto a provarlo?", end_s="Carica la pre-release, oppure leggi prima la guida. Eliche rimosse per le prove a banco.",
    ),
}

BADGE_CLS = {"bench": "good", "unv": "warn", "exp": "warn"}


def render(lang, ctx, cards_html):
    c = C[lang]
    p = ctx["pages"]
    meta = "".join(f"<span>{E(m)}</span>" for m in ctx["meta"])
    esc = E

    hero = (f'<div class="hero rl-hero"><div class="rl-hero-txt"><h1 class="logo-h1">{ctx["mark"]}RecLink</h1>'
            f'<p class="sub">{ctx["home_sub"]}</p><div class="meta">{meta}</div>'
            f'<p class="cta-row"><a class="btn lg" href="../flash/">{ctx["icons"]["fw"]}{c["cta_fw"]}</a>'
            f'<a class="btn lg alt" href="{p["qs"]}">{ctx["icons"]["qs"]}{c["cta_qs"]}</a>'
            f'<a class="btn lg alt" href="{ctx["gh_url"]}" target="_blank" rel="noopener">{ctx["gh_svg"]}{ctx["gh"]}</a></p></div>'
            f'<div class="rl-hero-img"><img src="../assets/board/board-iso.webp" alt="" width="640" height="640" loading="eager" decoding="async"></div></div>')

    callout = f'<div class="callout danger"><span class="tag">{ctx["pre_tag"]}</span><p>{ctx["pre"]}</p></div>'

    stats = "".join(f'<li><b>{esc(n)}</b><span>{esc(l)}</span></li>' for n, l in c["stats"])
    stats = f'<ul class="rl-stats">{stats}</ul>'

    acts = "".join(f'<article class="act"><span class="ico">{I[k]}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for k, t, d in c["acts"])
    sets = c["osd_sets"]
    osd_lines = "".join(f"<span>{esc(expand(l))}</span>" for l in sets[0][1])
    tpl_txt = esc("\n".join(sets[0][1]))
    sets_json = esc(json.dumps([s[1] for s in sets], ensure_ascii=False))
    dots = "".join(f'<button type="button" class="osd-dot{" on" if i == 0 else ""}" aria-label="{esc(s[0])}" data-i="{i}"></button>' for i, s in enumerate(sets))
    labels_json = esc(json.dumps([s[0] for s in sets], ensure_ascii=False))
    show = (f'<section class="rl-sec" id="action"><h2 class="sec">{c["act_h"]}</h2><p class="sec-s">{c["act_s"]}</p>'
            f'<div class="acts">{acts}</div>'
            f'<div class="osd-demo"><div class="osd-cap"><h3>{c["osd_h"]}</h3><p>{c["osd_cap"]}</p><p class="osd-note">{c["osd_note"]}</p></div>'
            f'<div class="osd-wrap"><div class="osd-screen" role="img" aria-label="{esc(c["osd_cap"])}" data-sets="{sets_json}" data-labels="{labels_json}"><div class="osd-lines">{osd_lines}</div></div>'
            f'<div class="osd-bar"><span class="osd-label">{esc(sets[0][0])}</span><span class="osd-dots">{dots}</span></div><pre class="osd-tpl" aria-hidden="true">{tpl_txt}</pre></div></div></section>')

    feats = "".join(f'<article class="feat"><span class="ico">{I[k]}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></article>' for k, t, d in c["feats"])
    feat = f'<section class="rl-sec" id="features"><h2 class="sec">{c["feat_h"]}</h2><p class="sec-s">{c["feat_s"]}</p><div class="feats">{feats}</div></section>'

    cams = "".join(
        f'<article class="cam"><div class="cam-top"><span class="brand-t">{esc(b)}</span><span class="badge {BADGE_CLS[k]}">{esc(bt)}</span></div>'
        f'<h3>{esc(m)}</h3><p class="proto">{esc(pr)}</p><p>{esc(d)}</p></article>'
        for b, m, pr, k, bt, d in c["cams"])
    rows = ""
    for name, g, d, gt, dt in c["mx_rows"]:
        rows += (f'<tr><th scope="row">{esc(name)}</th><td>{g.format(t=esc(gt or ""))}</td><td>{d.format(t=esc(dt or ""))}</td></tr>')
    # the glyph markup carries a visible caption only when there is one (partial / unavailable notes)
    legend = "".join(f'<li>{ {"ok": OK, "un": UN, "pa": PA, "no": NO}[k].format(t="")}<span>{esc(t)}</span></li>' for k, t in c["mx_leg"])
    cam = (f'<section class="rl-sec" id="cameras"><h2 class="sec">{c["cam_h"]}</h2><p class="sec-s">{c["cam_s"]}</p>'
           f'<div class="cams">{cams}</div><p class="fine">{c["cam_note"]}</p>'
           f'<h3 class="mx-h">{c["mx_h"]}</h3><div class="mx-wrap"><table class="mx"><thead><tr><th>{c["mx_cols"][0]}</th><th>{c["mx_cols"][1]}</th><th>{c["mx_cols"][2]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
           f'<ul class="mx-leg">{legend}</ul></section>')

    safes = "".join(f'<article class="safe"><span class="ico">{I[k]}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for k, t, d in c["safes"])
    safe = f'<section class="rl-sec" id="safety"><h2 class="sec">{c["safe_h"]}</h2><p class="sec-s">{c["safe_s"]}</p><div class="safes">{safes}</div></section>'

    pts = "".join(f'<li><b>{esc(t)}</b><span>{esc(d)}</span></li>' for t, d in c["pts"])
    portal = f'<section class="rl-sec" id="portal"><h2 class="sec">{c["pt_h"]}</h2><p class="sec-s">{c["pt_s"]}</p><ul class="tabs-list">{pts}</ul></section>'

    gos = "".join(f'<li><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for t, d in c["gos"])
    go = (f'<section class="rl-sec" id="start"><h2 class="sec">{c["go_h"]}</h2><p class="sec-s">{c["go_s"]}</p>'
          f'<ol class="go">{gos}</ol></section>')

    needs = "".join(f'<article class="need"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in c["needs"])
    need = f'<section class="rl-sec" id="need"><h2 class="sec">{c["need_h"]}</h2><p class="sec-s">{c["need_s"]}</p><div class="needs">{needs}</div></section>'

    more = f'<section class="rl-sec" id="more"><h2 class="sec">{c["more_h"]}</h2><div class="cards">{cards_html}</div></section>'

    end = (f'<section class="rl-end"><h2>{c["end_h"]}</h2><p>{c["end_s"]}</p><p class="cta-row center">'
           f'<a class="btn lg" href="../flash/">{ctx["icons"]["fw"]}{c["cta_fw"]}</a>'
           f'<a class="btn lg alt" href="{ctx["gh_url"]}" target="_blank" rel="noopener">{ctx["gh_svg"]}{ctx["gh"]}</a></p></section>')

    return hero + callout + stats + show + feat + cam + safe + portal + go + need + more + end + OSD_JS


# Live OSD preview: a simulated camera (connects, arms, records) feeds the same %tokens the firmware uses,
# and the page rotates through the example layouts. Reduced-motion users get a static first layout.
OSD_JS = r"""<script>
(function(){
  var s=document.querySelector('.osd-screen'); if(!s) return;
  var T=JSON.parse(s.getAttribute('data-sets')), labels=JSON.parse(s.getAttribute('data-labels'));
  var lines=s.querySelectorAll('.osd-lines span'), lab=document.querySelector('.osd-label'), dots=document.querySelectorAll('.osd-dot'), tpl=document.querySelector('.osd-tpl');
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var layout=0, sim=0, tick=null, rot=null;
  // simulated camera + FC: tokens stay blank until the camera has confirmed them (blank-on-unconfirmed)
  function values(t){
    var cam=t>=2, rec=t>=5, el=rec?t-5:0;
    var m=function(n){return Math.floor(n/60)+':'+('0'+(n%60)).slice(-2);};
    var rem=Math.max(0,5640-el), rm=Math.ceil(rem/60);
    var v={cn:'MY CINEWHOOP', gf:'3D', gs:String(13+Math.round(1.2*Math.sin(t/9)))};
    if(cam){
      v.st=rec?'REC':'IDLE'; v.et=m(el); v.bt=(87-Math.floor(el/54))+'%';
      v.rs='5.3K'; v.fp='60'; v.ln='WIDE'; v.md='VIDEO'; v.pr='HLG'; v.bd='10b'; v.ar='16:9';
      v.rt=rm>=100?Math.floor(rm/60)+'h':rm+'m'; v.sd=v.rt;
      v.sg=(38.4-0.1*Math.floor(el/7)).toFixed(1)+'G';
      v.cr=String(-62+Math.round(3*Math.sin(t/3)+2*Math.sin(t/1.7)));
    }
    return v;
  }
  function expand(tp,v){ return tp.replace(/%([a-z]{2})/g,function(x,k){ return k in v?v[k]:(/^(st|et|bt|rs|fp|ln|md|pr|bd|ar|rt|sd|sg|cr)$/.test(k)?'':x); }).replace(/\s+$/,'').slice(0,16); }
  function paint(){
    var v=values(sim), tp=T[layout];
    for(var k=0;k<lines.length;k++) lines[k].textContent=expand(tp[k]||'',v);
  }
  function show(n){
    layout=n; paint(); lab.textContent=labels[n]; tpl.textContent=T[n].join('\n');
    for(var d=0;d<dots.length;d++) dots[d].classList.toggle('on',d===n);
  }
  function go(n){ s.classList.add('swap'); setTimeout(function(){ show(n); s.classList.remove('swap'); },260); }
  function start(){
    stop(); if(reduce) return;
    tick=setInterval(function(){ sim=(sim+1)%150; paint(); },1000);
    rot=setInterval(function(){ go((layout+1)%T.length); },7000);
  }
  function stop(){ if(tick){clearInterval(tick);tick=null;} if(rot){clearInterval(rot);rot=null;} }
  for(var d=0;d<dots.length;d++) dots[d].addEventListener('click',function(){ go(+this.getAttribute('data-i')); start(); });
  document.addEventListener('visibilitychange',function(){ document.hidden?stop():start(); });
  if(reduce){ sim=40; }
  show(0); start();
})();
</script>"""
