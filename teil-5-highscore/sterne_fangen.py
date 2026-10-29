import random
from pathlib import Path

import pygame

# Ordner mit den Grafiken, Sounds und der Schrift, neben dieser Datei
ASSETS = Path(__file__).parent / "assets"
# Hier merkt sich das Spiel den Highscore
HIGHSCORE_DATEI = Path(__file__).parent / "highscore.txt"

# 1. Vorbereitung: Fenster, Uhr und zwei Schriftgrößen
pygame.init()
fenster = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sterne fangen")
uhr = pygame.time.Clock()
schrift = pygame.font.Font(ASSETS / "schrift.ttf", 32)
schrift_gross = pygame.font.Font(ASSETS / "schrift.ttf", 64)

# 2. Bilder und Sounds laden
hintergrund = pygame.image.load(ASSETS / "hintergrund.png").convert()
schiff_bild = pygame.image.load(ASSETS / "raumschiff.png").convert_alpha()
stern_bild = pygame.image.load(ASSETS / "stern.png").convert_alpha()
meteor_bild = pygame.image.load(ASSETS / "meteor.png").convert_alpha()
leben_bild = pygame.image.load(ASSETS / "leben.png").convert_alpha()
fang_ton = pygame.mixer.Sound(ASSETS / "fangen.ogg")
treffer_ton = pygame.mixer.Sound(ASSETS / "treffer.ogg")
verloren_ton = pygame.mixer.Sound(ASSETS / "verloren.ogg")


def nach_oben(rechteck):
    """Setzt ein Rechteck an eine zufällige Stelle über dem Fenster."""
    rechteck.x = random.randint(0, 800 - int(rechteck.width))
    rechteck.bottom = random.randint(-600, 0)


def text_mitte(inhalt, y, groesse):
    """Zeichnet einen weißen Text waagerecht in die Mitte des Fensters."""
    bild = groesse.render(inhalt, True, "white")
    fenster.blit(bild, bild.get_rect(center=(400, y)))


def highscore_laden():
    """Liest den Highscore aus der Datei. Gibt es noch keine, ist er 0."""
    if HIGHSCORE_DATEI.exists():
        return int(HIGHSCORE_DATEI.read_text())
    return 0


def tempo_fuer(punkte):
    """Ab 10, 25, 50 und 100 Punkten fällt alles schneller, danach bleibt es so."""
    if punkte >= 100:
        return 2.0
    if punkte >= 50:
        return 1.75
    if punkte >= 25:
        return 1.5
    if punkte >= 10:
        return 1.25
    return 1.0


# 3. Spielfiguren: Raumschiff, Listen mit Sternen und Meteoren
schiff = schiff_bild.get_frect(midbottom=(400, 580))
sterne = [stern_bild.get_frect() for _ in range(3)]
meteore = [meteor_bild.get_frect() for _ in range(4)]
punkte = 0
leben = 3
highscore = highscore_laden()
neuer_highscore = False


def neues_spiel():
    """Setzt das Raumschiff in die Mitte und alle Sterne und Meteore nach oben."""
    schiff.midbottom = (400, 580)
    for objekt in sterne + meteore:
        nach_oben(objekt)


# 4. Das Spiel startet auf dem Startbildschirm
zustand = "start"

# 5. Spielschleife: läuft, bis das Fenster geschlossen wird
laeuft = True
while laeuft:
    dt = uhr.tick(60) / 1000  # Sekunden seit dem letzten Bild

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False
        elif ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_SPACE:
            # 6. Leertaste startet ein neues Spiel, aber nicht mitten im Spiel
            if zustand != "spielen":
                punkte = 0
                leben = 3
                neuer_highscore = False
                neues_spiel()
                zustand = "spielen"

    if zustand == "spielen":
        # 7. Schwierigkeit: Das Tempo hängt von den Punkten ab
        tempo = tempo_fuer(punkte)

        # 8. Raumschiff mit den Pfeiltasten bewegen
        tasten = pygame.key.get_pressed()
        if tasten[pygame.K_LEFT]:
            schiff.x -= 400 * dt
        if tasten[pygame.K_RIGHT]:
            schiff.x += 400 * dt
        schiff.clamp_ip(fenster.get_rect())

        # 9. Alle Sterne fallen lassen und fangen
        for stern in sterne:
            stern.y += 250 * tempo * dt
            if stern.colliderect(schiff):
                punkte += 1
                fang_ton.play()
                nach_oben(stern)
            elif stern.top > 600:
                nach_oben(stern)

        # 10. Meteore fallen lassen, bei einem Treffer ein Leben abziehen
        for meteor in meteore:
            meteor.y += 200 * tempo * dt
            if meteor.top > 600:
                nach_oben(meteor)
        trefferzone = schiff.inflate(-30, -30)
        treffer = trefferzone.collidelist(meteore)
        if treffer != -1:
            leben -= 1
            nach_oben(meteore[treffer])
            if leben == 0:
                verloren_ton.play()
                zustand = "game_over"
                # 11. Neuer Highscore? Dann in die Datei schreiben
                if punkte > highscore:
                    highscore = punkte
                    neuer_highscore = True
                    HIGHSCORE_DATEI.write_text(str(highscore))
            else:
                treffer_ton.play()

    # 12. Zeichnen: Hintergrund und Raumschiff gibt es in jedem Zustand
    for x in range(0, 800, 256):
        for y in range(0, 600, 256):
            fenster.blit(hintergrund, (x, y))
    fenster.blit(schiff_bild, schiff)

    if zustand == "start":
        text_mitte("Sterne fangen", 200, schrift_gross)
        text_mitte(f"Highscore: {highscore}", 280, schrift)
        text_mitte("Pfeiltasten: lenken", 350, schrift)
        text_mitte("Leertaste: Start", 400, schrift)
    else:
        for stern in sterne:
            fenster.blit(stern_bild, stern)
        for meteor in meteore:
            fenster.blit(meteor_bild, meteor)
        text = schrift.render(f"Punkte: {punkte}", True, "white")
        fenster.blit(text, (20, 20))
        for nummer in range(leben):
            fenster.blit(leben_bild, (740 - nummer * 45, 25))

    if zustand == "game_over":
        text_mitte("Game Over", 220, schrift_gross)
        if neuer_highscore:
            text_mitte("Neuer Highscore!", 300, schrift)
        else:
            text_mitte(f"Highscore: {highscore}", 300, schrift)
        text_mitte("Leertaste: neues Spiel", 370, schrift)

    pygame.display.flip()

pygame.quit()
