# Technischer Einstieg — P03

## P03-T01 lokal nachprüfen

Im Projektordner ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/P03-T01-konsistenz.py
~~~

Im bereits eingerichteten lokalen Ausgabe-/Cachekontext ausführen. Der Check benötigt nur die Python-Standardbibliothek. Die tatsächlich verwendete Python-Version steht im [Prüfprotokoll](nachweise/P03-T01-konsistenz.txt).

Erwartet: drei nicht leere Dokumente, zehn verschiedene Fragen, acht passende Quellenbelege und zwei ausdrücklich unbeantwortbare Fragen. Bei Widersprüchen endet der Check mit Fehlercode 1, bei Erfolg mit 0. Er gleicht den unveränderten Katalog mit den separat dokumentierten Erwartungen ab. Die inhaltliche Kontrolle der erwarteten Antworten steht in der [Abnahme](nachweise/P03-T01-abnahme.md); sie wird durch den Textabgleich nicht automatisiert ersetzt.

## Lokale Suche ausführen — P03-T02

Voraussetzung: vorhandenes Python 3.12 über uv, ausschließlich Standardbibliothek. Kein Modell, Konto oder Netzwerkzugang erforderlich. Alle Befehle im Projektordner und mit dem vorhandenen lokalen Cachekontext ausführen.

~~~powershell
uv run --offline --python 3.12 python -X utf8 src/suchen.py "Port 8081"
uv run --offline --python 3.12 python -X utf8 src/suchen.py "Administratorkennwort"
uv run --offline --python 3.12 python -X utf8 src/suchen.py "?!"
~~~

Erwartet: zuerst zwei JSON-Treffer, `start.md/A001` vor `support.md/A001`, mit wörtlichem Text und übereinstimmenden Wörtern; danach eine leere Trefferliste mit Hinweis. Beide Aufrufe enden mit Code 0. Der dritte Aufruf liefert eine deutsche Eingabefehlermeldung und Code 2. Ohne Suchtext erscheint der Aufrufhinweis mit Code 2. Tatsächliche Ausgaben: [Programmaufrufe](nachweise/P03-T02-aufrufe.txt).

Ein Abschnitt ist ein nicht leerer Textabsatz. Leerzeilen und Markdown-Überschriften beginnen einen neuen Absatz; die letzte Überschrift wird als Kontext gespeichert. Die Kennungen `A001`, `A002` usw. zählen pro Datei in Dokumentreihenfolge. Zusammen mit dem Dateinamen sind sie eindeutig. Sie bleiben bei unverändertem Dokument stabil; eingefügte Absätze können spätere Kennungen verschieben. Den Treffertext zum Nachschlagen im Original verwenden.

Suchwörter werden ohne Beachtung der Großschreibung abgeglichen, einige deutsche Füllwörter werden entfernt. Ein gemeinsames Wort im Text oder seiner Überschrift reicht für einen Treffer. Mehr gemeinsame Wörter stehen zuerst, Gleichstände werden nach Dateiname und Kennung sortiert. Es gibt keine Wortstamm- oder Synonymerkennung: `Protokolle` findet beispielsweise nicht automatisch `Demoprotokolle`. Treffer liefern keine geprüfte Antwort; keine Treffer beweisen keine Unbeantwortbarkeit.

## Kleinste lokale Abnahme für P03-T02

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/P03-T02-pruefung.py
~~~

Erwartet: Code 0, drei unveränderte Originaldokumente, zehn unveränderte Fragen, referenzierbare wörtliche Treffer aus allen drei Dateien, Rangfolge, Großschreibung, leere Trefferliste und abgewiesene ungültige Suchtexte. Zusätzlich prüft ein synthetischer Text mehrere Absätze, mehrzeiligen Inhalt und Überschriftenwechsel ohne neue Beispieldateien. Beobachtete Version: Python 3.12.14. [Prüfausgabe](nachweise/P03-T02-pruefung.txt) und [Abnahme](nachweise/P03-T02-abnahme.md).

## Abgrenzung und spätere Aufgabe

P03-T02 endet mit der lokal geprüften Suche und Quellenkennungen. Die Startanweisung unter dokumente/start.md verweist weiterhin auf einen späteren Dienstbefehl, ohne ihn vorzugeben. Die Suche startet keinen Dienst und öffnet keinen Port. Die zehn Prüffragen wurden erhalten, aber hier nicht als vollständige Antwortauswertung ausgeführt. Modell, Unterdrückung unbelegter Antworten und MCP benötigen eigene spätere Nachweise. Lastenheft A1–A4 bleiben offen.

