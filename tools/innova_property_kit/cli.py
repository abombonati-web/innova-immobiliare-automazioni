"""Interfaccia a riga di comando del kit.

    python innova_property_kit.py \\
      --brief briefs/via-petrarca-36.json \\
      --drive-folder-id <id cartella immobile> \\
      --old-price 168000 --new-price 155000 \\
      --event-date 2026-08-05 --event-slots "12:00,15:30" \\
      --video-tone euforico --video-music jazz \\
      --output-dir ./output
"""

from __future__ import annotations

import argparse
import logging
import sys
import tempfile
import time
from pathlib import Path

from . import audio as au
from . import fmt, landing, pdf, photos, reel, script, slides, video, voice
from .brand import VOICE_TONES
from .model import MissingDataError, PropertyBrief

log = logging.getLogger("innova")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="innova_property_kit",
        description="Genera reel verticale + landing page (HTML e PDF) per un immobile Innova.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    source = parser.add_argument_group("immobile")
    source.add_argument("--brief", type=Path, help="JSON con i dati dell'immobile (vedi briefs/)")
    source.add_argument(
        "--property", dest="property_name",
        help="Nome/indirizzo dell'immobile (accetta anche 'Via X 1, Palermo')",
    )
    source.add_argument("--city", help="Comune dell'immobile (obbligatorio se non c'e --brief)")
    source.add_argument("--old-price", type=int, help="Prezzo precedente in euro")
    source.add_argument("--new-price", type=int, help="Nuovo prezzo ribassato in euro")
    source.add_argument("--event-date", help="Data dell'Innova Experience (YYYY-MM-DD)")
    source.add_argument("--event-slots", help="Orari dell'evento separati da virgola, es. '12:00,15:30'")
    source.add_argument("--phone", help="Telefono da mostrare nei materiali")

    photos_group = parser.add_argument_group("foto")
    photos_group.add_argument("--drive-folder-id", help="ID della cartella Drive dell'immobile")
    photos_group.add_argument("--drive-search", help="Cerca la cartella su Drive per nome")
    photos_group.add_argument("--photos-dir", type=Path, help="Cartella locale con le foto")
    photos_group.add_argument("--photos-manifest", type=Path, help="JSON con le foto gia scaricate")
    photos_group.add_argument("--photos", type=int, default=6, help="Quante foto usare (default: 6)")

    video_group = parser.add_argument_group("video")
    video_group.add_argument(
        "--video-tone", choices=sorted(VOICE_TONES), default="euforico",
        help="Registro della voce nel reel (default: euforico)",
    )
    video_group.add_argument(
        "--video-music", choices=["jazz", "nessuna"], default="jazz",
        help="Sottofondo musicale del reel (default: jazz)",
    )
    video_group.add_argument("--bpm", type=int, default=92, help="BPM del letto jazz (default: 92)")
    video_group.add_argument(
        "--max-duration", type=float, default=30.0,
        help="Durata massima del reel in secondi (default: 30)",
    )

    landing_group = parser.add_argument_group("landing")
    landing_group.add_argument(
        "--landing-tone", choices=sorted(VOICE_TONES), default="professionale",
        help="Registro della voce nella landing (default: professionale)",
    )

    output = parser.add_argument_group("output")
    output.add_argument("--output-dir", type=Path, default=Path("output"), help="Cartella dei deliverable")
    output.add_argument("--work-dir", type=Path, help="Cartella di lavoro (default: temporanea)")
    output.add_argument("--name", help="Basename dei file prodotti (default: dallo slug dell'immobile)")
    output.add_argument("--skip-video", action="store_true", help="Non generare il video")
    output.add_argument("--skip-landing", action="store_true", help="Non generare la landing HTML")
    output.add_argument("--skip-pdf", action="store_true", help="Non generare il PDF")
    output.add_argument("--keep-work-dir", action="store_true", help="Non cancellare i file intermedi")
    output.add_argument("-v", "--verbose", action="store_true", help="Log di debug")
    return parser


