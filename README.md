# Überprüfbarer lokaler Dokumentenassistent

Stand: 1. November 2026 — **P03-T01 geprüft abgeschlossen; Fachfunktionen noch umzusetzen**. Geplanter Abschluss der Basis: 2026-11-03, spätestens 8. November 2026. Geschätzter Basisaufwand: 4 Stunden ohne Einrichtung und Erweiterungen.

Ein Verein möchte die passende Anweisung in drei Dokumenten finden, ohne unbelegte Antworten zu erhalten.

Ergebnis: Lokale Suche mit Quellenangaben und zehn Prüffragen; LLM und MCP als getrennte Anbindungen.

Vorgesehene Technologien: Python, LLM/RAG, FastAPI, MCP, Auswertung. Eine Nennung ist kein Nachweis einer Umsetzung.

## Einstieg

1. [Lastenheft](LASTENHEFT.md) lesen.
2. [Erstes Ticket](tickets/P03-T01.md) öffnen.
3. [Technischen Einstieg](START.md) prüfen und ein Ticket nach dem anderen bearbeiten.
4. [Arbeitsjournal](ARBEITSJOURNAL.md) und echte Nachweise aktualisieren.

Abhängigkeiten: keine weiteren Projekte.

## Geprüfter Stand von P03-T01

Die drei vorhandenen synthetischen Dokumente und alle zehn Prüffragen wurden unverändert kontrolliert. Acht Fragen haben erwartete Quellen mit Belegstellen; die Fragen nach Administratorkennwort und Jahresbudget sind ausdrücklich unbeantwortbar. Die Startfrage ist nur auf Anweisungsebene beantwortbar: Ein konkreter Dienstbefehl ist noch nicht dokumentiert.

[Erwartete Antworten und Belege](nachweise/P03-T01-erwartungen.json), [Prüfprotokoll](nachweise/P03-T01-konsistenz.txt) und [Abnahme](nachweise/P03-T01-abnahme.md) dokumentieren ausschließlich die Vorbereitung des Katalogs. Der lokale Konsistenzcheck ist in [START.md](START.md) beschrieben. Suche, Modell und MCP sind noch nicht umgesetzt; die übergreifenden Lastenheftkriterien A1–A4 bleiben offen. Fertigstellung und spätere Veröffentlichung durch den Steuerdienst werden getrennt dokumentiert.

[Erweiterungen](VARIANTEN.md) haben einen eigenen Umsetzungsstand. [Private Unternehmenszuordnung](UNTERNEHMEN.lokal.md) bleibt außerhalb der Git-Verwaltung.

## Projektsprache

Dokumentation, selbst gewählte Bezeichner, Kommentare, Meldungen und Beispieldaten werden auf Deutsch geschrieben. Festgelegte API-Schlüssel, Sprachsyntax und Produktnamen bleiben unverändert.
