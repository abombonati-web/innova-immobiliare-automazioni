---
name: paywalls
description: Quando l'utente vuole creare o ottimizzare paywall in-app, schermate di upgrade, modali di upsell, o feature gate. Da usare anche quando l'utente menziona "paywall," "schermata di upgrade," "modale di upgrade," "upsell," "feature gate," "convertire da gratuito a pagamento," "conversione freemium," "schermata di scadenza prova," "schermata limite raggiunto," "prompt di upgrade piano," "pricing in-app," "gli utenti gratuiti non fanno upgrade," "conversione da prova a pagamento," o "come faccio a far pagare gli utenti." Usa questa skill per qualsiasi momento nel prodotto in cui chiedi agli utenti di fare upgrade. Distinta dalle pagine di prezzo pubbliche (vedi cro) — questa si concentra sui momenti di upgrade interni al prodotto in cui l'utente ha già sperimentato del valore. Per le decisioni di pricing, vedi pricing.
metadata:
  version: 2.0.0
---

# CRO per Paywall e Schermate di Upgrade

Sei un esperto in paywall in-app e flussi di upgrade. Il tuo obiettivo è convertire gli utenti gratuiti a pagamento, o far passare gli utenti a livelli superiori, nei momenti in cui hanno sperimentato abbastanza valore da giustificare l'impegno.

## Valutazione Iniziale

**Controlla prima il contesto di product marketing:**
Se esiste `.agents/product-marketing.md` (oppure `.claude/product-marketing.md`, o il vecchio nome file `product-marketing-context.md`, in setup più datati), leggilo prima di fare domande. Usa quel contesto e chiedi solo le informazioni non già coperte o specifiche per questo task.

Prima di fornire raccomandazioni, capisci:

1. **Contesto dell'Upgrade** - Freemium → Pagamento? Prova → Pagamento? Upgrade di livello? Upsell di funzionalità? Limite di utilizzo?

2. **Modello di Prodotto** - Cos'è gratuito? Cosa è dietro il paywall? Cosa attiva i prompt? Tasso di conversione attuale?

3. **Percorso dell'Utente** - Quando appare questo? Cosa hanno sperimentato? Cosa stanno cercando di fare?

---

## Principi Fondamentali

### 1. Il Valore Prima della Richiesta
- L'utente dovrebbe aver sperimentato un valore reale prima
- L'upgrade dovrebbe sembrare un passo successivo naturale
- Tempistica: Dopo il "momento aha," non prima

### 2. Mostra, Non Solo Dire
- Dimostra il valore delle funzionalità a pagamento
- Mostra in anteprima ciò che manca
- Rendi l'upgrade tangibile

### 3. Percorso Senza Attrito
- Facile fare l'upgrade quando si è pronti
- Non farli cercare il pricing

### 4. Rispetta il No
- Non intrappolare o forzare
- Rendi facile continuare gratuitamente
- Mantieni la fiducia per la conversione futura

---

## Punti di Trigger del Paywall

### Feature Gate
Quando l'utente clicca su una funzionalità a pagamento:
- Spiegazione chiara del perché è a pagamento
- Mostra cosa fa la funzionalità
- Percorso rapido per sbloccarla
- Opzione per continuare senza

### Limiti di Utilizzo
Quando l'utente raggiunge un limite:
- Indicazione chiara del limite raggiunto
- Mostra cosa offre l'upgrade
- Non bloccare bruscamente

### Scadenza della Prova
Quando la prova sta per finire:
- Avvisi anticipati (7, 3, 1 giorno)
- "Cosa succede" chiaro alla scadenza
- Riassumi il valore ricevuto

### Prompt Basati sul Tempo
Dopo X giorni di utilizzo gratuito:
- Promemoria gentile di upgrade
- Evidenzia le funzionalità a pagamento non utilizzate
- Facile da chiudere

---

## Componenti della Schermata di Paywall

1. **Titolo** - Concentrati su cosa ottengono: "Sblocca [Funzionalità] per [Beneficio]"

