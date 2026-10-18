# Agente AI personale per il team — Piattaforma Innova Experience

> Versione 1 · 18/10/2026 · Autore: Claude (Direttore Generale AI) su richiesta di Andrea Bombonati
> Piattaforma di destinazione: `innovaexperience.it/admin` (progetto `project-kruz` — SvelteKit + Supabase + Vercel)

---

## 1. Obiettivo

Ogni membro del team, dentro la piattaforma, ha **il proprio agente Claude**:

- **personale** — ha un nome, un tono e istruzioni che il membro può modificare;
- **per ruolo** — sa cosa serve a un broker, a un listing agent, al front office, al tecnico, al marketing;
- **operativo** — non solo risponde: legge e **inserisce/aggiorna dati** nella piattaforma (immobili, contatti, agenda, follow up, open house, valutazioni, moduli…);
- **completo come Claude** — analisi documenti (PDF, foto, planimetrie), ricerca web, scrittura di annunci/script/post, ragionamento strategico, memoria delle preferenze.

**Risultato atteso:** meno tempo su inserimenti e ricerche, nessun lead dimenticato, procedure Innova (Protocollo, lancio 14 giorni, Experience) eseguite sempre allo stesso modo.

---

## 2. Decisioni di architettura (e perché)

| # | Decisione | Motivo |
|---|---|---|
| D1 | L'agente gira **solo lato server** (SvelteKit `+server.ts`), la chiave Anthropic sta nelle variabili d'ambiente Vercel | La chiave API non deve mai arrivare al browser |
| D2 | Ogni strumento dell'agente esegue le query **con la sessione Supabase dell'utente** (RLS attiva), mai con la service-role key | L'agente non può mai fare più di quanto può fare il membro stesso: i permessi sono quelli già esistenti nella piattaforma |
| D3 | **Le scritture richiedono conferma** dell'utente (card «Conferma / Annulla») | Zero inserimenti sbagliati non visti; l'utente resta responsabile del dato |
| D4 | **Nessuna cancellazione** in v1 | Rischio non giustificato dal beneficio |
| D5 | Un **unico registro di strumenti** (tool registry) con permessi per ruolo | Un solo punto da mantenere; lo stesso registro può essere esposto in futuro come server MCP (vedi §10) |
| D6 | Modello `claude-opus-5-5`, thinking adattivo, effort `medium` per la chat (`high` per analisi documenti e valutazioni), streaming, prompt caching, fallback lato server | Qualità massima, costi contenuti dal caching del contesto Innova |
| D7 | Log di ogni azione (`agent_audit_log`) | Tracciabilità, GDPR, controllo dei broker |

> ⚠ Franchezza: «tutto ciò che fa Claude oggi» **non si trasferisce da solo**. Le funzioni del modello (ragionamento, scrittura, analisi PDF/immagini, ricerca web) sì. I connettori che usi su claude.ai (Gmail, Drive, Calendar, Canva, Windsor) vanno **ricostruiti uno per uno** come strumenti della piattaforma. Per questo il piano è a fasi (§9): prima la piattaforma, poi Google, poi il resto.

---

## 3. Flusso di una richiesta

```
Browser (pannello chat)                Server SvelteKit                       Anthropic API
───────────────────────               ─────────────────────                  ─────────────
messaggio + allegati ──POST /api/agent/chat──▶ 1. verifica sessione Supabase
                                                2. carica profilo agente + ruolo
                                                3. compone system prompt (cache)
                                                4. filtra strumenti per ruolo
                                                5. tool runner (stream) ─────────▶ claude-opus-5-5
                                                   ◀──── tool_use ──────────────
                                                6. esegue strumento con RLS utente
                                                   · lettura → risultato diretto
                                                   · scrittura → proposta, attende conferma
◀──── stream SSE (testo, card azione) ─────────  7. salva messaggi + audit log
click «Conferma» ──POST /api/agent/confirm──▶   8. esegue la scrittura, riprende il loop
```

---

## 4. Ruoli e permessi

Ruoli derivati dall'organigramma 2026. La colonna «Moduli» usa le voci reali del menu admin.

