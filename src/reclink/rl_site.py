"""The RecLink main page (EN/IT) and the FPVitt landing page, on the tasteskill design kit.

Deal (tech hardware, page type product): hero `product`, nav-cards, footer-dark, close-type, rhythm brand-band,
buttons solid; palette: the client's own green on warm stone (start.mjs brand), type IBM Plex Sans + Mono,
radius soft; moments: liquid-type (the safety statement) and line-carries-colour (the configurator on the
brand band); effect: grain-gradient behind the OSD window (the one [data-visual] frame).

The guides, the board explorer and the installer keep their own stylesheet (web/site.css); only the two
pages built here load the kit from RecLink/assets/kit/.
"""
import html
import json
import os

E = html.escape

# ----------------------------------------------------------------------------- shared head and tokens
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400..700&'
         'family=Geist+Mono:wght@400..500&display=swap" rel="stylesheet">')

ROOT_TOKENS = """:root {
  --p-bg: #dfdedb; --p-surface: #d5d4d0; --p-ink: #26251e; --p-muted: #57564f;
  --p-accent: #14632b; --p-accent-ink: #ffffff; --p-action: #14632b; --p-action-ink: #ffffff;
  --p-inv-bg: #26251e; --p-inv-surface: #313029; --p-inv-ink: #dfdedb; --p-inv-muted: #9e9d99;
  --p-inv-accent: #14632b; --p-inv-accent-ink: #ffffff; --p-inv-action: #14632b; --p-inv-action-ink: #ffffff;
  --font-display: "Geist", system-ui, sans-serif;
  --font-text: "Geist", system-ui, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --display-weight: 500;
  --display-tracking: -0.035em;
  --display-tracking-xl: -0.045em;
}"""

LOGO = ('<svg class="rl-logo" viewBox="0 0 168 80" aria-hidden="true"><path fill="currentColor" '
        'd="M6 6h30v12H18v44h18v12H6zM132 6h30v68h-30V62h18V18h-18z"/><circle fill="currentColor" cx="84" cy="40" r="21"/></svg>')
ARROW = '<svg class="m-arrow" viewBox="0 0 12 12" aria-hidden="true"><path class="m-arrow__stem" d="M1 6h8"/><path class="m-arrow__head" d="M4.5 2.5 8 6l-3.5 3.5"/></svg>'
GH_SVG = ('<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')

REPO = "https://github.com/FPVitt/RecLink"
FW = "0.2.1"


def head(lang, title, desc, seo, rel, favicon, theme="#dfdedb", extra_css="", note=None):
    """Everything up to </head>. rel is the path from the page to the RecLink/ folder ("../" or "RecLink/")."""
    k = rel + "assets/kit/"
    return f'''<!doctype html>
<!-- type: product (hardware, site-kind tech) · deal: hero product, nav-cards, footer-dark, close-type, rhythm brand-band, buttons solid,
     mark: the client's own logo · palette: the client's green on warm stone, IBM Plex · radius soft
     moments: liquid-type (the safety statement), line-carries-colour (the configurator band) · effect: grain-gradient (OSD frame) -->
<html lang="{lang}" data-type="product" data-radius="soft" data-buttons="solid" data-motion>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc, quote=True)}">
<meta name="theme-color" content="{theme}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title, quote=True)}">
<meta property="og:description" content="{E(desc, quote=True)}">
<meta name="site-kind" content="tech">
<meta name="page-type" content="product">
<link rel="icon" type="image/svg+xml" href="{favicon}">
{seo}
{FONTS}
<link rel="stylesheet" href="{k}system.css">
<link rel="stylesheet" href="{k}ui/cards.css">
<link rel="stylesheet" href="{k}motion/motion.css">
<link rel="stylesheet" href="{k}backgrounds/backgrounds.css">
<link rel="stylesheet" href="{k}layout/layout.css">
<link rel="stylesheet" href="{k}icons/icon.css">
<style>
{ROOT_TOKENS}
</style>
<link rel="stylesheet" href="{k}ui/base.css">
<link rel="stylesheet" href="{k}diagrams/diagram.css">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script src="{k}backgrounds/backgrounds.js"></script>
<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>
<link rel="modulepreload" href="{k}moments/moments.js"><link rel="modulepreload" href="{k}moments/lib.js">
<link rel="stylesheet" href="{rel}assets/home.css">
{extra_css}
</head>
'''


def scripts(rel, extra=""):
    k = rel + "assets/kit/"
    return (f'<script src="{rel}assets/stats.js" defer></script>\n'
            f'<script src="{k}system.js" type="module"></script>\n'
            f'<script src="{k}layout/layout.js" type="module"></script>\n'
            f'<script src="{k}motion/motion.js" type="module"></script>\n'
            f'<script src="{k}diagrams/mount.js" type="module"></script>\n{extra}')


# ----------------------------------------------------------------------------- copy
OSD_TPL = [
    ["%st %et  %bt", "%rs %fp %ln", "%sd %sg", "%md %pr"],
    ["", "%st %et", "", ""],
    ["%st %et", "SD %sd left", "%sg FREE", "BAT %bt"],
    ["%rs %fp %ln", "%pr %bd %ar", "%cr dBm  %bt", "%st %et"],
]
OSD_STATIC = dict(st="REC", et="0:00", bt="87%", rs="5.3K", fp="60", ln="WIDE", sd="94m", sg="38.4G", md="VIDEO", pr="HLG",
                  bd="10b", ar="16:9", cr="-62")


def expand(tpl):
    import re
    return re.sub(r"%([a-z]{2})", lambda m: OSD_STATIC.get(m.group(1), m.group(0)), tpl)[:16]


