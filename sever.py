import socket
import pygame
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('00000',60000))
s.listen(1)
print("server is listening on port 60000...")

s_client , client_address = s.accept()
print("waiting")


print(f"connection from {client_address}") # gives ip address and port of the connected client

data = b""
while True:
    chunk = s_client.recv(4096)
    if not chunk:  # No more data did this cause TCP you know
        break
    data += chunk

# Decode JSON
try:
    payload = json.loads(data.decode("utf-8"))
    #print("Received JSON:", payload)
except json.JSONDecodeError as e:
    print("Invalid JSON received:", e)


pygame.init()
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("Replay Inputs")
clock = pygame.time.Clock()

start_pos = pygame.Vector2(250, 75)
player_pos = start_pos.copy()
speed = 3
bg = pygame.image.load("")
bg = pygame.transform.smoothscale(bg, screen.get_size())
# Load inputs from JSON
with open("inputs_log.json", "r") as f:
    inputs_log = json.load(f)


def apply_inputs(keys_list, pos):
    if "w" in keys_list: pos.y -= speed
    if "s" in keys_list: pos.y += speed
    if "a" in keys_list: pos.x -= speed
    if "d" in keys_list: pos.x += speed


frame = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame < len(inputs_log):
        apply_inputs(inputs_log[frame], player_pos)
        frame += 1
    else:
        running = False  # end replay

    screen.fill((18, 18, 24))
    screen.blit(bg, (0, 0))
    pygame.draw.circle(screen, (90, 200, 255), (int(player_pos.x), int(player_pos.y)), 10)

    font = pygame.font.Font(None, 24)
    screen.blit(font.render("REPLAYING", True, (220, 220, 220)), (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

s.close()