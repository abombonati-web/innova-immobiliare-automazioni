# Punto aperto — Il modulo online

## Stato

Il contenuto esatto del modulo su `https://www.innovaexperience.it/modulo` **non è stato
recuperato**. Il dominio è bloccato dalla policy di rete dell'ambiente di sviluppo: ogni
richiesta viene rifiutata dal proxy aziendale con un 403 sul tunnel, prima ancora di
raggiungere il sito. Non è un problema del sito — da un browser normale la pagina si apre
regolarmente — ed è una regola che non va aggirata.

Quindi lo schema in `config/modulo-campi.json` è una **proposta**, non una fotografia
del modulo reale.

## Perché non blocca nulla

Il motore del semaforo non legge i campi del modulo: legge i **campi canonici**. Fra il
modulo e il motore c'è una mappa di corrispondenze. Cambiare il modulo, o scoprire che si
chiama diversamente da come immaginato, significa aggiungere righe a quella mappa — non
toccare il codice.

```
modulo reale          →  mappa corrispondenze  →  campo canonico  →  regole semaforo
"Come pensi di pagare?"  →  modalita_acquisto   →  contanti / mutuo…  →  verde / giallo
```

## I quattro campi che contano davvero

Di tutto il modulo, il semaforo ne usa quattro:

| Campo canonico | A cosa serve | Se manca |
|---|---|---|
| `intento` | sceglie il percorso: acquisto, affitto, valutazione | si chiede in pagina |
| `modalita_acquisto` | **è il campo che governa il semaforo** | esito giallo per dati incompleti |
| `budget_massimo` | confronto con il prezzo → esito rosso se troppo distante | il rosso non scatta mai |
| `reddito_mensile_netto` | solo affitto: incidenza del canone | affitto sempre in verifica |

Il campo decisivo è il secondo. Le sue sei opzioni proposte, con l'esito che producono:

| Opzione mostrata al cliente | Esito |
|---|---|
| Con liquidità già disponibile | 🟢 verde |
| Con un mutuo già deliberato dalla banca | 🟢 verde |
| Ho una pratica di mutuo in corso | 🟡 giallo |
| Dovrò richiedere un mutuo | 🟡 giallo |
| Devo prima vendere un altro immobile | 🟡 giallo |
| Non l'ho ancora deciso | 🟡 giallo |

## Come si chiude, in cinque minuti

Serve solo l'elenco dei campi del modulo attuale. Tre modi, uno vale l'altro:

1. Apri la pagina del modulo nel browser, seleziona tutto (Ctrl+A), copia e incolla il testo
   in una risposta qui. Bastano etichette e opzioni delle tendine.
2. Un paio di screenshot del modulo per intero.
3. Se il modulo è costruito con uno strumento che permette l'esportazione (Google Form,
   Typeform, un plugin WordPress), l'esportazione dei campi va benissimo.

Con quello in mano:

- si compila `corrispondenze.mappa` in `config/modulo-campi.json`;
- si allineano le opzioni reali a quelle canoniche;
- si aggiunge un test per ogni opzione nuova che deve produrre un esito.

Nessuna riga dei motori cambia.

## Se il modulo reale non chiede la modalità di pagamento

È il caso più probabile, ed è la ragione per cui questo punto era rimasto aperto nel tuo
documento. Senza quel campo il semaforo non ha su cosa decidere e tutto finisce in giallo,
cioè tutto passa dal consulente — che è esattamente il collo di bottiglia che il sistema
dovrebbe togliere.

In quel caso la domanda va aggiunta. Una sola tendina, sei opzioni, posizionata **dopo** i
campi di contatto: chiedere come si paga prima del nome fa scappare la gente, chiederlo
dopo — quando il modulo è quasi finito — ha un tasso di risposta molto più alto.