| Ruolo | Membri attuali | Moduli in lettura | Moduli in scrittura (con conferma) | Focus dell'agente |
|---|---|---|---|---|
| `broker` (admin) | Andrea Bombonati, Paolo Maltese | Tutti | Tutti tranne Utenti e Accessi Agenti IA | Strategia, KPI e funnel, pricing, controllo team, trattative |
| `listing_agent` | Angelo Sicilia | Immobili, Match, Open House, Lista Incarichi, Notizie, Agenda, Contatti, Valutazioni, Follow Up, Documenti immobile | Immobili (propri), Contatti, Agenda, Follow Up, Notizie, Valutazioni, Open House | Acquisizione, script e obiezioni, CMA, report venditore, procedura lancio 14 gg |
| `tecnico` | Marco Livigni, Benito La Barbera | Immobili, Documenti immobile, Valutazioni, Agenda | Documenti immobile, note tecniche immobile, Agenda | Lettura visure/APE/planimetrie/conformità, checklist documentale, computi |
| `front_office` | Chiara Lo Cascio | Contatti, Agenda, Moduli, Follow Up, Open House, Immobili | Contatti, Importa contatti, Agenda, Follow Up, stato lead | Lead entro SLA, stati lead Innova, appuntamenti, conferme e promemoria |
| `marketing` | Fotografo/videomaker, Innovation Manager | Immobili, Open House, Notizie, Dashboard | Testi annuncio, Notizie, Open House (contenuti) | Annunci emozionali, piani social, landing Experience, reel e caption |

Regole:
- Il permesso effettivo è sempre **ruolo ∩ RLS Supabase** (D2): se la piattaforma non permette un'azione all'utente, l'agente non la può fare.
- Solo i `broker` modificano i template di ruolo; ogni membro modifica **solo il proprio** profilo agente.

---

## 5. Personalizzazione (tre livelli)

Il system prompt è composto, in quest'ordine (stabile → variabile, per massimizzare la cache):

