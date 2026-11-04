#!/usr/bin/env python3
"""Sostituisce i dati fittizi con quelli reali del titolare.

Uso:  1) compila dati-titolare.json   2) python applica_dati.py
Aggiorna index.html (footer, privacy, versione EN, JSON-LD, canonical, Open Graph),
robots.txt e sitemap.xml. Va eseguito UNA volta, partendo dalla versione fittizia.
Alla fine controlla che non resti nessun dato di esempio.
"""
import json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(D, "dati-titolare.json"), encoding="utf-8"))

# valori fittizi attualmente presenti nei file
FAKE = dict(nome="Mario Rossi", forma_it="ditta individuale", forma_en="sole proprietorship",
            indirizzo="Via Esempio 1", cap="00100", citta_it="Roma (RM)", citta_en="Rome (RM)",
            partita_iva="12345678901", rea="RM-1234567", aut="0000", ente="Roma Capitale",
            pec="mario.rossi@pec.example.it", dominio="https://demolandingpage.github.io/andrei-ncc-landing/")

def need(k):
    v = (cfg.get(k) or "").strip()
    if not v:
        sys.exit(f"Manca il campo obbligatorio: {k}")
    return v

nome, forma_it, forma_en = need("nome"), need("forma_it"), need("forma_en")
indirizzo, cap = need("indirizzo"), need("cap")
citta_it, citta_en = need("citta_it"), need("citta_en")
piva, pec = need("partita_iva"), need("pec")
aut, ente = need("autorizzazione_numero"), need("autorizzazione_ente")
dominio = need("dominio").rstrip("/") + "/"
rea = (cfg.get("rea") or "").strip()
cf = (cfg.get("codice_fiscale") or "").strip()
if not re.fullmatch(r"\d{11}", piva):
    sys.exit("La partita IVA deve avere 11 cifre")
if not re.fullmatch(r"\d{5}", cap):
    sys.exit("Il CAP deve avere 5 cifre")
if not dominio.startswith("https://"):
    sys.exit("Il dominio deve iniziare con https://")

p = os.path.join(D, "index.html")
s = open(p, encoding="utf-8").read()
if FAKE["nome"] not in s:
    sys.exit("In index.html non ci sono più i dati fittizi: i dati sono già stati applicati?")

# 1) JSON-LD: arricchisco con i dati reali (prima delle sostituzioni testuali)
m = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', s, re.S)
ld = json.loads(m.group(2))
biz = next(x for x in ld["@graph"] if isinstance(x.get("@type"), list))
biz["legalName"] = nome
biz["vatID"] = "IT" + piva
if cf:
    biz["taxID"] = cf
biz["address"] = {"@type": "PostalAddress", "streetAddress": indirizzo, "postalCode": cap,
                  "addressLocality": "Roma", "addressRegion": "RM", "addressCountry": "IT"}
same = [cfg[k].strip() for k in ("google_business_profile", "instagram", "facebook") if (cfg.get(k) or "").strip()]
if same:
    biz["sameAs"] = same
if (cfg.get("google_maps") or "").strip():
    biz["hasMap"] = cfg["google_maps"].strip()
s = s[:m.start(2)] + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + s[m.end(2):]

# 2) sostituzioni testuali (footer, privacy, versione EN: chiave e traduzione restano coerenti)
def sub(a, b):
    global s
    s = s.replace(a, b)
sub(FAKE["pec"], pec)
sub(FAKE["nome"], nome)
sub(FAKE["forma_it"], forma_it)
sub(FAKE["forma_en"], forma_en)
sub(FAKE["indirizzo"], indirizzo)
sub(FAKE["cap"] + " " + FAKE["citta_it"], cap + " " + citta_it)
sub(FAKE["cap"] + " " + FAKE["citta_en"], cap + " " + citta_en)
sub(FAKE["partita_iva"], piva)
if rea:
    sub(FAKE["rea"], rea)
else:
    sub(" · REA " + FAKE["rea"], "")
sub("n. " + FAKE["aut"], "n. " + aut)
sub("no. " + FAKE["aut"], "no. " + aut)
sub(FAKE["ente"], ente)

# 3) dominio, indicizzazione, rimozione etichetta "Bozza"
s = re.sub(r"<!--DRAFT-->.*?<!--/DRAFT-->\s*", "", s, flags=re.S)
sub(FAKE["dominio"], dominio)
if not cfg.get("indicizzabile", True):
    s = s.replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                  '<meta name="robots" content="noindex, nofollow">')
open(p, "w", encoding="utf-8", newline="\n").write(s)

for f in ("robots.txt", "sitemap.xml"):
    fp = os.path.join(D, f)
    t = open(fp, encoding="utf-8").read().replace(FAKE["dominio"], dominio)
    open(fp, "w", encoding="utf-8", newline="\n").write(t)

# 4) controllo finale: nessun residuo fittizio (salvo che i nuovi valori coincidano)
resto = []
for f in ("index.html", "robots.txt", "sitemap.xml"):
    t = open(os.path.join(D, f), encoding="utf-8").read()
    for k in ("Mario Rossi", "Via Esempio", "12345678901", "RM-1234567", "pec.example.it", "n. 0000", "no. 0000"):
        if k in t and k not in (nome, indirizzo, piva, rea, pec, aut):
            resto.append((f, k))
    if "demolandingpage.github.io" in t and "demolandingpage" not in dominio:
        resto.append((f, "dominio di prova"))
if resto:
    print("ATTENZIONE, residui da controllare:", resto)
else:
    print("Fatto: dati reali applicati, nessun residuo fittizio.")
print("Restano da fare a mano: verifica della privacy policy con un consulente; foto e prezzi definitivi.")
