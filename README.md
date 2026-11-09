# BlackVans Transfer – landing page

Landing page statica (HTML/CSS/JS, nessuna build) per BlackVans Transfer, NCC a Roma. Italiano e inglese.

## Link per accedere

**https://demolandingpage.github.io/andrei-ncc-landing/**

> **Bozza 6** – anteprima da sottoporre al cliente: i dati del titolare sono fittizi (vedi sotto).
> Se il link non risponde: Settings → Pages → Source "Deploy from a branch", branch `main`, cartella `/ (root)`. Dopo il salvataggio servono 1–2 minuti.

## Contenuto

- `index.html` – pagina completa
- `img/` – foto ottimizzate (WebP)
- `fonts/` – font ospitati sul sito (nessuna richiesta a terzi, nessun banner cookie necessario)

Anteprima locale: `python -m http.server` nella cartella, poi apri http://localhost:8000

## Note

- **Lingue:** italiano/inglese con selettore in alto; la scelta viene ricordata nel browser e, alla prima visita, segue la lingua del browser.
- **Form di prenotazione:** invia la richiesta per email tramite FormSubmit (formsubmit.co) a andreiprivatetransfers@gmail.com e manda una conferma automatica al cliente; poi si può continuare su WhatsApp. Se l'invio fallisce si apre WhatsApp con il messaggio pronto. **Alla prima richiesta reale FormSubmit manda un'email di attivazione a quell'indirizzo: va cliccato il link.** Il sito non salva i dati.
- **Cookie/analytics:** nessuno. Nessun embed o script di terze parti, per questo non serve il banner cookie. Se in futuro si aggiungono Google Analytics, Maps o simili, va aggiunto un banner di consenso e aggiornata la privacy policy.
- **Recensioni:** nessuna recensione finta. Aggiungerne solo di reali.
- **Foto:** `van1`–`van6` e `hero` sono quelle del progetto originale. Le foto del nuovo Vito 2026 blu non sono ancora incluse.

## Quando arrivano i dati del titolare

1. Raccogliere i dati con la lista in [CHECKLIST-DATI.md](CHECKLIST-DATI.md).
2. Compilare `dati-titolare.json` (nome, indirizzo, P.IVA, REA, autorizzazione NCC, PEC, dominio, link Google Business Profile e social).
3. Eseguire una sola volta `python applica_dati.py`: aggiorna footer, privacy, versione inglese, dati strutturati, canonical, Open Graph, `robots.txt` e `sitemap.xml`, toglie l'etichetta «Bozza» e controlla che non resti nessun dato fittizio. Con `"indicizzabile": false` mette il `noindex`.
4. Controllare la pagina, pubblicare, registrare il sito su Search Console e inviare la sitemap.

## Da sostituire prima della pubblicazione definitiva

- I dati del titolare sono **fittizi**: Mario Rossi, Via Esempio 1, 00100 Roma, P.IVA 12345678901, REA RM-1234567, autorizzazione NCC n. 0000, PEC mario.rossi@pec.example.it. Compaiono nel footer e nella sezione Privacy.
- Telefono ed email sono quelli reali del cliente.
- La privacy policy è una bozza generica: da far verificare.
- **SEO:** la pagina è indicizzabile (nessun `noindex`). I dati fittizi non devono restare online sotto un indirizzo indicizzato: sostituirli prima di chiedere l'indicizzazione.

## SEO

Già presenti: title e description con parole chiave, H1/H2/H3 strutturati, canonical, Open Graph e Twitter Card, dati strutturati JSON-LD (TaxiService/LocalBusiness con tariffe, orari, zona servita, FAQPage), `robots.txt`, `sitemap.xml`, alt su tutte le immagini, font e immagini ottimizzati.

Da fare alla messa online sul dominio definitivo:
1. Sostituire l'URL `https://demolandingpage.github.io/andrei-ncc-landing/` con il dominio reale in `index.html` (canonical, og:url, og:image, JSON-LD), `robots.txt` e `sitemap.xml`.
2. Registrare il sito su Google Search Console e inviare la sitemap.
3. Creare e verificare la scheda Google Business Profile (indirizzo reale, orari, foto, recensioni vere): è il fattore principale per le ricerche "NCC Roma".
4. Inserire indirizzo, P.IVA e telefono reali (devono coincidere con la scheda Google).