1. **Base Innova** (uguale per tutti, in cache 1h) — identità aziendale, Metodo Innova con i soli numeri verificati, Protocollo 10 servizi, Innova Experience e stati lead, partner, brand e tono, zone, regole non negoziabili (zero invenzioni, no dati OMI, GDPR, rimando al professionista su questioni legali). Fonte: Istruzioni Master v3 + `Procedure_Innova_acquisizione_e_rilancio.md`.
2. **Template di ruolo** (per ruolo, in cache) — compiti, procedure, formati di output, cosa può/non può fare.
3. **Profilo personale** (per membro) — nome dell'agente (es. «Leo» per Angelo), tono (formale/diretto/sintetico), istruzioni libere, firma email/WhatsApp, zone seguite, obiettivi del mese.
4. **Memorie** — appunti che l'agente salva su richiesta («ricorda che preferisco i report il venerdì»), visibili e cancellabili dall'utente in Impostazioni.
5. **Contesto della pagina** (dinamico, dopo l'ultimo breakpoint di cache) — se l'utente apre la chat dalla scheda di un immobile o contatto, l'agente riceve l'ID e sa di cosa si parla.

---

## 6. Strumenti dell'agente (catalogo v1)

Nomi indicativi: in implementazione vanno legati alle **tabelle reali** di Supabase (vedi PROMPT_CLAUDE_CODE.md, step 1). Nessuno strumento cancella dati.

**Lettura (esecuzione immediata)**
- `cerca_immobili` — filtri: zona, tipologia, prezzo, stato incarico, agente
- `dettaglio_immobile` — scheda completa + documenti + open house collegati
- `cerca_contatti` / `dettaglio_contatto` — con storico interazioni e follow up
- `trova_match` — acquirenti compatibili per un immobile (usa la logica «Match» già esistente)
- `agenda` — appuntamenti in un intervallo, per utente
- `follow_up_in_scadenza` — oggi / settimana
- `risposte_moduli` — lead da Moduli Experience/Locazione/Feedback con filtri
- `kpi_funnel` — contatti → appuntamenti → incarichi → visite → proposte → vendite nel periodo
- `leggi_documento_immobile` — passa il file (PDF/immagine) al modello come blocco `document`/`image`
- `guida_piattaforma` — risponde a «come si fa X in piattaforma» da una pagina di aiuto mantenuta in `agent_knowledge`

**Scrittura (proposta → conferma utente → esecuzione)**
- `crea_contatto` / `aggiorna_contatto` (incluso stato lead: APPUNTAMENTO FISSATO / DA FISSARE / CONTATTO GIRATO AL REFERENTE / HANNO TROVATO)
- `crea_appuntamento` / `sposta_appuntamento`
- `crea_follow_up` / `chiudi_follow_up`
- `crea_immobile_bozza` / `aggiorna_immobile` (testi, prezzo, caratteristiche — mai pubblicazione automatica sui portali in v1)
- `crea_open_house` / `aggiorna_open_house`
- `salva_valutazione`
- `crea_notizia`
- `salva_memoria` / `elimina_memoria` (solo sulle memorie dell'utente)

**Strumenti server Anthropic**
- `web_search` / `web_fetch` (versione `_20260209`) — ricerca mercato, normativa, portali. Con dominio `allowed_domains` opzionale per ruolo.

---

## 7. Modello dati (nuove tabelle Supabase)

SQL di partenza in `PROMPT_CLAUDE_CODE.md`. Tutte con RLS.

| Tabella | Contenuto | Chi vede/modifica |
|---|---|---|
| `agent_role_templates` | ruolo, prompt di ruolo, strumenti abilitati, effort | lettura tutti; scrittura broker |
| `agent_profiles` | user_id, ruolo, nome agente, tono, istruzioni personali, firma, attivo | il proprio utente; broker in lettura |
| `agent_memories` | user_id, testo, data | solo il proprio utente |
| `agent_conversations` | user_id, titolo, contesto pagina, data | solo il proprio utente |
| `agent_messages` | conversation_id, ruolo, contenuto JSON (blocchi Anthropic completi) | solo il proprio utente |
| `agent_pending_actions` | azione proposta, input, stato (in attesa/confermata/annullata/scaduta) | solo il proprio utente |
| `agent_audit_log` | user_id, strumento, input, esito, timestamp | inserimento server; lettura broker |
| `agent_knowledge` | sezioni della base Innova e guida piattaforma, versione | lettura tutti; scrittura broker |

Conservazione: conversazioni 12 mesi (coerente con l'informativa Innova per richieste informative), poi cancellazione automatica; audit log 24 mesi — **da confermare con Andrea**.

---

## 8. Interfaccia

- **Pulsante flottante** in tutte le pagine admin → pannello laterale chat (Poppins, palette Innova: ambra `#E8982A`, antracite `#2B2A28`, crema `#FBF6EE`).
- **Contesto automatico**: aperto da un immobile/contatto, il pannello mostra «Stai parlando di: PM-274 Sanfilippo».
- **Card azione** per ogni scrittura: riepilogo campi → «Conferma» / «Modifica» / «Annulla».
- **Allegati**: trascina PDF/foto (visure, APE, planimetrie, atti) direttamente in chat.
- **Azioni rapide per ruolo** (chip sopra l'input): es. listing agent «Prepara report venditore», front office «Lead di oggi da richiamare», broker «Funnel della settimana».
- **Impostazioni → Il mio agente**: nome, tono, istruzioni, memorie, storico conversazioni.
- **Utenti → Agenti IA** (solo broker): template di ruolo, consumo per utente, audit log.

---

## 9. Piano di rilascio

| Fase | Contenuto | Criterio di uscita |
|---|---|---|
| **1 — MVP lettura** (sett. 1) | Pannello chat, profili e template, base Innova in cache, strumenti di sola lettura, analisi documenti, web search, audit log | Andrea e Paolo lo usano 5 giorni senza errori sui dati |
| **2 — Scritture con conferma** (sett. 2-3) | Tutti gli strumenti di scrittura §6, card di conferma, contesto pagina, azioni rapide | Chiara e Angelo inseriscono contatti/appuntamenti/follow up dall'agente |
| **3 — Google Workspace** (sett. 4-5) | Gmail (bozze, mai invio senza conferma), Calendar, Drive (cartelle immobili), con OAuth per utente | Report venditore → bozza email in 1 messaggio |
| **4 — Estensioni** | Canva, Windsor.ai (KPI ads), export onOffice, server MCP della piattaforma (§10) | Su richiesta |

---

## 10. Opzione da valutare: piattaforma come server MCP

Lo stesso registro strumenti (D5) può essere esposto come **server MCP remoto** con login per utente. Così ogni membro, oltre alla chat interna, può usare la piattaforma da Claude (app desktop/mobile, Claude Code) con **tutte** le funzioni di Claude e i connettori già attivi. La voce di menu «Accessi Agenti IA» suggerisce che una parte di questo esista già: va verificato nel codice prima di costruire.

---

## 11. Sicurezza e GDPR

- Chiave API solo in env server; rate limit per utente (es. 60 messaggi/ora) e tetto di spesa mensile per utente.
- RLS su tutte le tabelle; strumenti con sessione utente (D2).
- I dati personali dei lead passano ad Anthropic per l'elaborazione: **aggiornare l'informativa privacy** includendo il fornitore AI tra i destinatari/responsabili — da verificare con il consulente privacy.
- Contenuti di documenti e pagine web sono trattati come dati, non come istruzioni (difesa da prompt injection nel system prompt di base).
- Nessuna azione verso l'esterno (email, pubblicazione portali, social) senza conferma esplicita.

---

## 12. KPI dell'agente (pannello broker)

- Utenti attivi/settimana · messaggi per utente · azioni confermate vs annullate
- Tempo medio di risposta ai lead (prima/dopo)
- Follow up scaduti (prima/dopo)
- Costo API per utente/mese

---

## 13. Da confermare con Andrea

1. Accesso al repository `project-kruz` (per implementare direttamente — vedi README).
2. Chi ricopre oggi il ruolo «Innovation Manager» e il fotografo: hanno un account in piattaforma?
3. Il listing agent può modificare solo i **propri** immobili o tutti?
4. Durata di conservazione conversazioni/audit (§7).
5. Budget mensile API per utente.
