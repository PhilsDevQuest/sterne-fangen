import random
from pathlib import Path

import pygame

# Ordner mit den Grafiken, Sounds und der Schrift, neben dieser Datei
ASSETS = Path(__file__).parent / "assets"

# 1. Vorbereitung: Fenster, Uhr und Schrift
pygame.init()
fenster = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sterne fangen")
uhr = pygame.time.Clock()
schrift = pygame.font.Font(ASSETS / "schrift.ttf", 32)

# 2. Bilder und Sounds laden
hintergrund = pygame.image.load(ASSETS / "hintergrund.png").convert()
schiff_bild = pygame.image.load(ASSETS / "raumschiff.png").convert_alpha()
stern_bild = pygame.image.load(ASSETS / "stern.png").convert_alpha()
meteor_bild = pygame.image.load(ASSETS / "meteor.png").convert_alpha()
leben_bild = pygame.image.load(ASSETS / "leben.png").convert_alpha()
fang_ton = pygame.mixer.Sound(ASSETS / "fangen.ogg")
treffer_ton = pygame.mixer.Sound(ASSETS / "treffer.ogg")


def nach_oben(rechteck):
    """Setzt ein Rechteck an eine zufällige Stelle über dem Fenster."""
    rechteck.x = random.randint(0, 800 - int(rechteck.width))
    rechteck.bottom = random.randint(-600, 0)


# 3. Spielfiguren: Raumschiff, Listen mit Sternen und Meteoren, Punkte und Leben
schiff = schiff_bild.get_frect(midbottom=(400, 580))
sterne = [stern_bild.get_frect() for _ in range(3)]
meteore = [meteor_bild.get_frect() for _ in range(4)]
for objekt in sterne + meteore:
    nach_oben(objekt)
punkte = 0
leben = 3

# 4. Spielschleife: läuft, bis das Fenster geschlossen wird
laeuft = True
while laeuft:
    dt = uhr.tick(60) / 1000  # Sekunden seit dem letzten Bild

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

    if leben > 0:
        # 5. Raumschiff mit den Pfeiltasten bewegen
        tasten = pygame.key.get_pressed()
        if tasten[pygame.K_LEFT]:
            schiff.x -= 400 * dt
        if tasten[pygame.K_RIGHT]:
            schiff.x += 400 * dt
        schiff.clamp_ip(fenster.get_rect())

        # 6. Alle Sterne fallen lassen und fangen
        for stern in sterne:
            stern.y += 250 * dt
            if stern.colliderect(schiff):
                punkte += 1
                fang_ton.play()
                nach_oben(stern)
            elif stern.top > 600:
                nach_oben(stern)

        # 7. Meteore fallen lassen und prüfen, ob einer das Schiff trifft
        for meteor in meteore:
            meteor.y += 200 * dt
            if meteor.top > 600:
                nach_oben(meteor)
        trefferzone = schiff.inflate(-30, -30)
        treffer = trefferzone.collidelist(meteore)
        if treffer != -1:
            leben -= 1
            treffer_ton.play()
            nach_oben(meteore[treffer])

    # 8. Alles zeichnen
    for x in range(0, 800, 256):
        for y in range(0, 600, 256):
            fenster.blit(hintergrund, (x, y))
    fenster.blit(schiff_bild, schiff)
    for stern in sterne:
        fenster.blit(stern_bild, stern)
    for meteor in meteore:
        fenster.blit(meteor_bild, meteor)
    text = schrift.render(f"Punkte: {punkte}", True, "white")
    fenster.blit(text, (20, 20))
    for nummer in range(leben):
        fenster.blit(leben_bild, (740 - nummer * 45, 25))
    if leben == 0:
        ende = schrift.render("Game Over", True, "white")
        fenster.blit(ende, ende.get_rect(center=(400, 300)))
    pygame.display.flip()

pygame.quit()
