/* ============================================================
   CALCOLI ECONOMICI DELLA LANDING
   ------------------------------------------------------------
   Provvigioni in chiaro e stima dei costi dei tre passaggi
   dell'acquisto (o degli importi da versare in caso di affitto).

   Tutti i numeri arrivano dai file di configurazione: aliquote,
   moltiplicatori catastali e percentuali non sono scritti qui
   dentro, così quando la normativa cambia si aggiorna un JSON.
   ============================================================ */

export function euro(valore, decimali = 0) {
  if (valore === null || valore === undefined || Number.isNaN(valore)) return "—";
  return new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
    minimumFractionDigits: decimali,
    maximumFractionDigits: decimali
  }).format(valore);
}

export function percentuale(valore) {
  return `${(valore * 100).toLocaleString("it-IT", { maximumFractionDigits: 2 })}%`;
}

/* ---------- Provvigioni ---------- */

/**
 * Calcola la provvigione dovuta a Innova, imponibile e IVA separate.
 * @returns {{imponibile:number, iva:number, totale:number, criterio:string}}
 */
export function calcolaProvvigione(immobile, config) {
  const pubblico = immobile.pubblico;
  const iva = config.iva;

  if (immobile.tipo_operazione === "affitto") {
    const canoneAnnuo = (pubblico.canone_mensile || 0) * 12;
    const imponibile = canoneAnnuo * config.affitto.percentuale;
    return {
      imponibile,
      iva: imponibile * iva,
      totale: imponibile * (1 + iva),
      criterio: config.affitto.testo,
      quando: config.affitto.quando_e_dovuta,
      base: canoneAnnuo
    };
  }

  const prezzo = pubblico.prezzo || 0;
  const scaglione = prezzo <= config.vendita.soglia
    ? config.vendita.sotto_soglia
    : config.vendita.sopra_soglia;

  const imponibile = scaglione.tipo === "fisso"
    ? scaglione.importo
    : prezzo * scaglione.percentuale;

  return {
    imponibile,
    iva: imponibile * iva,
    totale: imponibile * (1 + iva),
    criterio: scaglione.testo,
    quando: config.vendita.quando_e_dovuta,
    base: prezzo
  };
}

/* ---------- Valore catastale e imposta di registro ---------- */

/**
 * Valore catastale con il meccanismo "prezzo-valore": la base
 * imponibile del rogito non è il prezzo pagato ma la rendita
 * catastale rivalutata e moltiplicata.
 */
export function valoreCatastale(rendita, primaCasa, config) {
  if (!rendita) return null;
  const moltiplicatori = config.vendita.moltiplicatori_catastali;
  const m = primaCasa ? moltiplicatori.prima_casa : moltiplicatori.seconda_casa;
  return rendita * m;
}

export function impostaRegistroRogito(rendita, primaCasa, config) {
  const base = valoreCatastale(rendita, primaCasa, config);
  if (base === null) return null;
  const aliquote = config.vendita.aliquote_registro;
  const aliquota = primaCasa ? aliquote.prima_casa : aliquote.seconda_casa;
  return Math.max(base * aliquota, aliquote.minimo);
}

/* ---------- I tre passaggi dell'acquisto ---------- */

/**
 * Costruisce le tre tappe con le voci di costo già calcolate sul
 * prezzo e sui dati catastali dell'immobile.
 *
 * @param {object} opzioni.primaCasa  true se l'acquirente ha i requisiti prima casa
 */
