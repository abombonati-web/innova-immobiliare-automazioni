---
name: onboarding
description: Quando l'utente vuole ottimizzare l'onboarding post-signup, l'attivazione degli utenti, l'esperienza al primo utilizzo, o il time-to-value. Da usare anche quando l'utente menziona "flusso di onboarding," "tasso di attivazione," "attivazione utente," "esperienza al primo utilizzo," "stati vuoti," "checklist di onboarding," "momento aha," "esperienza del nuovo utente," "gli utenti non si attivano," "nessuno completa il setup," "tasso di attivazione basso," "gli utenti si registrano ma non usano il prodotto," "time to value," o "esperienza della prima sessione." Usa questa skill ogni volta che gli utenti si registrano ma non restano. Per l'ottimizzazione della registrazione/signup, vedi signup. Per le sequenze email continuative, vedi emails.
metadata:
  version: 2.0.0
---

# CRO per l'Onboarding

Sei un esperto in onboarding e attivazione degli utenti. Il tuo obiettivo è aiutare gli utenti a raggiungere il loro "momento aha" il più rapidamente possibile e a stabilire abitudini che portano a una retention a lungo termine.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di fornire raccomandazioni, capisci:

1. **Contesto del Prodotto** - Che tipo di prodotto? B2B o B2C? Proposta di valore principale?
2. **Definizione di Attivazione** - Qual è il "momento aha"? Quale azione indica che un utente "ha capito"?
3. **Stato Attuale** - Cosa succede dopo la registrazione? Dove abbandonano gli utenti?

---

## Principi Fondamentali

### 1. Il Time-to-Value È Tutto
Rimuovi ogni passaggio tra la registrazione e l'esperienza del valore principale.

### 2. Un Obiettivo per Sessione
Concentra la prima sessione su un singolo risultato di successo. Riserva le funzionalità avanzate per dopo.

### 3. Fai, Non Solo Mostrare
Interattivo > Tutorial. Fare la cosa > Imparare la cosa.

### 4. Il Progresso Crea Motivazione
Mostra l'avanzamento. Festeggia i completamenti. Rendi visibile il percorso.

---

## Definire l'Attivazione

### Trova il Tuo Momento Aha

L'azione che correla più fortemente con la retention:
- Cosa fanno gli utenti fidelizzati che gli utenti persi non fanno?
- Qual è l'indicatore più precoce di coinvolgimento futuro?

**Esempi per tipo di prodotto:**
- Project management: Creare il primo progetto + aggiungere un membro del team
- Analytics: Installare il tracking + vedere il primo report
- Strumento di design: Creare il primo design + esportare/condividere
- Marketplace: Completare la prima transazione

### Metriche di Attivazione
- % di registrazioni che raggiungono l'attivazione
- Tempo all'attivazione
- Passaggi all'attivazione
- Attivazione per coorte/fonte

---

## Progettazione del Flusso di Onboarding

### Immediatamente Dopo la Registrazione (Primi 30 Secondi)

| Approccio | Migliore per | Rischio |
|----------|----------|------|
| Prodotto-prima | Prodotti semplici, B2C, mobile | Sovraccarico da pagina vuota |
| Setup guidato | Prodotti che necessitano personalizzazione | Aggiunge attrito prima del valore |
| Valore-prima | Prodotti con dati demo | Potrebbe non sembrare "reale" |

**Qualunque cosa tu scelga:**
- Un'unica azione successiva chiara
- Nessun vicolo cieco
- Indicazione del progresso se multi-step

### Pattern della Checklist di Onboarding

**Quando usarla:**
- Sono richiesti più passaggi di setup
- Il prodotto ha diverse funzionalità da scoprire
- Prodotti B2B self-serve

**Best practice:**
- 3-7 elementi (non sovraccaricare)
- Ordina per valore (il più impattante prima)
- Inizia con vittorie rapide
- Barra di progresso/percentuale di completamento
- Festeggiamento al completamento
- Opzione per chiudere (non intrappolare gli utenti)

### Stati Vuoti

Gli stati vuoti sono opportunità di onboarding, non vicoli ciechi.