## P03-T03 — fehlende Modellvoraussetzung nachprüfen

Status am 10. November 2026: blockiert, keine Modellanbindung umgesetzt. Der verfügbare Offlinebetrieb bleibt die oben beschriebene Stichwortsuche; sie erzeugt keine Antworten und belegt keine generative Produktverwendung.

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/P03-T03-voraussetzungen.py
~~~

Der Check nutzt nur die Standardbibliothek: Konfigurationsfeldnamen, Verfügbarkeit ausgewählter Programme und Umgebungsvariablen (ohne Werte), lokale TCP-Ports 11434/1234/8080 und bei offenem Port eine begrenzte Modelllistenabfrage ohne Proxy oder Weiterleitung. Modelldateien werden nur innerhalb dieses Projekts gesucht. Drei Dokumente und zehn Fragen werden mit den T01-Prüfsummen abgeglichen. Code 0 bestätigt die Ausführung dieser Kontrolle, keine Modellverfügbarkeit oder T03-Abnahme. Ergebnisse sind rechner- und zeitabhängig; keine vollständige Rechnersuche.

Wiederaufnahme benötigt ein tatsächlich verfügbares, kostenfrei nutzbares lokales Modell mit benanntem Aufrufweg oder einen ausdrücklich freigegebenen vorhandenen Zugang. Es wurde nichts heruntergeladen, installiert oder als Modell simuliert. [Befund und benötigte Prüfdateien](nachweise/P03-T03-blockade.md). Die vollständige Auswertung der zehn Fragen und spätere Varianten wurden nicht vorweggenommen.

## Technische Quellen (bisheriger Stand)

- [Python-CSV-Modul](https://docs.python.org/3/library/csv.html)
- [Offizielle Angular-CLI-Anleitung](https://angular.dev/tools/cli/setup-local)
- [WPF mit .NET](https://learn.microsoft.com/de-de/dotnet/desktop/wpf/get-started/create-app-visual-studio)

Vor dem Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.

## Modellanbindung vom 17. November 2026

P03-T03 ist jetzt geprüft. Die früheren Blockaden vom 10. November bleiben Verlauf. `src/antworten.py` verwendet die vorhandene Stichwortsuche und fragt das echte lokale Modell `qwen2.5:1.5b` über Ollama ab. Das Modell liefert Quelle und wörtliches Zitat als JSON. Nur ein tatsächlich in der angegebenen Quelle vorhandenes, nicht leeres Zitat wird ausgegeben. Freie oder veränderte Texte werden unterdrückt. Ein Beleg kann trotzdem irrelevant sein: Die Schutzprüfung ersetzt keine semantische Bewertung. Keine Vektorsuche, FastAPI- oder MCP-Anbindung behauptet.

Voraussetzungen: laufendes Ollama unter `127.0.0.1:11434`, installiertes `qwen2.5:1.5b`, Python 3.12. Keine zusätzlichen Python-Pakete. CPU-Einstellungen sind im Aufruf festgelegt: zwei Threads, kein GPU-Einsatz, Kontext 2048 Token. Der erste allgemeine Installationsprobelauf mit Standardbeschleunigung überschritt den Zeitrahmen; der CPU-Probelauf war erfolgreich.

~~~powershell
uv run --offline --python 3.12 python -X utf8 src/antworten.py "Welchen Port verwendet die Demo?"
uv run --offline --python 3.12 python -X utf8 src/antworten.py "Wie lautet das Administratorkennwort?"
uv run --offline --python 3.12 python -X utf8 src/antworten.py "Port 8081" --ohne-modell
uv run --offline --python 3.12 python -X utf8 nachweise/P03-T03-pruefung.py
~~~

Die strukturierte Ausgabe protokolliert Frage, Zeitpunkt, Modell, verwendete Quellen, rohen Modellvorschlag und geprüften Beleg. Kein dauerndes Mitschreiben privater Fragen. HTTP-Ziel ist fest lokal; keine Proxys oder Weiterleitungen. Zeitlimit 90 Sekunden, begrenzte Antwortgröße. Bei fehlendem Modell nur Stichworttreffer und Status `offline`; es gibt keine simulierte Modellantwort. Kontrollierte Modellfehler im Prüfskript testen nur den Schutz. Der zusätzliche echte Aufruf in derselben Prüfung muss erfolgreich sein.

Gelesene Primärquellen: [Ollama Generate](https://docs.ollama.com/api/generate), [strukturierte Ausgaben](https://docs.ollama.com/capabilities/structured-outputs).