export function calcolaPassaggiVendita(immobile, configCosti, configProvvigioni, opzioni = {}) {
  const primaCasa = opzioni.primaCasa !== false;
  const prezzo = immobile.pubblico.prezzo || 0;
  const rendita = immobile.pubblico.rendita_catastale;
  const provvigione = calcolaProvvigione(immobile, configProvvigioni);

  // Serve per la voce "caparra al netto del deposito già versato".
  const vociProposta = configCosti.vendita.passaggi[0].voci;
  const deposito = prezzo * (vociProposta[0].percentuale || 0);

  let caparraLorda = 0;

  const passaggi = configCosti.vendita.passaggi.map((passaggio) => {
    const voci = passaggio.voci.map((voce) => {
      let importo = null;
      let dettaglio = voce.nota || "";

      switch (voce.calcolo) {
        case "fisso":
          importo = voce.importo;
          break;

        case "percentuale_prezzo":
          importo = prezzo * voce.percentuale;
          if (voce.id === "caparra") {
            caparraLorda = importo;
            importo = Math.max(0, importo - deposito); // il deposito è già nelle mani dell'agenzia
            dettaglio = `${voce.nota} Dal totale è già scalato il deposito di ${euro(deposito)} versato con la proposta.`;
          }
          break;

        case "percentuale_caparra":
          importo = caparraLorda * voce.percentuale;
          break;

        case "provvigione":
          importo = provvigione.totale;
          dettaglio = `${provvigione.criterio}. ${euro(provvigione.imponibile)} + IVA ${euro(provvigione.iva)}.`;
          break;

        case "saldo_prezzo":
          importo = prezzo - caparraLorda;
          break;

        case "imposta_registro_catastale": {
          importo = impostaRegistroRogito(rendita, primaCasa, configCosti);
          const base = valoreCatastale(rendita, primaCasa, configCosti);
          dettaglio = base
            ? `Calcolata su un valore catastale di ${euro(base)} (rendita ${euro(rendita, 2)}), aliquota ${primaCasa ? "2% prima casa" : "9% seconda casa"}. ${voce.nota}`
            : "Rendita catastale non disponibile: importo da calcolare.";
          break;
        }

        case "stima_notaio": {
          const stima = configCosti.vendita.stima_notaio;
          const calcolata = Math.min(
            Math.max(prezzo * stima.percentuale_prezzo, stima.minimo),
            stima.massimo
          );
          importo = calcolata;
          break;
        }

        default:
          importo = null;
      }

      return { ...voce, importo, dettaglio };
    });

    // Il saldo del prezzo non è un "costo aggiuntivo": va mostrato
    // ma tenuto fuori dal totale delle spese, altrimenti il numero
    // in pagina spaventa senza motivo.
    const totaleSpese = voci
      .filter((v) => v.calcolo !== "saldo_prezzo" && !v.scalata_dal_prezzo && v.importo)
      .reduce((somma, v) => somma + v.importo, 0);

    return { ...passaggio, voci, totale_spese: totaleSpese };
  });

  const totaleSpeseComplessive = passaggi.reduce((s, p) => s + p.totale_spese, 0);

  return {
    passaggi,
    prezzo,
    prima_casa: primaCasa,
    totale_spese_complessive: totaleSpeseComplessive,
    provvigione,
    avvertenza: configCosti.avvertenza
  };
}

/* ---------- Affitto ---------- */

export function calcolaImportiAffitto(immobile, configCosti, configProvvigioni) {
  const canone = immobile.pubblico.canone_mensile || 0;
  const canoneAnnuo = canone * 12;
  const provvigione = calcolaProvvigione(immobile, configProvvigioni);
  const cedolareSecca = (immobile.pubblico.tipo_contratto || "").toLowerCase().includes("cedolare");

  const risolvi = (voce) => {
    let importo = null;
    switch (voce.calcolo) {
      case "mensilita":
        importo = canone * voce.mensilita;
        break;
      case "provvigione":
        importo = provvigione.totale;
        break;
      case "percentuale_canone_annuo":
        importo = cedolareSecca ? 0 : canoneAnnuo * voce.percentuale;
        break;
      case "fisso":
        importo = voce.importo;
        break;
      default:
        importo = null;
    }
    const nonDovuta = voce.id === "registrazione" && cedolareSecca;
    return {
      ...voce,
      importo,
      dettaglio: nonDovuta
        ? "Non dovuta: il contratto è a cedolare secca."
        : voce.nota || ""
    };
  };

  const allaProposta = configCosti.affitto.alla_proposta.map(risolvi);
  const allaFirma = configCosti.affitto.alla_firma.map(risolvi);

  const somma = (voci) => voci.reduce((s, v) => s + (v.importo || 0), 0);

  return {
    canone,
    canone_annuo: canoneAnnuo,
    alla_proposta: allaProposta,
    alla_firma: allaFirma,
    totale_proposta: somma(allaProposta),
    totale_firma: somma(allaFirma),
    documenti_richiesti: configCosti.affitto.documenti_richiesti,
    come_velocizzare: configCosti.affitto.come_velocizzare,
    provvigione,
    cedolare_secca: cedolareSecca
  };
}
