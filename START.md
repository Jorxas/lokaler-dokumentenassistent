# Technischer Einstieg — P03

## P03-T01 lokal nachprüfen

Im Projektordner ausführen:

~~~powershell
uv run --offline --python 3.12 python -X utf8 nachweise/P03-T01-konsistenz.py
~~~

Im bereits eingerichteten lokalen Ausgabe-/Cachekontext ausführen. Der Check benötigt nur die Python-Standardbibliothek. Die tatsächlich verwendete Python-Version steht im [Prüfprotokoll](nachweise/P03-T01-konsistenz.txt).

Erwartet: drei nicht leere Dokumente, zehn verschiedene Fragen, acht passende Quellenbelege und zwei ausdrücklich unbeantwortbare Fragen. Bei Widersprüchen endet der Check mit Fehlercode 1, bei Erfolg mit 0. Er gleicht den unveränderten Katalog mit den separat dokumentierten Erwartungen ab. Die inhaltliche Kontrolle der erwarteten Antworten steht in der [Abnahme](nachweise/P03-T01-abnahme.md); sie wird durch den Textabgleich nicht automatisiert ersetzt.

## Einstiegspunkt ausführen

Voraussetzungen: Python 3; Lokales Modell oder API-Zugang nur für die generative Variante.

~~~powershell
uv run --offline --python 3.12 python -X utf8 src/suchen.py
~~~

Das Startprogramm meldet den Initialisierungsstand. Fachfunktionen sind bewusst noch nicht implementiert und melden dies bei einem Aufruf. Fehlende Bibliotheken und Frameworks erst im passenden Ticket mit ihrer tatsächlichen Version ergänzen.

## Abgrenzung und spätere Aufgabe

P03-T01 endet mit dem geprüften Dokumenten- und Fragenkatalog. Die Startanweisung unter dokumente/start.md verweist auf einen späteren Dienstbefehl, ohne ihn vorzugeben. Daraus keinen lauffähigen Dienst ableiten. Suche mit Quellen gehört zu P03-T02 und wird in dieser Arbeitseinheit nicht begonnen. Modell und MCP benötigen eigene spätere Nachweise.

## Technische Quellen

- [Python-CSV-Modul](https://docs.python.org/3/library/csv.html)
- [Offizielle Angular-CLI-Anleitung](https://angular.dev/tools/cli/setup-local)
- [WPF mit .NET](https://learn.microsoft.com/de-de/dotnet/desktop/wpf/get-started/create-app-visual-studio)

Vor dem Einbinden eines Frameworks dessen aktuelle offizielle Anleitung lesen.
