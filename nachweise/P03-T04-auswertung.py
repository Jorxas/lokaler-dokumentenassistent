"""Unveränderte zehn Fragen wirklich ausführen; Fehler nicht ausblenden."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJEKT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJEKT / "src"))
from antworten import beantworten
from suchen import mit_quellen_suchen

ziel = PROJEKT / "nachweise/P03-T04-auswertung.json"
if ziel.exists() and not (PROJEKT / "nachweise/P03-T04-erster-lauf.json").exists():
    (PROJEKT / "nachweise/P03-T04-erster-lauf.json").write_bytes(ziel.read_bytes())
fragen = json.loads((PROJEKT / "beispieldaten/fragen.json").read_text(encoding="utf-8-sig"))
ergebnisse = []
for nummer, eintrag in enumerate(fragen, 1):
    frage = eintrag["frage"]
    suche = mit_quellen_suchen(frage)
    modell = beantworten(frage)
    assert modell["status"] != "offline", modell
    if modell["antwort"]:
        assert any(q["kennung"] == modell["antwort"]["quelle"]
                   and modell["antwort"]["zitat"] in q["text"] for q in modell["quellen"])
    soll = eintrag["quelle"]
    ist = modell["antwort"]["quelle"].split("/")[0] if modell["antwort"] else None
    ergebnisse.append({"nummer": nummer, "sollQuelle": soll,
                       "quellenauswahlRichtig": soll == ist,
                       "suchtreffer": [t["dateiname"] for t in suche], "modell": modell})
    print(f"Frage {nummer}/10: {modell['status']}; Sollquelle={soll}, Istquelle={ist}", flush=True)

unbeantwortbar = [e for e in ergebnisse if e["sollQuelle"] is None]
assert all(e["modell"]["antwort"] is None for e in unbeantwortbar), "Unbelegte Antwort nicht zurückgehalten."
dateien = [PROJEKT / "beispieldaten/fragen.json", *sorted((PROJEKT / "dokumente").glob("*.md"))]
ausgabe = {"zeit": datetime.now(timezone.utc).isoformat(), "fragen": len(ergebnisse),
           "richtigZugeordneteQuellen": sum(e["quellenauswahlRichtig"] for e in ergebnisse),
           "echteModellaufrufe": sum(e["modell"]["modellAufgerufen"] for e in ergebnisse),
           "unbeantwortbareFragenZurueckgehalten": len(unbeantwortbar),
           "datenpruefsummen": {str(p.relative_to(PROJEKT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dateien},
           "ergebnisse": ergebnisse,
           "grenze": "Quellenauswahl misst keine vollständige semantische Antwortqualität. Keine industrielle Übertragbarkeit. MCP nicht implementiert."}
(PROJEKT / "nachweise/P03-T04-auswertung.json").write_text(
    json.dumps(ausgabe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"AUSGEFÜHRT: {len(ergebnisse)} Fragen; {ausgabe['richtigZugeordneteQuellen']}/10 Quellenauswahlen richtig.")
