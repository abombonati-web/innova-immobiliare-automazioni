# innova-immobiliare-automazioni

Automazioni Make, script CRM e workflow per Innova Immobiliare.

## Contenuto

| Cosa | Dove |
|---|---|
| Landing page Innova Experience — Villa Città Giardino (pubblicata su GitHub Pages) | `index.html` |
| **Innova Property Kit** — genera reel verticale + landing page + PDF da un brief immobile | `innova_property_kit.py`, `tools/innova_property_kit/` |
| Brief degli immobili (dati dalle schede ufficiali) | `briefs/` |
| Documentazione del kit | [`docs/innova-property-kit.md`](docs/innova-property-kit.md) |

## Innova Property Kit in breve

```bash
apt-get install -y ffmpeg wkhtmltopdf
pip install -r requirements.txt

python innova_property_kit.py \
  --brief briefs/via-petrarca-36.json \
  --drive-folder-id <id cartella immobile su Drive> \
  --old-price 168000 --new-price 155000 \
  --event-date 2026-08-05 --event-slots "12:00,15:30" \
  --video-tone euforico --video-music jazz \
  --output-dir ./output
```

Produce:

* `Innova_Petrarca36_VoceJazz.mp4` — reel 1080×1920 con voce narrante italiana e jazz sintetizzato;
* `landing-via-petrarca-36.html` — landing page autonoma (foto e audio incorporati) con player vocale;
* `landing-via-petrarca-36.pdf` — versione stampabile.

Tutto in locale con software open source: niente TTS a pagamento, niente musica con
royalty, niente servizi cloud. Prezzo, metratura e date evento non vengono mai dedotti:
se un dato manca, il tool si ferma e lo chiede.

Test: `python -m pytest tests -q`
