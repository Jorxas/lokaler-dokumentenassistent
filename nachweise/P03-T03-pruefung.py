"""Antwortschutz separat prüfen; danach echten lokalen Modellaufruf ausführen."""
import json
import sys
from pathlib import Path
from urllib.error import URLError

PROJEKT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJEKT / "src"))
from antworten import beantworten, beleg_pruefen

quellen = [{"kennung": "start.md/A001", "text": "Die Demo verwendet Port 8081."}]
assert beleg_pruefen({"quelle": "start.md/A001", "zitat": "Port 8081"}, quellen)
for falsch in [None, [], {"quelle": "fremd", "zitat": "Port 8081"},
               {"quelle": "start.md/A001", "zitat": "Port 9999"},
               {"quelle": "start.md/A001", "zitat": ""},
               {"quelle": "start.md/A001", "zitat": 8081}]:
    assert beleg_pruefen(falsch, quellen) is None


def unerreichbar(frage, quellen):
    raise URLError("Absichtlich nicht verfügbarer Prüfdienst")


def erfunden(frage, quellen):
    return {"vorschlag": {"quelle": quellen[0]["kennung"], "zitat": "Erfundene Antwort"}}


assert beantworten("Port 8081", modellfunktion=unerreichbar)["status"] == "offline"
assert beantworten("Port 8081", modellfunktion=erfunden)["antwort"] is None
assert beantworten("Port 8081", ohne_modell=True)["modellAufgerufen"] is False
ohne_beleg = beantworten("Wie lautet das Administratorkennwort?")
assert ohne_beleg["status"] == "unbeantwortbar" and ohne_beleg["antwort"] is None
assert ohne_beleg["modellAufgerufen"] is False
echt = beantworten("Welchen Port verwendet die Demo?")
assert echt["modellAufgerufen"] and echt["status"] == "belegt", echt
assert echt["antwort"]["quelle"] == "start.md/A001", echt
assert "8081" in echt["antwort"]["zitat"], echt
protokoll = {"schutzpruefungen": "bestanden; kontrollierte Fehler sind ausschließlich Testfälle",
             "echterModellaufruf": echt, "ohneBeleg": ohne_beleg}
(PROJEKT / "nachweise/P03-T03-modellabnahme.json").write_text(
    json.dumps(protokoll, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("BESTANDEN: Antwortschutz, Offlinebetrieb, echte lokale Portantwort und unbeantwortbare Frage.")
