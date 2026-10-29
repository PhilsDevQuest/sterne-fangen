import random

import pygame

# 1. Vorbereitung: Fenster, Uhr und Schrift
pygame.init()
fenster = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sterne fangen")
uhr = pygame.time.Clock()
schrift = pygame.font.Font(None, 48)

# 2. Spielfiguren: Korb, Stern und Punktestand
korb = pygame.FRect(0, 0, 120, 20)
korb.midbottom = (400, 580)
stern = pygame.FRect(random.randint(0, 780), -20, 20, 20)
punkte = 0

# 3. Spielschleife: läuft, bis das Fenster geschlossen wird
laeuft = True
while laeuft:
    dt = uhr.tick(60) / 1000  # Sekunden seit dem letzten Bild

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            laeuft = False

    # 4. Korb mit den Pfeiltasten bewegen
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_LEFT]:
        korb.x -= 400 * dt
    if tasten[pygame.K_RIGHT]:
        korb.x += 400 * dt
    korb.clamp_ip(fenster.get_rect())

    # 5. Stern fallen lassen und fangen
    stern.y += 250 * dt
    if stern.colliderect(korb):
        punkte += 1
        stern.topleft = (random.randint(0, 780), -20)
    elif stern.top > 600:
        stern.topleft = (random.randint(0, 780), -20)

    # 6. Alles zeichnen
    fenster.fill("midnightblue")
    pygame.draw.rect(fenster, "orange", korb)
    pygame.draw.circle(fenster, "gold", stern.center, 10)
    text = schrift.render(f"Punkte: {punkte}", True, "white")
    fenster.blit(text, (20, 20))
    pygame.display.flip()

pygame.quit()
