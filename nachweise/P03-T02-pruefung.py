"""Kleine lokale Abnahme der Abschnittsbildung und tatsächlichen Quellensuche."""
import hashlib
import json
import platform
import sys
from datetime import datetime
from pathlib import Path

PROJEKTORDNER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJEKTORDNER / "src"))
from suchen import abschnitte_aufteilen, dokumente_aufteilen, mit_quellen_suchen


def pruefen():
    print(f"Prüfzeitpunkt: {datetime.now().astimezone().isoformat(timespec='seconds')}")
    print(f"Python: {platform.python_version()}")
    abschnitte = abschnitte_aufteilen(
        "# Erster Titel\n\nErster Absatz.\nZweite Zeile.\n\nZweiter Absatz.\n"
        "## Zweiter Titel\nDritter Absatz.\n", "prueftext.md"
    )
    assert [abschnitt["abschnittskennung"] for abschnitt in abschnitte] == [
        "A001", "A002", "A003"
    ]
    assert [abschnitt["ueberschrift"] for abschnitt in abschnitte] == [
        "Erster Titel", "Erster Titel", "Zweiter Titel"
    ]
    assert abschnitte[0]["text"] == "Erster Absatz.\nZweite Zeile."
    assert abschnitte_aufteilen("# Nur Überschrift\n\n", "leer.md") == []
    print("BESTANDEN: mehrere Absätze, mehrzeiliger Text, Überschriftenwechsel, leerer Inhalt.")

    dokumentordner = PROJEKTORDNER / "dokumente"
    abschnitte = dokumente_aufteilen(dokumentordner)
    assert len(abschnitte) == 3
    assert len({(a["dateiname"], a["abschnittskennung"]) for a in abschnitte}) == 3
    for abschnitt in abschnitte:
        original = (dokumentordner / abschnitt["dateiname"]).read_text(encoding="utf-8-sig")
        assert abschnitt["text"] in original
    print("BESTANDEN: 3 Originaldokumente ergeben 3 eindeutig referenzierte, wörtliche Absätze.")

    for suchtext, dateiname in [("Port 8081", "start.md"),
                                ("personenbezogenen Daten", "daten.md"),
                                ("Demoprotokolle", "support.md")]:
        treffer = mit_quellen_suchen(suchtext)
        assert treffer[0]["dateiname"] == dateiname
        assert treffer[0]["abschnittskennung"] == "A001"
        assert treffer == mit_quellen_suchen(suchtext.upper())
        assert all(t["text"] in (dokumentordner / t["dateiname"]).read_text(
            encoding="utf-8-sig") for t in treffer)
        print(json.dumps({"suchtext": suchtext, "treffer": treffer}, ensure_ascii=False))
    assert mit_quellen_suchen("Port") == mit_quellen_suchen("Port")
    assert [t["dateiname"] for t in mit_quellen_suchen("Port")] == ["start.md", "support.md"]
    assert mit_quellen_suchen("Administratorkennwort") == []
    print("BESTANDEN: Quellen aller 3 Dateien, Rangfolge, Großschreibung und leere Trefferliste.")

    for suchtext in ["", "?!", "wie der die"]:
        try:
            mit_quellen_suchen(suchtext)
        except ValueError as fehler:
            print(f"Erwarteter Eingabefehler für {suchtext!r}: {fehler}")
        else:
            raise AssertionError("Ungültige Suche wurde nicht abgelehnt.")

    # Unveränderte Originalbeispiele gegen die bereits gesicherten T01-Prüfsummen prüfen.
    vorheriges_protokoll = (PROJEKTORDNER / "nachweise/P03-T01-konsistenz.txt").read_text(
        encoding="utf-8-sig"
    )
    for pfad in [*sorted(dokumentordner.glob("*.md")),
                 PROJEKTORDNER / "beispieldaten/fragen.json"]:
        zeile = f"SHA256 {pfad.relative_to(PROJEKTORDNER).as_posix()}: {hashlib.sha256(pfad.read_bytes()).hexdigest()}"
        assert zeile in vorheriges_protokoll
        print(zeile)
    fragen = json.loads((PROJEKTORDNER / "beispieldaten/fragen.json").read_text(encoding="utf-8-sig"))
    assert len(fragen) == 10
    for pfad in [PROJEKTORDNER / "src/suchen.py", Path(__file__)]:
        print(f"SHA256 {pfad.relative_to(PROJEKTORDNER).as_posix()}: {hashlib.sha256(pfad.read_bytes()).hexdigest()}")
    print("BESTANDEN: P03-T02-Endpunkt; 3 Dokumente und 10 Fragen unverändert.")
    print("Grenze: Wortabgleich; keine semantische Antwortprüfung, kein Modell, kein MCP.")
    return 0


if __name__ == "__main__":
    raise SystemExit(pruefen())
