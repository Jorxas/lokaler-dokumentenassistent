"""Lokale Stichwortsuche in Markdown-Absätzen mit überprüfbaren Quellen."""
import json
import re
import sys
from pathlib import Path

PROJEKTORDNER = Path(__file__).resolve().parents[1]

FUELLWOERTER = set("der die das den dem des ein eine einer einem einen und oder "
                  "wie was wo wann ich im in ist sind mit zu zum zur fuer für "
                  "welche welcher welches welchen".split())


def suchwoerter_bilden(text):
    return set(re.findall(r"\w+", text.casefold())) - FUELLWOERTER


def abschnitte_aufteilen(text, dateiname):
    """Jeder nicht leere Absatz wird ein Abschnitt; Überschriften geben Kontext."""
    abschnitte = []
    ueberschrift = ""
    absatz = []

    def absatz_sichern():
        if absatz:
            abschnitte.append({
                "dateiname": dateiname,
                "abschnittskennung": f"A{len(abschnitte) + 1:03d}",
                "ueberschrift": ueberschrift,
                "text": "\n".join(absatz),
            })
            absatz.clear()

    for zeile in text.splitlines():
        titel = re.match(r"^#{1,6}\s+(.+)$", zeile)
        if titel:
            absatz_sichern()
            ueberschrift = titel.group(1).strip()
        elif not zeile.strip():
            absatz_sichern()
        else:
            absatz.append(zeile)
    absatz_sichern()
    return abschnitte


def dokumente_aufteilen(dokumentordner):
    dokumentpfade = sorted(Path(dokumentordner).glob("*.md"))
    if not dokumentpfade:
        raise ValueError("Keine Markdown-Dokumente im Dokumentordner gefunden.")
    return [
        abschnitt
        for pfad in dokumentpfade
        for abschnitt in abschnitte_aufteilen(
            pfad.read_text(encoding="utf-8-sig"), pfad.name
        )
    ]


def mit_quellen_suchen(suchtext, dokumentordner=PROJEKTORDNER / "dokumente"):
    """Liefert wörtliche Absätze, geordnet nach Anzahl passender Suchwörter."""
    suchwoerter = suchwoerter_bilden(suchtext)
    if not suchwoerter:
        raise ValueError("Mindestens ein Suchwort außer Füllwörtern ist erforderlich.")
    treffer = []
    for abschnitt in dokumente_aufteilen(dokumentordner):
        woerter = suchwoerter_bilden(abschnitt["ueberschrift"] + " " + abschnitt["text"])
        uebereinstimmungen = sorted(suchwoerter & woerter)
        if uebereinstimmungen:
            treffer.append({**abschnitt, "uebereinstimmungen": uebereinstimmungen})
    return sorted(treffer, key=lambda treffer: (
        -len(treffer["uebereinstimmungen"]),
        treffer["dateiname"], treffer["abschnittskennung"],
    ))


def hauptprogramm():
    suchtext = " ".join(sys.argv[1:]).strip()
    if not suchtext:
        print('Aufruf: python src/suchen.py "Port 8081"', file=sys.stderr)
        return 2
    try:
        treffer = mit_quellen_suchen(suchtext)
    except (OSError, UnicodeError, ValueError) as fehler:
        print(f"Suche fehlgeschlagen: {fehler}", file=sys.stderr)
        return 2
    print(json.dumps({
        "suchtext": suchtext,
        "hinweis": ("Stichworttreffer sind Quellenhinweise, keine geprüften Antworten."
                    if treffer else "Keine Stichworttreffer in den lokalen Dokumenten."),
        "treffer": treffer,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(hauptprogramm())
