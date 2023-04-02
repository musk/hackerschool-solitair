# Solitair
Bei diesem Projekt handelt es sich um das Spiel Solitair. Das Projekt ist als Basis für einen Pythonkurs für die Hackerschool (https://hacker-school.de)  gedacht um das Konzept von Klassen und Objekten näher zu bringen.

Das Spiel nutzt Python 3.9 und lediglich die Standardpythonbibliotheken um die Abhängigkeiten auf ein Minimum zu halten. Es nutzt ein standard Terminal um das Spielfeld zu zeichnen. 
Alle notwendigen Klassen werden mit dem Spiel geliefert. 

Um das Spiel zu starten führen sie
```shell
python solitair.py
```
aus

## Spielregeln
Die Spielregeln kannst du unter [SPIELREGELN.md](SPIELREGELN.md) nachlesen. 

## Struktur
Der Code ist in 3 Module aufgeteilt:
* solitair.py - beinhaltet die Hautpklasse des Spiels und den einstiegs Punkt um das Spiel zu starten.
* cards.py - beinhaltet alle Klassen rundum Karten und Stapeln.
* ascii.py - beinhaltet alle Klassen rundum die grafische Darstellung .

Zusätzlich gibt es noch Klassen zum testen der Funktionalität:
* cards_test.py - alle Unit Tests für das cards.py Modul
* solitair_test.py - Unit Test für das solitair.py Modul