def load_brief(args: argparse.Namespace) -> PropertyBrief:
    if args.brief:
        brief = PropertyBrief.load(args.brief)
    elif args.property_name:
        brief = PropertyBrief.from_dict({"property": {"name": args.property_name}})
    else:
        raise MissingDataError(["--brief oppure --property: senza i dati non si genera nulla"])

    brief.apply_overrides(
        property=args.property_name,
        city=args.city,
        old_price=args.old_price,
        new_price=args.new_price,
        event_date=args.event_date,
        event_slots=args.event_slots,
        phone=args.phone,
    )
    return brief.validate()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
        stream=sys.stdout,
    )

    started = time.time()
    try:
        brief = load_brief(args)
    except (MissingDataError, ValueError) as exc:
        print(f"\n✗ {exc}\n", file=sys.stderr)
        return 2

    print()
    print(brief.summary())
    print()

    work_root = args.work_dir or Path(tempfile.mkdtemp(prefix="innova-kit-"))
    work_root.mkdir(parents=True, exist_ok=True)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.name or brief.slug
    produced: list[Path] = []

    # ---------------------------------------------------------------- foto ---
    log.info("[1/5] foto dell'immobile")
    drive_search = args.drive_search
    if not any([args.photos_dir, args.photos_manifest, args.drive_folder_id, drive_search]):
        # nessuna sorgente indicata: si tenta la ricerca su Drive per nome immobile
        drive_search = brief.title
    picture_list = photos.fetch_property_photos(
        args.photos,
        photos_dir=args.photos_dir,
        manifest=args.photos_manifest,
        drive_folder_id=args.drive_folder_id,
        drive_search=drive_search,
        work_dir=work_root / "foto",
    )

    # --------------------------------------------------------------- video ---
    if not args.skip_video:
        log.info("[2/5] slide brandizzate")
        slide_set = slides.build_all_slides(brief, work_root / "slides")

        log.info("[3/5] voce narrante (%s)", args.video_tone)
        segments = [(s.key, s.text) for s in script.video_script(brief)]
        track = voice.synthesize_voice(segments, tone=args.video_tone)

        timeline = reel.build_timeline(
            brief, picture_list, slide_set, track, work_root / "overlay",
            max_duration=args.max_duration,
        )
        soundtrack = video.build_soundtrack(
            timeline,
            {clip.key: clip.samples for clip in track.clips},
            music="jazz" if args.video_music == "jazz" else "nessuna",
            bpm=args.bpm,
        )
        audio_path = au.write_wav(work_root / "colonna-sonora.wav", soundtrack)

        suffix = "VoceJazz" if args.video_music == "jazz" else "Voce"
        video_path = output_dir / f"Innova_{fmt.camel(brief.title)}_{suffix}.mp4"
        video.assemble_video(timeline, audio_path, video_path, work_root / "clips")
        produced.append(video_path)
    else:
        log.info("[2-3/5] video saltato (--skip-video)")

    # ------------------------------------------------------------- landing ---
    if not args.skip_landing:
        log.info("[4/5] presentazione vocale della landing (%s)", args.landing_tone)
        narration_wav, narration_seconds = voice.render_narration(
            script.landing_script(brief),
            work_root / "landing-voce.wav",
            tone=args.landing_tone,
        )
        narration_mp3 = au.wav_to_mp3(narration_wav, work_root / "landing-voce.mp3")
        log.info("  %.1fs, %d KB", narration_seconds, narration_mp3.stat().st_size // 1024)

        html_path = output_dir / f"landing-{basename}.html"
        landing.build_landing_html(brief, picture_list, html_path, audio_path=narration_mp3)
        produced.append(html_path)

        if not args.skip_pdf:
            log.info("[5/5] versione stampabile")
            produced.append(
                pdf.html_to_pdf(
                    html_path,
                    output_dir / f"landing-{basename}.pdf",
                    maps_url=brief.maps_url,
                    address=brief.full_address,
                )
            )
    else:
        log.info("[4-5/5] landing saltata (--skip-landing)")

    if not args.keep_work_dir and args.work_dir is None:
        import shutil

        shutil.rmtree(work_root, ignore_errors=True)
    else:
        log.info("file intermedi in %s", work_root)

    print("\nDeliverable prodotti:")
    for path in produced:
        print(f"  {path}  ({path.stat().st_size / 1e6:.1f} MB)")
    print(f"\nCompletato in {time.time() - started:.0f}s.\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