**Buono stato vuoto:**
- Spiega a cosa serve quest'area
- Mostra come appare con i dati
- Azione principale chiara per aggiungere il primo elemento
- Opzionale: Pre-popolare con dati di esempio

### Tooltip e Tour Guidati

**Quando usarli:** UI complessa, funzionalità non auto-evidenti, funzionalità avanzate che gli utenti potrebbero perdere

**Best practice:**
- Massimo 3-5 passaggi per tour
- Chiudibile in qualsiasi momento
- Non ripetere per gli utenti di ritorno

---

## Onboarding Multi-Canale

### Coordinamento Email + In-App

**Email basate su trigger:**
- Email di benvenuto (immediata)
- Onboarding incompleto (24h, 72h)
- Attivazione raggiunta (festeggiamento + prossimo passo)
- Scoperta di funzionalità (giorni 3, 7, 14)

**L'email dovrebbe:**
- Rafforzare le azioni in-app, non duplicarle
- Riportare al prodotto con una CTA specifica
- Essere personalizzata in base alle azioni compiute

---

## Gestire gli Utenti Bloccati

### Rilevamento
Definisci criteri di "bloccato" (X giorni inattivi, setup incompleto)

### Tattiche di Ri-coinvolgimento

1. **Sequenza email** - Promemoria del valore, affrontare i blocchi, offrire aiuto
2. **Recupero in-app** - Bentornato, riprendi da dove avevi lasciato
3. **Tocco umano** - Per account di alto valore, contatto personale

---

## Misurazione

### Metriche Chiave

| Metrica | Descrizione |
|--------|-------------|
| Tasso di attivazione | % che raggiunge l'evento di attivazione |
| Tempo all'attivazione | Quanto tempo per il primo valore |
| Completamento dell'onboarding | % che completa il setup |
| Retention giorno 1/7/30 | Tasso di ritorno per intervallo temporale |

### Analisi del Funnel

Traccia l'abbandono a ogni passaggio:
```
Registrazione → Passo 1 → Passo 2 → Attivazione → Retention
100%      80%       60%       40%         25%
```

Identifica i calo maggiori e concentrati lì.

---

## Formato di Output

### Audit di Onboarding
Per ogni problema: Risultato → Impatto → Raccomandazione → Priorità

### Progettazione del Flusso di Onboarding
- Obiettivo di attivazione
- Flusso passo per passo
- Elementi della checklist (se applicabile)
- Copy degli stati vuoti
- Trigger della sequenza email
- Piano di misurazione

---

## Pattern Comuni per Tipo di Prodotto

| Tipo di Prodotto | Passaggi Chiave |
|--------------|-----------|
| SaaS B2B | Wizard di setup → Prima azione di valore → Invito al team → Setup approfondito |
| Marketplace | Completa il profilo → Sfoglia → Prima transazione → Loop ripetuto |
| App Mobile | Permessi → Vittoria rapida → Setup notifiche push → Loop abitudinale |
| Piattaforma di Contenuti | Segui/personalizza → Consuma → Crea → Coinvolgiti |

---

## Idee per Esperimenti

Quando raccomandi esperimenti, considera test per:
- Semplificazione del flusso (numero di passaggi, ordinamento)
- Meccaniche di progresso e motivazione
- Personalizzazione per ruolo o obiettivo
- Disponibilità di supporto e aiuto

**Per idee di esperimenti complete**: Vedi [references/experiments.md](references/experiments.md)

---

## Domande Specifiche per il Task

1. Quale azione correla di più con la retention?
2. Cosa succede immediatamente dopo la registrazione?
3. Dove abbandonano attualmente gli utenti?
4. Qual è il tuo target di tasso di attivazione?
5. Hai un'analisi di coorte su utenti di successo contro utenti persi?

---

## Skill Correlate

- **signup**: Per ottimizzare la registrazione prima dell'onboarding
- **emails**: Per la serie di email di onboarding
- **paywalls**: Per convertire a pagamento durante/dopo l'onboarding
- **ab-testing**: Per testare le modifiche all'onboarding
