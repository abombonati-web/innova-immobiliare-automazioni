# Ordine di sviluppo

Le cinque fasi che hai indicato, con dentro quello che è già fatto e quello che manca.
Ogni fase produce qualcosa di usabile da sola: se ci si ferma dopo la seconda, si ha già
un sistema che porta appuntamenti veri in agenda.

---

## Fase 1 — La landing con il modulo

**Fatto nel prototipo.** Landing generata dal file dell'immobile, carta d'identità completa,
descrizione, galleria, video, due percorsi di esperienza, gate del club, provvigioni in
chiaro, tre passaggi dell'acquisto o percorso affitto, ventaglio servizi.

Per andare in produzione manca:

- [ ] Contenuto esatto del modulo online (vedi `05-modulo-campi.md`) — **punto aperto**
- [ ] API che serve gli immobili dal gestionale, restituendo solo il nodo pubblico
- [ ] URL Vrexx per immobile
- [ ] Due video istituzionali collegati
- [ ] Dominio e pagina informativa privacy aggiornata con la profilazione del semaforo

## Fase 2 — Il motore del semaforo con il calendario

**Prototipato.** Regole configurabili, tre esiti, revisione umana sempre disponibile,
generazione slot che esclude gli orari occupati, evento calendario e file .ics.

Manca:

- [ ] **Spostare la valutazione lato server** (non rimandabile: nel browser è aggirabile)
- [ ] Chiave Google Calendar: FreeBusy in lettura, Events.insert in scrittura
- [ ] Pagina per il consulente finanziario dove registrare l'esito di un giallo
- [ ] Notifica al consulente con SLA di 4 ore e sollecito a 24

Alla fine di questa fase il sistema è già utile: porta in agenda solo clienti verdi
e manda gli altri al consulente.

## Fase 3 — Le automazioni di follow-up

**Configurato.** Tutte le sequenze sono scritte e il piano di invio viene calcolato con
canale e orario esatto, rispettando fascia oraria, giorni e tetto di un messaggio al giorno.

Manca:

- [ ] Provider WhatsApp Business e **approvazione dei modelli da parte di Meta** — è il
      passaggio più lento, va avviato all'inizio della fase 2, non qui
- [ ] Servizio email transazionale con dominio verificato (SPF, DKIM, DMARC)
- [ ] Coda di invio con ritenta, e registro di cosa è partito verso chi
- [ ] Interruzione automatica su risposta del cliente (aggancio al webhook in ingresso)
- [ ] Disiscrizione: STOP su WhatsApp, link nelle email

## Fase 4 — Le pipeline differenziate

Manca quasi tutto, ma la logica c'è già:

- [ ] Landing venditore dedicata, con modulo snello e valutazione immediata
- [ ] Percorso investitore: rendimento lordo e netto, frazionamento, affitti brevi
- [ ] Percorso affittuario completo con caricamento documenti
- [ ] Etichetta e gestione riservata dei contatti in difficoltà economica
- [ ] Assegnazione automatica dell'agente per zona e tipologia

## Fase 5 — Il cruscotto di monitoraggio

Il tracciamento raccoglie già gli eventi; manca il posto dove guardarli.

- [ ] Endpoint in Innova Experience che riceve la coda di eventi
- [ ] Vista contatto: che cosa ha guardato, per quanto, dove si è fermato
- [ ] Vista immobile: quante aperture, quanti moduli, quanti verdi, quante visite
- [ ] Imbuto: da apertura a prenotazione, con il punto esatto di dispersione
- [ ] Comandi: sospendere una sequenza, forzare un esito, riassegnare un contatto

---

## Due cose da anticipare

**I modelli WhatsApp.** L'approvazione Meta richiede giorni e senza modelli approvati
metà delle automazioni non parte. Va avviata durante la fase 2.

**Il modulo online.** È l'unico punto aperto del progetto e blocca la chiusura della fase 1.
Bastano cinque minuti per risolverlo: vedi `05-modulo-campi.md`.

## Come si prova adesso

```bash
cd progetto-landing-ai
python3 -m http.server 8080      # poi apri http://localhost:8080/demo/
node --test "test/*.test.js"     # 51 test sui motori
```
