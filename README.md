# Sterne fangen

Der Code zur Blog-Reihe [„Spiele mit Pygame CE“](https://philsdevquest.de/blog/pygame-ce/) auf [philsdevquest.de](https://philsdevquest.de). Ein kleines Spiel: Du lenkst ein Raumschiff, fängst Sterne und weichst Meteoren aus.

Jeder Ordner ist der fertige Stand nach einem Teil der Reihe:

| Ordner | Teil | Beitrag |
|---|---|---|
| `teil-1-erstes-mini-spiel` | 1 | [Pygame CE: Unterschied zu Pygame und ein erstes Mini-Spiel](https://philsdevquest.de/blog/pygame-ce/) |
| `teil-2-bilder-und-sound` | 2 | [Kenney Assets in Pygame CE: Bilder und Sound einbauen](https://philsdevquest.de/blog/kenney-assets-pygame/) |
| `teil-3-kollisionen` | 3 | [Pygame Rect: Kollisionen mit vielen Objekten](https://philsdevquest.de/blog/pygame-rect-kollision/) |
| `teil-4-game-over` | 4 | [Pygame Game Over: Startbildschirm und Neustart per Taste](https://philsdevquest.de/blog/pygame-game-over/) |
| `teil-5-highscore` | 5 | [Pygame Highscore: speichern und Spiel schneller machen](https://philsdevquest.de/blog/pygame-highscore/) |
| `teil-6-im-browser` | 6 | [Pygame im Browser: Spiel mit pygbag auf itch.io bringen](https://philsdevquest.de/blog/pygame-im-browser/) |

## Starten

Getestet mit Python 3.15.0 und pygame-ce 2.5.8 auf macOS.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python teil-5-highscore/sterne_fangen.py
```

Unter Windows heißt die zweite Zeile `.venv\Scripts\activate`.

Teil 6 läuft am Rechner genauso (`python teil-6-im-browser/main.py`). Für den Browser baut ihn pygbag:

```bash
pygbag teil-6-im-browser
```

Danach im Browser `http://localhost:8000` öffnen und einmal ins Bild klicken.

## Grafiken und Töne

Alle Dateien in den Ordnern `assets` stammen aus [Space Shooter Remastered von Kenney](https://kenney.nl/assets/space-shooter-remastered) und stehen unter [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Sie wurden für das Spiel nur umbenannt.

## Lizenz

Der Code steht unter der [MIT-Lizenz](LICENSE). Die Grafiken und Töne von Kenney stehen unter CC0, siehe oben.
