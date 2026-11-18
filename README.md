# Überprüfbarer lokaler Dokumentenassistent

Stand: 10. November 2026 — **P03-T03 wegen fehlendem nachgewiesenem Modellzugang blockiert; P03-T02 bleibt lokal geprüft abgeschlossen**. Das ursprüngliche Basisziel vom 8. November wurde verfehlt; Fortsetzungszeitraum bis 15. November. Geschätzter Basisaufwand: 4 Stunden ohne Einrichtung und Erweiterungen.

Ein Verein möchte die passende Anweisung in drei Dokumenten finden, ohne unbelegte Antworten zu erhalten.

Ergebnis: Lokale Suche mit Quellenangaben und zehn Prüffragen; LLM und MCP als getrennte Anbindungen.

Vorgesehene Technologien: Python, LLM/RAG, FastAPI, MCP, Auswertung. Eine Nennung ist kein Nachweis einer Umsetzung.

## Einstieg

1. [Lastenheft](LASTENHEFT.md) lesen.
2. [Geprüftes Suchticket](tickets/P03-T02.md) öffnen.
3. [Technischen Einstieg](START.md) prüfen und ein Ticket nach dem anderen bearbeiten.
4. [Arbeitsjournal](ARBEITSJOURNAL.md) und echte Nachweise aktualisieren.

Abhängigkeiten: keine weiteren Projekte.

## Geprüfter Stand von P03-T01

Die drei vorhandenen synthetischen Dokumente und alle zehn Prüffragen wurden unverändert kontrolliert. Acht Fragen haben erwartete Quellen mit Belegstellen; die Fragen nach Administratorkennwort und Jahresbudget sind ausdrücklich unbeantwortbar. Die Startfrage ist nur auf Anweisungsebene beantwortbar: Ein konkreter Dienstbefehl ist noch nicht dokumentiert.

[Erwartete Antworten und Belege](nachweise/P03-T01-erwartungen.json), [Prüfprotokoll](nachweise/P03-T01-konsistenz.txt) und [Abnahme](nachweise/P03-T01-abnahme.md) dokumentieren ausschließlich die Vorbereitung des Katalogs. Der lokale Konsistenzcheck ist in [START.md](START.md) beschrieben.

## Geprüfter Stand von P03-T02

Die lokale Python-Suche teilt Markdown-Dokumente an Leerzeilen und Überschriften in Absätze auf. Jeder Treffer enthält Dateiname, Abschnittskennung, Überschrift und wörtlichen Text. `Port 8081` liefert `start.md/A001` vor `support.md/A001`. Die drei vorhandenen Dokumente enthalten jeweils einen Textabsatz; mehrere Absätze und Überschriftenwechsel wurden zusätzlich mit einem synthetischen Prüftext im Prüfskript kontrolliert.

[Abnahme](nachweise/P03-T02-abnahme.md), [Prüfausgabe](nachweise/P03-T02-pruefung.txt) und [Programmaufrufe](nachweise/P03-T02-aufrufe.txt) belegen ausschließlich diese lokale Stichwortsuche. Keine Wortstammerkennung, semantische Suche, Antworterzeugung, Modell-, FastAPI- oder MCP-Anbindung. Keine Treffer sind kein Beweis für Unbeantwortbarkeit. Die übergreifenden Lastenheftkriterien A1–A4 bleiben offen. Fertigstellung ist im Journal dokumentiert; spätere Veröffentlichung und Commit übernimmt der Steuerdienst.

[Erweiterungen](VARIANTEN.md) haben einen eigenen Umsetzungsstand. [Private Unternehmenszuordnung](UNTERNEHMEN.lokal.md) bleibt außerhalb der Git-Verwaltung.

## Voraussetzung von P03-T03 geprüft

Im Projekt ist kein Modellzugang konfiguriert. Die begrenzte lokale Prüfung fand weder Modellprogramme im Suchpfad noch Modelldateien im Projekt. Die Ports 11434 und 1234 waren nicht erreichbar; Port 8080 war offen, lieferte unter `/v1/models` aber keine lesbare JSON-Modellliste. Das beweist keine allgemeine Abwesenheit installierter Modelle, bietet jedoch keine überprüfbare Grundlage für die freigegebene Anbindung.

**Offlinebetrieb: ausschließlich lokale Stichwortsuche, keine Modellantworten.** Schnittstelle, Quellenprotokoll der Modellaufrufe und Unterdrückung unbelegter Modellantworten sind weiterhin offen. Es wurde keine Ersatzsimulation erstellt. [Blockadenachweis](nachweise/P03-T03-blockade.md) und [Voraussetzungsprüfung](nachweise/P03-T03-voraussetzungen.txt). T03 ist nicht abgenommen; Lastenheft A1–A4 und die Folgephase bleiben offen.

## Projektsprache

Dokumentation, selbst gewählte Bezeichner, Kommentare, Meldungen und Beispieldaten werden auf Deutsch geschrieben. Festgelegte API-Schlüssel, Sprachsyntax und Produktnamen bleiben unverändert.

## Modellanbindung vom 17. November 2026

P03-T03 ist jetzt geprüft. Die früheren Blockaden vom 10. November bleiben Verlauf. `src/antworten.py` verwendet die vorhandene Stichwortsuche und fragt das echte lokale Modell `qwen2.5:1.5b` über Ollama ab. Das Modell liefert Quelle und wörtliches Zitat als JSON. Nur ein tatsächlich in der angegebenen Quelle vorhandenes, nicht leeres Zitat wird ausgegeben. Freie oder veränderte Texte werden unterdrückt. Ein Beleg kann trotzdem irrelevant sein: Die Schutzprüfung ersetzt keine semantische Bewertung. Keine Vektorsuche, FastAPI- oder MCP-Anbindung behauptet.

Tatsächlich geprüft: lokale Portantwort mit `start.md/A001`, unbeantwortbare Kennwortfrage, Ablehnung erfundener Zitate und expliziter Offlinebetrieb. [Modellabnahme](nachweise/P03-T03-modellabnahme.json), [Prüfskript](nachweise/P03-T03-pruefung.py). T04 und die vollständige Zehn-Fragen-Auswertung sind noch offen.
