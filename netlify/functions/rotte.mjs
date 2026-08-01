/* ============================================================
   INNOVA EXPERIENCE — le rotte della piattaforma
   ------------------------------------------------------------
   Le regole di risposta, separate da dove l'archivio è
   materialmente conservato e da come parte l'email: quei due
   pezzi arrivano da fuori, così le rotte si possono provare
   per intero senza dipendere da Netlify.
============================================================ */

import {
  ARCHIVIO_VUOTO, ATTIVITA_FISSA,
  nuovoContatto, nuovaAttivitaFissa, trovaDuplicato, fondiArchivio,
  creaToken, tokenValido, passwordCorretta, costruisciEmail
} from "./nucleo.mjs";

const json = (corpo, stato = 200) => new Response(JSON.stringify(corpo), {
  status: stato,
  headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
});
const errore = (messaggio, stato) => json({ errore: messaggio }, stato);

/**
 * @param leggi   () => Promise<archivio|null>
 * @param scrivi  (archivio) => Promise<void>
 * @param inviaEmail (corpo, casella) => Promise<boolean>
 * @param env     variabili d'ambiente
 */
export function creaGestore({ leggi, scrivi, inviaEmail, env = {} }){

  async function archivioCorrente(){
    const dati = await leggi();
    if(!dati) return { ...ARCHIVIO_VUOTO, contatti: [], attivita: [], attivitaFissa: { ...ATTIVITA_FISSA } };
    return {
      contatti: dati.contatti || [],
      attivita: dati.attivita || [],
      attivitaFissa: dati.attivitaFissa || { ...ATTIVITA_FISSA },
      versione: dati.versione || 0,
      aggiornato: dati.aggiornato || null
    };
  }

  function autorizzato(req){
    const token = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "").trim();
    return tokenValido(token, env.INNOVA_SEGRETO);
  }

  return async function gestore(req){
    const url = new URL(req.url);
    const rotta = url.pathname.replace(/^\/api\/?/, "").replace(/\/$/, "");

    try{
      /* ---------- Una candidatura entra nella piattaforma ---------- */
      if(rotta === "lead" && req.method === "POST"){
        const dati = await req.json().catch(() => ({}));
        if(dati._honey) return json({ ok: true });          /* spam: si scarta in silenzio */
        if(!dati.nome && !dati.telefono && !dati.email){
          return errore("Servono almeno un nome o un recapito.", 400);
        }

        const archivio = await archivioCorrente();

        /* Chi ha già scritto non diventa un doppione: la scheda si
           aggiorna e il richiamo viene comunque messo in agenda. */
        const esistente = trovaDuplicato(archivio.contatti, dati);
        let contatto;
        if(esistente){
          contatto = {
            ...esistente,
            nome:          dati.nome          || esistente.nome,
            telefono:      dati.telefono      || esistente.telefono,
            email:         dati.email         || esistente.email,
            slot:          dati.slot          || esistente.slot,
            interesse:     dati.interesse     || esistente.interesse,
            finanziamento: dati.finanziamento || esistente.finanziamento,
            note:          [esistente.note, dati.note].filter(Boolean).join("\n—\n"),
            aggiornato:    new Date().toISOString()
          };
          archivio.contatti = archivio.contatti.map(c => c.id === contatto.id ? contatto : c);
        }else{
          contatto = nuovoContatto(dati);
          archivio.contatti.unshift(contatto);
        }

        const attivita = nuovaAttivitaFissa(contatto, archivio.attivitaFissa);
        archivio.attivita.unshift(attivita);
        archivio.versione = (archivio.versione || 0) + 1;
        archivio.aggiornato = new Date().toISOString();
        await scrivi(archivio);

        /* L'email è un di più: se non parte, la lead resta comunque in archivio */
        let emailInviata = false;
        try{
          const corpo = costruisciEmail(contatto, attivita, `${url.origin}/gestione.html#contatto=${contatto.id}`);
          emailInviata = await inviaEmail(corpo, env.INNOVA_EMAIL || "info@innovaimmobiliare.it");
        }catch(_){ emailInviata = false; }

        return json({ ok: true, contattoId: contatto.id, giaPresente: !!esistente, emailInviata });
      }

      /* ---------- Accesso ---------- */
      if(rotta === "accesso" && req.method === "POST"){
        const { password } = await req.json().catch(() => ({}));
        if(!env.INNOVA_PASSWORD || !env.INNOVA_SEGRETO){
          return errore("La piattaforma non è ancora configurata: mancano INNOVA_PASSWORD e INNOVA_SEGRETO.", 503);
        }
        if(!passwordCorretta(password, env.INNOVA_PASSWORD)) return errore("Password errata.", 401);
        return json({ token: creaToken(env.INNOVA_SEGRETO) });
      }

      /* ---------- Lettura dell'archivio ---------- */
      if(rotta === "archivio" && req.method === "GET"){
        if(!autorizzato(req)) return errore("Accesso non valido.", 401);
        return json(await archivioCorrente());
      }

      /* ---------- Sincronizzazione ---------- */
      if(rotta === "sincronizza" && req.method === "POST"){
        if(!autorizzato(req)) return errore("Accesso non valido.", 401);
        const arrivato = await req.json().catch(() => ({}));
        const unito = fondiArchivio(await archivioCorrente(), arrivato);
        await scrivi(unito);
        return json(unito);
      }

      return errore("Rotta non trovata.", 404);

    }catch(e){
      return errore("Errore della piattaforma: " + e.message, 500);
    }
  };
}
