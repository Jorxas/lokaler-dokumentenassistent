"""Begrenzte lokale Voraussetzungskontrolle; keine Modell- oder Antwortabnahme."""
import hashlib
import json
import os
import platform
import shutil
import socket
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

PROJEKTORDNER = Path(__file__).resolve().parents[1]


def pruefen():
    print(f"Prüfzeitpunkt: {datetime.now().astimezone().isoformat(timespec='seconds')}")
    print(f"Python: {platform.python_version()}")
    konfiguration = json.loads((PROJEKTORDNER / "projekt.json").read_text(encoding="utf-8-sig"))
    # Nur Feldnamen zeigen, keine Zugangsdaten oder Umgebungswerte ausgeben.
    modellfelder = [name for name in konfiguration if any(
        wort in name.casefold() for wort in ("modell", "model", "llm", "endpoint", "endpunkt")
    )]
    print(f"Modellbezogene Konfigurationsfelder: {modellfelder}")
    for programm in ("ollama", "llama-cli", "llama-server", "lms"):
        print(f"Programm {programm} im Suchpfad: {'ja' if shutil.which(programm) else 'nein'}")
    for name in ("OLLAMA_HOST", "OLLAMA_MODELS", "OPENAI_BASE_URL", "OPENAI_API_KEY",
                 "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "LLM_MODEL", "MODEL_PATH"):
        print(f"Umgebungsvariable {name} gesetzt: {'ja' if os.environ.get(name) else 'nein'}")
    for port in (11434, 1234, 8080):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                print(f"TCP 127.0.0.1:{port}: erreichbar; Modellverfügbarkeit damit noch nicht belegt")
        except OSError as fehler:
            print(f"TCP 127.0.0.1:{port}: nicht erreichbar ({type(fehler).__name__}, Fehlercode {fehler.errno})")
            continue
        # Ein offener Port kann ein anderer Dienst sein. Keine Proxys oder Weiterleitungen.
        class OhneWeiterleitung(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        zugang = urllib.request.build_opener(urllib.request.ProxyHandler({}), OhneWeiterleitung())
        pfad = "/api/tags" if port == 11434 else "/v1/models"
        try:
            with zugang.open(f"http://127.0.0.1:{port}{pfad}", timeout=2) as antwort:
                inhalt = antwort.read(65537)
                if len(inhalt) > 65536:
                    print(f"Modellliste Port {port}: Antwort zu groß; nicht ausgewertet")
                    continue
                daten = json.loads(inhalt)
                modelle = daten.get("models" if port == 11434 else "data") if isinstance(daten, dict) else None
                print(f"Modellliste Port {port}: " + (
                    f"{len(modelle)} Einträge; gesonderte Modellprüfung erforderlich"
                    if isinstance(modelle, list) else "keine erwartete Modelllistenstruktur"))
        except urllib.error.HTTPError as fehler:
            print(f"Modellliste Port {port}: HTTP {fehler.code}; keine Modellliste erhalten")
        except (OSError, ValueError) as fehler:
            print(f"Modellliste Port {port}: nicht lesbar ({type(fehler).__name__})")
    # Ausschließlich Projektordner durchsuchen; keine privaten Listen oder fremden Caches.
    modelldateien = sorted(pfad.relative_to(PROJEKTORDNER).as_posix()
                          for pfad in PROJEKTORDNER.rglob("*")
                          if pfad.is_file() and pfad.suffix.casefold() in (".gguf", ".safetensors"))
    print(f"Modelldateien .gguf/.safetensors im Projekt: {modelldateien}")
    dokumente = sorted((PROJEKTORDNER / "dokumente").glob("*.md"))
    fragenpfad = PROJEKTORDNER / "beispieldaten/fragen.json"
    fragen = json.loads(fragenpfad.read_text(encoding="utf-8-sig"))
    assert len(dokumente) == 3 and len(fragen) == 10
    vorheriges_protokoll = (PROJEKTORDNER / "nachweise/P03-T01-konsistenz.txt").read_text(encoding="utf-8-sig")
    for pfad in [*dokumente, fragenpfad]:
        zeile = f"SHA256 {pfad.relative_to(PROJEKTORDNER).as_posix()}: {hashlib.sha256(pfad.read_bytes()).hexdigest()}"
        assert zeile in vorheriges_protokoll
        print(zeile)
    print("BESTANDEN: 3 synthetische Dokumente und 10 Prüffragen unverändert.")
    print("Grenze: begrenzte Voraussetzungskontrolle, keine vollständige Rechnersuche.")
    print("Kein Modellaufruf, keine Antworterzeugung oder Zehn-Fragen-Auswertung ausgeführt.")
    print("Code 0 bedeutet erfolgreiche Voraussetzungskontrolle, keine erfolgreiche T03-Abnahme.")
    return 0


if __name__ == "__main__":
    raise SystemExit(pruefen())