# status glyphs of the compatibility matrix
OK = '<span class="cm ok" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg><i>{t}</i></span>'
UN = '<span class="cm un" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2.4 2"/><path d="M5.4 8.3l1.9 1.9 3.4-3.7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg><i>{t}</i></span>'
PA = '<span class="cm pa" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M8 2a6 6 0 0 0 0 12z" fill="currentColor"/></svg><i>{t}</i></span>'
NO = '<span class="cm no" title="{t}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 8h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><i>{t}</i></span>'

# lucide interface glyphs (ISC), inline so they take the text colour
G = {
    "rec": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3" fill="currentColor"/>',
    "zones": '<line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="16" x2="16" y1="18" y2="22"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "cams": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "wifi": '<path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/><path d="M5 12.859a10 10 0 0 1 14 0"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
}


def glyph(k, cls="rl-glyph"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round">{G[k]}</svg>')


C = {
    "en": dict(
        lang="en", other="it", other_name="Italiano", other_href="../it/",
        title="RecLink: Betaflight camera link for GoPro and DJI Osmo",
        desc="Open-source ESP32 firmware that starts recording on arm, shows camera status on your Betaflight OSD and syncs the camera clock. Runs on a 0.68 g board or an ESP32 dev board.",
        skip="Skip to content", menu="Menu",
        nav=[("Features", "#features"), ("Cameras", "#cameras"), ("Boards", "#boards")], guides="Guides",
        guide_cards=[("quick-start.html", "Quick start", "Wire, flash and pair in about 15 minutes.", "binding"),
                     ("user-guide.html", "User guide", "Every setting and indicator, with screenshots.", "first"),
                     ("the-board.html", "The board in 3D", "Take the RecLink board apart, layer by layer.", "board")],
        cta="Install the firmware", cta_qs="Read the quick start",
        notice=f"Pre-release {FW}. Tested on the bench, never in flight.",
        h1="Betaflight camera link for GoPro and DJI",
        lead="Open-source ESP32 firmware that records on arm or from a radio switch and shows camera status on your OSD. It never touches flight, and it fits a 0.68 g board.",
        hero_alt="The three boards RecLink runs on: the RecLink board, the ESP32-C3 SuperMini and the ESP32-S3-Zero",
        safe_h="Passenger, not pilot",
        safe_lead="RecLink reads from the flight controller and writes OSD text. Nothing it sends can change how the quad flies.",
        safes=[("Only reads from Betaflight", "It writes OSD text and nothing else. The code refuses arming, RC and PID commands."),
               ("Restarts the link after a fault", "The board is back in about 300 ms and the quad stays fully flyable."),
               ("Wi-Fi link goes off on arm", "The access point is down within 100 ms. In flight only Bluetooth runs."),
               ("Never waits on the camera", "Commands go out and are confirmed afterwards, so a slow camera stalls nothing.")],
        con_h="One board between FC and camera",
        con_lead="One small board sits between Betaflight and the camera. It reads arm state, switches and GPS time over MSP, and talks to the camera over Bluetooth LE.",
        con_link="Read the wiring steps",
        dg=dict(alt="Arm state, an AUX switch and GPS time from Betaflight go into RecLink. Out come recording, camera settings and the camera clock.",
                src=[("Arm state", "ui:power", "MSP"), ("AUX switch", "ui:toggle-right", "MSP"), ("GPS time", "ui:map-pin", "MSP")],
                core=("RecLink", "ui:cpu"),
                dst=[("Recording", "ui:video", "start, stop"), ("Settings", "ui:sliders-horizontal", "2 to 6 zones"), ("Clock", "ui:clock", "from GPS")]),
        osd_h="Camera status on your OSD",
        osd_lead="Four lines of 16 characters, built from 22 tokens you place yourself.",
        osd_link="Read the OSD guide",
        osd_sets=["Full status", "Minimal", "Card and battery", "Camera settings"],
        osd_pause="Pause the demo", osd_play="Play the demo", osd_alt="Simulated OSD text, four lines of 16 characters",
        osd_sub="Simulated camera",
        feat_h="RecLink features",
        feats=[("rec", "Records the camera on arm or a switch", "Arm, a switch, either, or both. The camera confirms every command."),
               ("zones", "Changes camera settings in flight", "A 2 to 6 position switch picks resolution, frame rate and lens on a GoPro."),
               ("tag", "Tags a moment on the camera", "A momentary switch adds a HiLight tag on a GoPro, a Quick-Switch press on a DJI."),
               ("cams", "Pairs up to 4 cameras", "Any mix of GoPro and DJI. At power-up it joins the strongest signal."),
               ("clock", "Sets the camera clock", "Time comes from the flight controller's GPS, so footage is dated correctly."),
               ("eye", "Draws Betaflight OSD, analog or digital", "Digital mode keeps to the glyphs the DJI goggles can draw.")],
        cfg_h="Set up the camera link from your phone",
        cfg_lead="Join the RECLINK Wi-Fi while disarmed. Pair cameras, build zones, lay out the OSD and update the firmware. No app, no cloud, no account.",
        cfg_tabs=["Status", "Cam control", "OSD", "Binding", "Network", "System"],
        cfg_alts=["The configurator's status page: aircraft disarmed, camera link ready", "Record settings: trigger on a radio switch with the AUX channel and its threshold", "Binding: paired GoPro HERO11 Black connected, DJI Osmo Action 5 in standby"],
        status_alt="The status page with live camera values: link, recording time, resolution, battery and SD card",
        zones_alt="Zone builder in the configurator: a six-position switch with camera settings for each zone",
        cam_h="Compatible cameras",
        cam_lead="Two brands over Bluetooth LE. What is verified and what is not.",
        cams=[("GoPro", "HERO 9 to 13", "Open GoPro BLE", "good", "Bench-tested", "Record, OSD telemetry and zones work on a HERO11 Black. The other models use the same API."),
              ("GoPro", "Mission 1 and Mission 1 Pro", "Open GoPro BLE", "warn", "Unverified", "Expected to work, but it may need setting ids this firmware does not use yet."),
              ("DJI", "Osmo Action 4, 5 Pro and 6, Osmo Nano, Osmo 360", "DUML over BLE", "warn", "Experimental", "Implemented from DJI's open-source demo. No DJI camera has been tested yet.")],
        cam_note="HERO8 and older have no Bluetooth API and are not supported.",
        mx_cols=("Feature", "GoPro", "DJI"),
        mx_rows=[("Connect and auto-reconnect", OK, UN),
                 ("OSD telemetry: record, battery, SD, timers", OK, UN),
                 ("Resolution, frame rate and mode readout", OK, UN),
                 ("Start and stop recording", OK, UN),
                 ("Zones as camera settings", OK, NO),
                 ("Zones as camera mode", NO, UN),
                 ("Highlight tag (DJI uses Quick-Switch)", UN, PA),
                 ("Clock sync from FC GPS (DJI: no read-back)", UN, PA),
                 ("Aircraft position to the camera", NO, UN)],
        mx_words=dict(ok="Tested", un="Unconfirmed", pa="Limited", no="No"),
        mx_note="Tested: bench-tested on hardware. Unconfirmed: implemented, awaiting a hardware test.",
        mx_h="What each camera can do",
        brd_h="Firmware for the board you have",
        brd_lead="The same firmware runs on all three. You do not need the RecLink board.",
        brds=[("RecLink camera board", "board-iso", "warn", "In development", "0.68 g, 12 × 13 mm, four solder pads: GND, 5V, TX and RX.", "FC TX to RX, FC RX to TX"),
              ("ESP32-C3 SuperMini", "supermini", "good", "Supported", "A tiny, cheap dev board. Flash it from your browser over USB.", "FC TX to pin 7, RX to pin 6"),
              ("Waveshare ESP32-S3-Zero", "s3zero", "good", "Supported", "Its RGB LED shows the status in colour. Flash it over USB.", "FC TX to pin 4, RX to pin 5")],
        needs=[("Flight controller", "Betaflight 2025.12 or newer"), ("Camera", "GoPro HERO 9 or newer, or a DJI Osmo"), ("Wiring", "One free UART"), ("Licence", "GPL-3.0, free software")],
        close_h="Put RecLink on your quad", close_lead="About fifteen minutes from the box to your first recording. Props off for the bench work.",
        foot_lede="Open-source firmware that links Betaflight to a GoPro or DJI Osmo.",
        cols=[("Guides", [("quick-start.html", "Quick start"), ("user-guide.html", "User guide"), ("the-board.html", "The board")]),
              ("Firmware", [("../flash/", "Installer"), (REPO + "/releases", "Releases"), (REPO, "Source code")]),
              ("Project", [(REPO + "/blob/main/LICENSE", "GPL-3.0 licence"), ("https://fpvitt.github.io/", "FPVitt")])],
        legal=f"Firmware {FW} (pre-release) · free software, GPL-3.0",
        marks="GoPro, DJI, Betaflight and Espressif are trademarks of their owners.",
        statline="Anonymous visit statistics (GoatCounter), no cookies.",
    ),
    "it": dict(
        lang="it", other="en", other_name="English", other_href="../en/",
        title="RecLink: collegamento camera per Betaflight, GoPro e DJI Osmo",
        desc="Firmware ESP32 open source che avvia la registrazione all'arm, mostra lo stato della camera nell'OSD di Betaflight e sincronizza l'orologio. Gira su una scheda da 0,68 g o su una scheda ESP32.",
        skip="Vai al contenuto", menu="Menu",
        nav=[("Funzioni", "#features"), ("Camere", "#cameras"), ("Schede", "#boards")], guides="Guide",
        guide_cards=[("guida-rapida.html", "Guida rapida", "Cabla, carica e abbina in circa 15 minuti.", "binding"),
                     ("guida-utente.html", "Guida utente", "Ogni impostazione e indicatore, con schermate.", "first"),
                     ("la-scheda.html", "La scheda in 3D", "Smonta la scheda RecLink, strato per strato.", "board")],
        cta="Installa il firmware", cta_qs="Leggi la guida rapida",
        notice=f"Pre-release {FW}. Provato a banco, mai in volo.",
        h1="Collegamento camera per Betaflight, GoPro e DJI",
        lead="Firmware ESP32 open source che registra all'arm o da un interruttore e mostra lo stato della camera nell'OSD. Non tocca mai il volo e sta su una scheda da 0,68 g.",
        hero_alt="Le tre schede su cui gira RecLink: la scheda RecLink, la ESP32-C3 SuperMini e la ESP32-S3-Zero",
        safe_h="Passeggero, non pilota",
        safe_lead="RecLink legge dal flight controller e scrive testo OSD. Niente di ciò che invia può cambiare il modo in cui vola il quad.",
        safes=[("Legge solo da Betaflight", "Scrive solo testo OSD. Il codice rifiuta i comandi di arming, RC e PID."),
               ("Riavvia il collegamento dopo un guasto", "La scheda torna in circa 300 ms e il quad resta pilotabile."),
               ("Collegamento Wi-Fi spento all'arm", "Il punto di accesso si spegne entro 100 ms. In volo gira solo il Bluetooth."),
               ("Non aspetta mai la camera", "I comandi partono e si confermano dopo, quindi una camera lenta non blocca nulla.")],
        con_h="Una scheda tra FC e camera",
        con_lead="Una piccola scheda sta tra Betaflight e la camera. Legge stato dell'arm, interruttori e ora GPS via MSP, e parla con la camera via Bluetooth LE.",
        con_link="Leggi i passi di cablaggio",
        dg=dict(alt="Stato dell'arm, un interruttore AUX e l'ora GPS di Betaflight entrano in RecLink. Escono registrazione, impostazioni della camera e orologio della camera.",
                src=[("Stato arm", "ui:power", "MSP"), ("Interruttore AUX", "ui:toggle-right", "MSP"), ("Ora GPS", "ui:map-pin", "MSP")],
                core=("RecLink", "ui:cpu"),
                dst=[("Registrazione", "ui:video", "avvio, stop"), ("Impostazioni", "ui:sliders-horizontal", "2-6 zone"), ("Orologio", "ui:clock", "dal GPS")]),
        osd_h="Lo stato della camera nell'OSD",
        osd_lead="Quattro righe da 16 caratteri, composte con 22 token che piazzi tu.",
        osd_link="Leggi la guida all'OSD",
        osd_sets=["Stato completo", "Minimale", "SD e batteria", "Impostazioni camera"],
        osd_pause="Metti in pausa la demo", osd_play="Riavvia la demo", osd_alt="Testo OSD simulato, quattro righe da 16 caratteri",
        osd_sub="Camera simulata",
        feat_h="Funzioni di RecLink",
        feats=[("rec", "Registra la camera all'arm o da interruttore", "Arm, interruttore, uno dei due o entrambi. La camera conferma ogni comando."),
               ("zones", "Cambia le impostazioni in volo", "Un interruttore a 2-6 posizioni sceglie risoluzione, frame rate e lente su GoPro."),
               ("tag", "Segna un momento sulla camera", "Un interruttore a impulso aggiunge un tag HiLight su GoPro, il Quick-Switch su DJI."),
               ("cams", "Abbina fino a 4 camere", "Qualsiasi mix di GoPro e DJI. All'accensione sceglie il segnale più forte."),
               ("clock", "Imposta l'orologio della camera", "L'ora arriva dal GPS del flight controller, così i filmati hanno la data giusta."),
               ("eye", "Disegna l'OSD Betaflight, analogico o digitale", "La modalità digitale usa solo i glifi che i goggles DJI sanno disegnare.")],
        cfg_h="Imposta il collegamento camera dal telefono",
        cfg_lead="Collegati al Wi-Fi RECLINK da disarmato. Abbina le camere, crea le zone, disegna l'OSD e aggiorna il firmware. Nessuna app, nessun cloud, nessun account.",
        cfg_tabs=["Stato", "Controllo cam", "OSD", "Abbinamento", "Rete", "Sistema"],
        cfg_alts=["La pagina di stato del configuratore: velivolo disarmato, camera collegata", "Impostazioni di registrazione: trigger da interruttore con canale AUX e soglia", "Abbinamento: GoPro HERO11 Black collegata, DJI Osmo Action 5 in standby"],
        status_alt="La pagina di stato con i valori in tempo reale della camera: collegamento, tempo di registrazione, risoluzione, batteria e scheda SD",
        zones_alt="Costruttore di zone nel configuratore: un interruttore a sei posizioni con le impostazioni della camera per ogni zona",
        cam_h="Camere compatibili",
        cam_lead="Due marchi via Bluetooth LE. Cosa è verificato e cosa no.",
        cams=[("GoPro", "HERO 9-13", "Open GoPro BLE", "good", "Provata a banco", "Registrazione, telemetria OSD e zone funzionano su una HERO11 Black. Gli altri modelli usano la stessa API."),
              ("GoPro", "Mission 1 e Mission 1 Pro", "Open GoPro BLE", "warn", "Non verificata", "Dovrebbe funzionare, ma potrebbe servire id di impostazione che questo firmware non usa ancora."),
              ("DJI", "Osmo Action 4, 5 Pro e 6, Osmo Nano, Osmo 360", "DUML via BLE", "warn", "Sperimentale", "Implementato dalla demo open source di DJI. Nessuna camera DJI è stata ancora provata.")],
        cam_note="HERO8 e precedenti non hanno l'API Bluetooth e non sono supportate.",
        mx_cols=("Funzione", "GoPro", "DJI"),
        mx_rows=[("Connessione e riconnessione automatica", OK, UN),
                 ("Telemetria OSD: rec, batteria, SD, tempi", OK, UN),
                 ("Lettura di risoluzione, frame rate e modalità", OK, UN),
                 ("Avvio e stop registrazione", OK, UN),
                 ("Zone come impostazioni della camera", OK, NO),
                 ("Zone come modalità della camera", NO, UN),
                 ("Tag di highlight (su DJI il Quick-Switch)", UN, PA),
                 ("Orologio dal GPS del FC (DJI: senza verifica)", UN, PA),
                 ("Posizione del velivolo alla camera", NO, UN)],
        mx_words=dict(ok="Provato", un="Non confermato", pa="Limitato", no="No"),
        mx_note="Provato: provato a banco su hardware. Non confermato: implementato, in attesa di una prova su hardware.",
        mx_h="Cosa sa fare ogni camera",
        brd_h="Firmware per la scheda che hai",
        brd_lead="Lo stesso firmware gira su tutte e tre. Non ti serve la scheda RecLink.",
        brds=[("Scheda RecLink per camere", "board-iso", "warn", "In sviluppo", "0,68 g, 12 × 13 mm, quattro pad da saldare: GND, 5V, TX e RX.", "TX FC a RX, RX FC a TX"),
              ("ESP32-C3 SuperMini", "supermini", "good", "Supportata", "Una scheda minuscola ed economica. Caricala dal browser via USB.", "TX FC al pin 7, RX al pin 6"),
              ("Waveshare ESP32-S3-Zero", "s3zero", "good", "Supportata", "Il LED RGB mostra lo stato a colori. Caricala via USB.", "TX FC al pin 4, RX al pin 5")],
        needs=[("Flight controller", "Betaflight 2025.12 o successivo"), ("Camera", "GoPro HERO 9 o successiva, o una DJI Osmo"), ("Cablaggio", "Una UART libera"), ("Licenza", "GPL-3.0, software libero")],
        close_h="Metti RecLink sul tuo quad", close_lead="Circa quindici minuti dalla scatola alla prima registrazione. Eliche rimosse per le prove a banco.",
        foot_lede="Firmware open source che collega Betaflight a una GoPro o DJI Osmo.",
        cols=[("Guide", [("guida-rapida.html", "Guida rapida"), ("guida-utente.html", "Guida utente"), ("la-scheda.html", "La scheda")]),
              ("Firmware", [("../flash/", "Installer"), (REPO + "/releases", "Release"), (REPO, "Codice sorgente")]),
              ("Progetto", [(REPO + "/blob/main/LICENSE", "Licenza GPL-3.0"), ("https://fpvitt.github.io/", "FPVitt")])],
        legal=f"Firmware {FW} (pre-release) · software libero, GPL-3.0",
        marks="GoPro, DJI, Betaflight ed Espressif sono marchi dei rispettivi proprietari.",
        statline="Statistiche di visita anonime (GoatCounter), nessun cookie.",
    ),
}


def dg_spec(c):
    d = c["dg"]
    spec = {"layout": "bowtie", "size": "band", "alt": d["alt"],
            "sources": [{"label": l, "icon": i, "sub": s} for l, i, s in d["src"]],
            "core": {"label": d["core"][0], "icon": d["core"][1]},
            "targets": [{"label": l, "icon": i, "sub": s} for l, i, s in d["dst"]]}
    return json.dumps(spec, ensure_ascii=False)


def nav_html(c, rel, page="home"):
    cards = ""
    for href, t, d, img in c["guide_cards"]:
        src = {"binding": rel + "assets/board/guide-binding.webp", "first": rel + "assets/board/guide-first.webp",
               "board": rel + "assets/board/board-iso.webp"}[img]
        cards += (f'<a class="menu-card span-4" href="{href}"><div class="panel rl-menu-panel rl-menu--{img}"><img class="frame__img" src="{src}" alt="" loading="lazy"></div>'
                  f'<span class="t-card">{E(t)}</span><span class="t-small muted">{E(d)}</span></a>')
    words = "".join(f'<div class="nav__item"><a class="nav__link" href="{h}">{E(w)}</a></div>' for w, h in c["nav"])
    return f'''<header class="nav">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">{E(c["skip"])}</a>
    <a class="nav__logo" href="#top">{LOGO}RecLink</a>
    <nav class="nav__links" aria-label="Main">
      {words}
      <div class="nav__item"><a class="nav__link" href="{c["guide_cards"][1][0]}">{E(c["guides"])} <svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
        <div class="nav__menu"><div class="wrap grid">{cards}</div></div></div>
      <div class="nav__item"><a class="nav__link" href="{c["other_href"]}" hreflang="{c["other"]}" lang="{c["other"]}">{E(c["other_name"])}</a></div>
    </nav>
    <div class="nav__actions">
      <a class="btn btn--primary" href="../flash/">{E(c["cta"])}</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="{E(c["menu"])}">
      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>'''


def footer_html(c, close_h, close_lead, cta_href, cta, cols, rel_home, brand=None):
    brand = brand or f"{LOGO}RecLink"
    colhtml = "".join(
        f'<div class="span-2 footer__col"><h3>{E(t)}</h3><ul>' + "".join(f'<li><a href="{h}">{E(l)}</a></li>' for h, l in links) + '</ul></div>'
        for t, links in cols)
    return f'''<footer class="footer footer--dark ground-inverse closing" id="contact" aria-labelledby="close-h">
  <div class="wrap">
    <div class="closing__cta close--type">
      <div class="section-head"><h2 id="close-h">{E(close_h)}</h2><p>{E(close_lead)}</p></div>
      <a class="btn btn--primary btn--xl btn--wide" href="{cta_href}">{E(cta)}{ARROW}</a>
    </div>
    <div class="closing__links">
      <div class="grid">
        <div class="span-6 stack-4"><a class="nav__logo" href="#top">{brand}</a><p class="footer__lede">{E(c["foot_lede"])}</p></div>
        {colhtml}
      </div>
      <div class="footer__legal"><span>{E(c["legal"])}</span><span>{E(c["marks"])}</span><a class="rl-gh" href="{REPO}" target="_blank" rel="noopener">{GH_SVG}GitHub</a></div>
    </div>
  </div>
</footer>'''


# ----------------------------------------------------------------------------- the RecLink main page
def render_main(lang, seo, pages_rel="../"):
    c = C[lang]
    rel = "../"
    a = rel + "assets/board/"

    hero = f'''<section class="hero hero--product" data-enter aria-labelledby="hero-h">
    <div class="wrap"><div class="hero-text hero__in">
      <p class="hero-notice">{E(c["notice"])}</p>
      <div class="hero__head">
        <div>
          <h1 id="hero-h">{E(c["h1"])}</h1>
          <p class="hero__lead">{E(c["lead"])}</p>
        </div>
        <div class="btn-row"><a class="btn btn--primary" href="../flash/">{E(c["cta"])}{ARROW}</a><a class="btn btn--secondary" href="{c["guide_cards"][0][0]}">{E(c["cta_qs"])}</a></div>
      </div>
      <div class="hero__stage"><img class="is-cutout" src="{a}lineup.webp" width="2000" height="760" alt="{E(c["hero_alt"])}" fetchpriority="high"></div>
    </div></div>
  </section>'''

    safes = "".join(f'<li><h3>{E(t)}</h3><p>{E(d)}</p></li>' for t, d in c["safes"])
    safety = f'''<section class="section" id="safety" aria-labelledby="safety-h" style="--h: 1"><div class="wrap">
    <div class="rl-statement" data-moment="liquid-type" data-moment-opts='{{"strength": 0.8}}'>
      <h2 class="mo-lt__type" id="safety-h">{E(c["safe_h"])}</h2>
      <p class="t-lead">{E(c["safe_lead"])}</p>
    </div>
    <ul class="rl-points">{safes}</ul>
  </div></section>'''

    connect = f'''<section class="section" id="connect" aria-labelledby="connect-h" style="--h: 1"><div class="wrap">
    <div class="section-head section-head--split"><div><h2 id="connect-h">{E(c["con_h"])}</h2><p>{E(c["con_lead"])}</p></div>
      <a class="link" href="{c["guide_cards"][0][0]}">{E(c["con_link"])}</a></div>
    <div class="panel rl-dg"><div class="dg" data-diagram><script type="application/json">{dg_spec(c)}</script></div></div>
  </div></section>'''

    sets = OSD_TPL
    osd_lines = E("\n".join(expand(l) for l in sets[0]))
    chips = "".join(f'<button type="button" class="rl-chip{" is-on" if i == 0 else ""}" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">{E(n)}</button>' for i, n in enumerate(c["osd_sets"]))
    osd = f'''<section class="section" id="osd" aria-labelledby="osd-h" style="--h: 1"><div class="wrap">
    <div class="section-head section-head--split"><div><h2 id="osd-h">{E(c["osd_h"])}</h2><p>{E(c["osd_lead"])}</p></div>
      <a class="link" href="{c["guide_cards"][1][0]}">{E(c["osd_link"])}</a></div>
    <div class="frame rl-osd" data-visual data-fx="grain-gradient" data-fx-seed="7">
      <div class="rl-osd__chips" role="group" aria-label="{E(c["osd_h"])}">{chips}</div>
      <div class="rl-osd__screen ui" role="img" aria-label="{E(c["osd_alt"])}" data-sets="{E(json.dumps(sets), quote=True)}" data-labels="{E(json.dumps(c["osd_sets"], ensure_ascii=False), quote=True)}">
        <div class="rl-osd__lines" aria-hidden="true">{osd_lines}</div>
      </div>
      <button class="loop-pause" type="button" aria-label="{E(c["osd_pause"])}" aria-pressed="false" data-pause="{E(c["osd_pause"])}" data-play="{E(c["osd_play"])}"><svg viewBox="0 0 14 14" aria-hidden="true"><path class="p-a" d="M3 2h3v10H3zM8 2h3v10H8z"/></svg></button>
    </div>
  </div></section>'''

    feats = "".join(f'<li>{glyph(k)}<div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for k, t, d in c["feats"])
    features = f'''<section class="section" id="features" aria-labelledby="features-h" style="--h: 1; --hm: 2"><div class="wrap">
    <div class="grid grid--top">
      <div class="span-6 rl-text">
        <h2 id="features-h">{E(c["feat_h"])}</h2>
        <ul class="rl-featlist">{feats}</ul>
      </div>
      <div class="rl-pic span-6 start-7"><img src="{rel}assets/board/shot-zones.webp" width="640" height="891" alt="{E(c["zones_alt"])}" loading="lazy"></div>
    </div>
  </div></section>'''

    tabs = "".join(f"<li>{E(t)}</li>" for t in c["cfg_tabs"])
    shots = (f'<img src="{rel}assets/board/shot-first.webp" width="640" height="1376" alt="{E(c["cfg_alts"][0])}" loading="lazy">'
             f'<img src="{rel}assets/board/shot-record.webp" width="640" height="920" alt="{E(c["cfg_alts"][1])}" loading="lazy">')
    config = f'''<section class="section ground-brand" id="configurator" aria-labelledby="cfg-h" style="--h: 1" data-moment="line-carries-colour" data-moment-opts='{{"from": "base"}}'><div class="wrap">
    <div class="grid grid--top">
      <div class="span-6 rl-text">
        <h2 id="cfg-h">{E(c["cfg_h"])}</h2>
        <p class="t-lead">{E(c["cfg_lead"])}</p>
        <ul class="rl-tabs">{tabs}</ul>
      </div>
      <div class="rl-shots span-6 start-7">{shots}</div>
    </div>
  </div></section>'''

    cams = ""
    for brand, model, proto, cls, badge, d in c["cams"]:
        mark = ('<img class="rl-brandmark" data-icon="si:dji" src="../assets/kit/icons/dji.svg" alt="">' if brand == "DJI" else "")
        cams += (f'<li class="rl-cam"><div class="rl-cam__top"><span class="rl-brand">{mark}{E(brand)}</span><span class="rl-badge rl-badge--{cls}">{E(badge)}</span></div>'
                 f'<h3>{E(model)}</h3><p class="rl-proto">{E(proto)}</p><p>{E(d)}</p></li>')
    rows = ""
    for name, g, d in c["mx_rows"]:
        rows += (f'<div class="rl-mx__row" role="row"><span role="rowheader">{E(name)}</span><span role="cell">{g.format(t=E(c["mx_words"][g[16:18]]))}</span>'
                 f'<span role="cell">{d.format(t=E(c["mx_words"][d[16:18]]))}</span></div>')
    cameras = f'''<section class="section" id="cameras" aria-labelledby="cameras-h" style="--h: 1"><div class="wrap">
    <div class="grid grid--top">
      <div class="span-6 rl-text">
        <h2 id="cameras-h">{E(c["cam_h"])}</h2>
        <p class="t-lead">{E(c["cam_lead"])}</p>
        <ul class="rl-camlist">{cams}</ul>
        <p class="t-small muted">{E(c["cam_note"])}</p>
      </div>
      <div class="rl-pic span-6 start-7"><img src="{rel}assets/board/shot-binding.webp" width="640" height="802" alt="{E(c["cfg_alts"][2])}" loading="lazy"></div>
    </div>
  </div></section>

  <section class="section" id="matrix" aria-labelledby="matrix-h" style="--h: 1; --hm: 2"><div class="wrap">
    <div class="grid grid--top">
      <div class="span-6 rl-text">
        <h2 id="matrix-h">{E(c["mx_h"])}</h2>
        <div class="rl-mx" role="table" aria-label="{E(c["mx_h"])}">
          <div class="rl-mx__row rl-mx__head" role="row"><span role="columnheader">{E(c["mx_cols"][0])}</span><span role="columnheader">{E(c["mx_cols"][1])}</span><span role="columnheader">{E(c["mx_cols"][2])}</span></div>
          {rows}
        </div>
        <p class="t-small muted">{E(c["mx_note"])}</p>
      </div>
      <div class="rl-pic span-6 start-7"><img src="{rel}assets/board/shot-status.webp" width="640" height="1083" alt="{E(c["status_alt"])}" loading="lazy"></div>
    </div>
  </div></section>'''

    tiles = ""
    for name, img, cls, badge, d, wire in c["brds"]:
        tiles += (f'<article class="tile rl-board"><div class="tile__media rl-board__media"><img src="{a}{ {"board-iso": "board-iso", "supermini": "hero-supermini", "s3zero": "hero-s3zero"}[img] }.webp" alt="{E(name)}" loading="lazy"></div>'
                  f'<div class="tile__head"><h3>{E(name)}</h3><span class="rl-badge rl-badge--{cls}">{E(badge)}</span></div><p>{E(d)}</p><p class="rl-wire">{E(wire)}</p></article>')
    needs = "".join(f'<li><span>{E(k)}</span><b>{E(v)}</b></li>' for k, v in c["needs"])
    boards = f'''<section class="section" id="boards" aria-labelledby="boards-h" style="--h: 1; --hm: 2"><div class="wrap">
    <div class="section-head"><h2 id="boards-h">{E(c["brd_h"])}</h2><p>{E(c["brd_lead"])}</p></div>
    <div class="rl-grid rl-boards">{tiles}</div>
    <ul class="rl-needs">{needs}</ul>
  </div></section>'''

    main = f'<main id="top">\n{hero}\n{safety}\n{connect}\n{osd}\n{features}\n{config}\n{cameras}\n{boards}\n</main>'
    foot = footer_html(c, c["close_h"], c["close_lead"], "../flash/", c["cta"], c["cols"], "../")
    body = f'<body>\n{nav_html(c, rel)}\n{main}\n{foot}\n'
    return head(lang, c["title"], c["desc"], seo, rel, rel + "assets/favicon.svg") + body + scripts(rel, f'<script src="{rel}assets/osd.js" defer></script>\n') + '</body>\n</html>\n'


# ----------------------------------------------------------------------------- the lineup picture (hero)
def make_lineup(src_dir, out):
    """The three boards side by side on a transparent ground, cropped to their drawing."""
    from PIL import Image
    files = ("board-iso.webp", "hero-supermini.webp", "hero-s3zero.webp")
    ims = []
    for f in files:
        im = Image.open(os.path.join(src_dir, f)).convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())
        ims.append(im)
    H = 640
    ims = [im.resize((round(im.width * H / im.height), H), Image.LANCZOS) for im in ims]
    gap = 90
    W = sum(i.width for i in ims) + gap * (len(ims) - 1)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 0
    for im in ims:
        canvas.paste(im, (x, 0), im)
        x += im.width + gap
    canvas.save(out, "WEBP", quality=88, method=6)
    return canvas.size


# ----------------------------------------------------------------------------- the FPVitt landing page
HOME = dict(
    title="FPVitt: FPV drone projects, firmware and guides",
    desc="Open-source firmware, hardware and guides for FPV pilots. The first project is RecLink, a camera link for Betaflight, GoPro and DJI.",
    h1="FPV drone projects and tools",
    lead="Open-source firmware, hardware and guides for FPV pilots. The first project is RecLink, a camera link for Betaflight.",
    cta="Install the firmware", cta2="See the RecLink project",
    facts=[("Projects", "One: RecLink"), ("Firmware", "0.2.1, pre-release"), ("Licence", "GPL-3.0"), ("Boards", "Three supported")],
    nav=[("Projects", "#projects"), ("Guides", "RecLink/en/"), ("Board", "RecLink/en/the-board.html"), ("Source", REPO)],
    hero_alt="The three boards RecLink runs on, the RecLink board, the ESP32-C3 SuperMini and the ESP32-S3-Zero, on a stone-coloured ground",
    proj_h="Projects",
    proj_name="RecLink", proj_sub="Camera link for Betaflight, GoPro and DJI",
    proj_lead="ESP32 firmware that starts recording on arm or a radio switch, draws camera status on your OSD and syncs the camera clock. It runs on a 0.68 g board or a common ESP32 dev board.",
    proj_links=[("RecLink/en/quick-start.html", "Read the quick start"), ("RecLink/en/the-board.html", "Explore the board in 3D"), (REPO, "Read the source on GitHub")],
    proj_alt="The RecLink board seen from above: an ESP32-C3, a ceramic antenna and four solder pads along one edge",
    stats=[("22", "OSD tokens"), ("4", "cameras paired at once"), ("6", "radio-switch zones, at most"), ("300", "ms to restart after a fault")],
    close_h="Put RecLink on your quad", close_lead="About fifteen minutes from the box to your first recording. Props off for the bench work.",
    foot_lede="Open-source FPV firmware, hardware and guides.",
    cols=[("RecLink", [("RecLink/en/quick-start.html", "Quick start"), ("RecLink/en/user-guide.html", "User guide"), ("RecLink/en/the-board.html", "The board"), ("RecLink/flash/", "Installer")]),
          ("Source", [("https://github.com/FPVitt", "FPVitt on GitHub"), (REPO, "RecLink code"), (REPO + "/releases", "Releases")]),
          ("Licence", [(REPO + "/blob/main/LICENSE", "GPL-3.0")])],
    legal=f"Firmware {FW} (pre-release) · free software, GPL-3.0",
    marks="GoPro, DJI, Betaflight and Espressif are trademarks of their owners.",
)


def make_hero(src_dir, out):
    """A wide still of the three boards on the page ground, calm on the left for the words."""
    from PIL import Image, ImageFilter
    W, H = 2400, 1500
    bg = (0xdf, 0xde, 0xdb)
    canvas = Image.new("RGB", (W, H), bg)
    spec = (("board-iso.webp", 1760, 480, 860), ("hero-supermini.webp", 1300, 1130, 500), ("hero-s3zero.webp", 2060, 1130, 440))
    for f, cx, cy, w in spec:
        im = Image.open(os.path.join(src_dir, f)).convert("RGBA")
        im = im.crop(im.getchannel("A").getbbox())
        h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        sh = Image.new("RGBA", (w + 160, h + 160), (0, 0, 0, 0))
        a = im.getchannel("A").point(lambda v: int(v * 0.22))
        sh.paste((38, 37, 30, 255), (80, 100), a)
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        canvas.paste(sh, (cx - w // 2 - 80, cy - h // 2 - 80), sh)
        canvas.paste(im, (cx - w // 2, cy - h // 2), im)
    canvas.save(out, "WEBP", quality=86, method=6)
    return canvas.size


def render_home(seo):
    h = HOME
    rel = "RecLink/"
    k = rel + "assets/kit/"
    words = "".join(f'<div class="nav__item"><a class="nav__link" href="{u}">{E(w)}</a></div>' for w, u in h["nav"])
    nav = f'''<header class="nav">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">Skip to content</a>
    <a class="nav__logo" href="#top">FPVitt</a>
    <nav class="nav__links" aria-label="Main">{words}</nav>
    <div class="nav__actions"><a class="btn btn--primary" href="RecLink/flash/">{E(h["cta"])}</a></div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
  </div>
</header>'''
    facts = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in h["facts"])
    hero = f'''<section class="hero hero--photo" data-enter data-calm="left" aria-labelledby="hero-h">
    <img class="hero__bg" src="{rel}assets/board/fpvitt-hero.webp" width="2400" height="1500" alt="{E(h["hero_alt"])}" style="--ly-pos: 70% 50%; --ly-pos-phone: 70% 50%" fetchpriority="high">
    <div class="wrap"><div class="hero-text">
      <div class="hero__text">
        <h1 id="hero-h">{E(h["h1"])}</h1>
        <p class="hero__lead">{E(h["lead"])}</p>
        <div class="btn-row"><a class="btn btn--primary" href="RecLink/flash/">{E(h["cta"])}{ARROW}</a><a class="btn btn--secondary" href="#projects">{E(h["cta2"])}</a></div>
      </div>
      <dl class="hero__facts">{facts}</dl>
    </div></div>
  </section>'''
    links = "".join(f'<li><a class="link" href="{u}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{E(t)}</a></li>' for u, t in h["proj_links"])
    stats = "".join(f'<div><p class="t-stat">{E(n)}</p><p class="t-small muted">{E(l)}</p></div>' for n, l in h["stats"])
    projects = f'''<section class="section" id="projects" aria-labelledby="projects-h" style="--h: 1; --hm: 2"><div class="wrap">
    <div class="grid grid--top">
      <div class="span-6 rl-text">
        <h2 id="projects-h">{E(h["proj_h"])}</h2>
        <h3 class="rl-projname">{LOGO}{E(h["proj_name"])}<span>{E(h["proj_sub"])}</span></h3>
        <p class="t-lead">{E(h["proj_lead"])}</p>
        <ul class="rl-links">{links}</ul>
      </div>
      <a class="rl-pic rl-pic--board span-6 start-7" href="RecLink/en/the-board.html"><img src="{rel}assets/board/board-top.webp" width="800" height="870" alt="{E(h["proj_alt"])}" loading="lazy"></a>
    </div>
    <div class="rl-figures" data-moment="counter-rolls">{stats}</div>
  </div></section>'''
    cols = [(t, [(u, l) for u, l in ls]) for t, ls in h["cols"]]
    foot = footer_html(h, h["close_h"], h["close_lead"], "RecLink/flash/", h["cta"], cols, "", brand="FPVitt")
    head_html = head("en", h["title"], h["desc"], seo, rel, rel + "assets/favicon.svg", note=("type: product (tech) · deal: hero photo, footer-dark, close-type, buttons solid, mark: wordmark;\n"
                     "     palette and type as the RecLink pages · moment: counter-rolls (the figures row)"))
    body = f'<body>\n{nav}\n<main id="top">\n{hero}\n{projects}\n</main>\n{foot}\n'
    return head_html + body + scripts(rel, "") + "</body>\n</html>\n"
