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

# 2. Bilder und Sound laden
hintergrund = pygame.image.load(ASSETS / "hintergrund.png").convert()
schiff_bild = pygame.image.load(ASSETS / "raumschiff.png").convert_alpha()
stern_bild = pygame.image.load(ASSETS / "stern.png").convert_alpha()
fang_ton = pygame.mixer.Sound(ASSETS / "fangen.ogg")

# 3. Spielfiguren: Raumschiff, Stern und Punktestand
schiff = schiff_bild.get_frect(midbottom=(400, 580))
stern = stern_bild.get_frect(topleft=(random.randint(0, 770), -30))
punkte = 0

# 4. Spielschleife: läuft, bis das Fenster geschlossen wird
laeuft = True
while laeuft:
    dt = uhr.tick(60) / 1000  # Sekunden seit dem letzten Bild

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

    # 5. Raumschiff mit den Pfeiltasten bewegen
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_LEFT]:
        schiff.x -= 400 * dt
    if tasten[pygame.K_RIGHT]:
        schiff.x += 400 * dt
    schiff.clamp_ip(fenster.get_rect())

    # 6. Stern fallen lassen und fangen
    stern.y += 250 * dt
    if stern.colliderect(schiff):
        punkte += 1
        fang_ton.play()
        stern.topleft = (random.randint(0, 770), -30)
    elif stern.top > 600:
        stern.topleft = (random.randint(0, 770), -30)

    # 7. Alles zeichnen: Hintergrund als Kacheln, dann Schiff, Stern und Punkte
    for x in range(0, 800, 256):
        for y in range(0, 600, 256):
            fenster.blit(hintergrund, (x, y))
    fenster.blit(schiff_bild, schiff)
    fenster.blit(stern_bild, stern)
    text = schrift.render(f"Punkte: {punkte}", True, "white")
    fenster.blit(text, (20, 20))
    pygame.display.flip()

pygame.quit()
