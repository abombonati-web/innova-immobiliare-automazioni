/* ============================================================
   INNOVA EXPERIENCE — lato server della piattaforma
   ------------------------------------------------------------
   Questa funzione risponde su /api/… e collega le rotte
   (rotte.mjs) all'archivio condiviso nei Netlify Blobs e
   all'invio dell'email di riepilogo.

     POST /api/lead          pubblico  — una nuova candidatura entra
                                         in archivio con la sua
                                         attività fissa, e parte
                                         l'email di riepilogo
     POST /api/accesso       pubblico  — password condivisa → token
     GET  /api/archivio      riservato — l'archivio completo
     POST /api/sincronizza   riservato — invia le modifiche fatte e
                                         riceve l'archivio aggiornato

   Variabili d'ambiente da impostare su Netlify:
     INNOVA_PASSWORD   password di accesso alla gestione
     INNOVA_SEGRETO    stringa lunga e casuale per firmare i token
     INNOVA_EMAIL      casella a cui arrivano i riepiloghi
                       (se assente: info@innovaimmobiliare.it)
============================================================ */

import { getStore } from "@netlify/blobs";
import { creaGestore } from "./rotte.mjs";

export const config = { path: "/api/*" };

const NOME_STORE = "innova-experience";
const CHIAVE = "archivio";

const gestore = creaGestore({
  leggi:  () => getStore(NOME_STORE).get(CHIAVE, { type: "json" }),
  scrivi: (archivio) => getStore(NOME_STORE).setJSON(CHIAVE, archivio),

  /* L'email di riepilogo parte via FormSubmit, la stessa casella già in uso */
  inviaEmail: async (corpo, casella) => {
    const r = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(casella), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(corpo)
    });
    return r.ok;
  },

  env: process.env
});

export default (req) => gestore(req);
