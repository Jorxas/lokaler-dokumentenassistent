"""Prüft den vorbereiteten Fragenkatalog, ohne eine Suche auszuführen."""

import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path


def pruefen():
    projektordner = Path(__file__).resolve().parents[1]
    fragenpfad = projektordner / "beispieldaten/fragen.json"
    erwartungspfad = projektordner / "nachweise/P03-T01-erwartungen.json"
    fragen = json.loads(fragenpfad.read_text(encoding="utf-8-sig"))
    erwartungen = json.loads(erwartungspfad.read_text(encoding="utf-8"))
    dokumentpfade = sorted((projektordner / "dokumente").glob("*.md"))
    dokumente = {
        pfad.name: pfad.read_text(encoding="utf-8-sig") for pfad in dokumentpfade
    }
    fehler = []

    def kontrollieren(bedingung, meldung):
        if not bedingung:
            fehler.append(meldung)

    kontrollieren(set(dokumente) == {"start.md", "daten.md", "support.md"},
                  "Die drei erwarteten Dokumente müssen vorhanden sein.")
    kontrollieren(all(inhalt.strip() for inhalt in dokumente.values()),
                  "Ein Dokument ist leer.")
    kontrollieren(len(fragen) == len(erwartungen) == 10,
                  "Genau zehn Fragen und zehn Erwartungen erforderlich.")
    kontrollieren(len({eintrag["frage"] for eintrag in fragen}) == 10,
                  "Die zehn Fragen müssen verschieden sein.")
    kontrollieren(sum(eintrag["quelle"] is None for eintrag in fragen) == 2,
                  "Genau zwei Fragen müssen ohne Quelle bleiben.")

    print(f"Prüfzeitpunkt: {datetime.now().astimezone().isoformat(timespec='seconds')}")
    print(f"Python: {platform.python_version()}")
    for nummer, (frage, erwartung) in enumerate(zip(fragen, erwartungen), start=1):
        kontrollieren(frage["frage"] == erwartung["frage"],
                      f"Frage {nummer}: Fragetext weicht ab.")
        kontrollieren(frage["quelle"] == erwartung["quelle"],
                      f"Frage {nummer}: Erwartete Quelle weicht ab.")
        quelle = erwartung["quelle"]
        antwort = erwartung["erwartete_antwort"]
        beleg = erwartung["beleg"]
        kontrollieren(isinstance(antwort, str) and bool(antwort.strip()),
                      f"Frage {nummer}: Erwartete Antwort fehlt.")
        if quelle is None:
            kontrollieren(beleg is None and antwort.startswith("Unbeantwortbar:"),
                          f"Frage {nummer}: Unbeantwortbarkeit nicht eindeutig markiert.")
        else:
            kontrollieren(quelle in dokumente and isinstance(beleg, str)
                          and bool(beleg) and beleg in dokumente.get(quelle, ""),
                          f"Frage {nummer}: Beleg fehlt im erwarteten Dokument.")
        print(f"{nummer:02d}: {frage['frage']} | {quelle or 'Unbeantwortbar'}")

    for pfad in [*dokumentpfade, fragenpfad, erwartungspfad, Path(__file__)]:
        pruefsumme = hashlib.sha256(pfad.read_bytes()).hexdigest()
        print(f"SHA256 {pfad.relative_to(projektordner).as_posix()}: {pruefsumme}")
    if fehler:
        for meldung in fehler:
            print(f"FEHLER: {meldung}")
        return 1
    print("BESTANDEN: 3 Dokumente, 10 Fragen, 8 Quellenbelege, 2 unbeantwortbare Fragen.")
    print("Grenze: Struktur- und Belegabgleich; keine Such- oder Modellantworten geprüft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(pruefen())