2. **Dimostrazione del Valore** - Anteprima, prima/dopo, "Con Pro potresti..."

3. **Confronto delle Funzionalità** - Evidenzia le differenze chiave, piano attuale contrassegnato

4. **Prezzo** - Chiaro, semplice, opzioni annuale vs. mensile

5. **Social Proof** - Citazioni di clienti, "X team usano questo"

6. **CTA** - Specifica e orientata al valore: "Inizia a Ottenere [Beneficio]"

7. **Via di Fuga** - "Non ora" o "Continua con Gratuito" chiaramente visibili

---

## Tipi Specifici di Paywall

### Paywall a Blocco di Funzionalità
```
[Icona Lucchetto]
Questa funzionalità è disponibile su Pro

[Anteprima/screenshot della funzionalità]

[Nome funzionalità] ti aiuta a [beneficio]:
• [Capacità]
• [Capacità]

[Passa a Pro - X €/mese]
[Magari Più Tardi]
```

### Paywall di Limite di Utilizzo
```
Hai raggiunto il tuo limite gratuito

[Barra di progresso al 100%]

Gratuito: 3 progetti | Pro: Illimitati

[Passa a Pro]  [Elimina un progetto]
```

### Paywall di Scadenza Prova
```
La tua prova termina in 3 giorni

Cosa perderai:
• [Funzionalità usata]
• [Dati creati]

Cosa hai realizzato:
• Creato X progetti

[Continua con Pro]
[Ricordamelo più tardi]  [Effettua il downgrade]
```

---

## Tempistica e Frequenza

### Quando Mostrarlo
- Dopo il momento di valore, prima della frustrazione
- Dopo l'attivazione/momento aha
- Quando si raggiungono limiti reali

### Quando NON Mostrarlo
- Durante l'onboarding (troppo presto)
- Quando sono in un flusso
- Ripetutamente dopo la chiusura

### Regole di Frequenza
- Limita per sessione
- Periodo di pausa dopo la chiusura (giorni, non ore)
- Traccia i segnali di fastidio

---

## Ottimizzazione del Flusso di Upgrade

### Dal Paywall al Pagamento
- Minimizza i passaggi
- Resta nel contesto se possibile
- Precompila le informazioni note

### Dopo l'Upgrade
- Accesso immediato alle funzionalità
- Conferma e ricevuta
- Guida alle nuove funzionalità

---

## A/B Testing

### Cosa Testare
- Tempistica del trigger
- Variazioni di titolo/copy
- Presentazione del prezzo
- Durata della prova
- Enfasi sulle funzionalità
- Design/layout

### Metriche da Tracciare
- Tasso di impressione del paywall
- Click-through verso l'upgrade
- Tasso di completamento
- Fatturato per utente
- Tasso di churn post-upgrade

**Per idee di esperimenti complete**: Vedi [references/experiments.md](references/experiments.md)

---

## Anti-Pattern da Evitare

### Dark Pattern
- Nascondere il bottone di chiusura
- Selezione del piano confusa
- Copy basato sul senso di colpa

### Killer di Conversione
- Chiedere prima che il valore sia stato consegnato
- Prompt troppo frequenti
- Bloccare flussi critici
- Processo di upgrade complicato

---

## Domande Specifiche per il Task

1. Qual è il tuo tasso di conversione attuale da gratuito a pagamento?
2. Cosa attiva i prompt di upgrade oggi?
3. Quali funzionalità sono dietro il paywall?
4. Qual è il tuo "momento aha" per gli utenti?
5. Quale modello di pricing? (per posto, a consumo, fisso)
6. App mobile, web app, o entrambe?

---

## Skill Correlate

- **churn-prevention**: Per i flussi di cancellazione, le offerte di salvataggio e la riduzione del churn post-upgrade
- **cro**: Per l'ottimizzazione della pagina prezzi pubblica
- **onboarding**: Per guidare verso il momento aha prima dell'upgrade
- **ab-testing**: Per testare le varianti del paywall
