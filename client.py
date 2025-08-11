import socket
import json
from collections import namedtuple
import pygame


#if __name__ == '__main__':
pygame.init()
screen = pygame.display.set_mode((500, 350))
pygame.display.set_caption("Record Inputs")
clock = pygame.time.Clock()

start_pos = pygame.Vector2(250, 75)
player_pos = start_pos.copy()
speed = 3
bg = pygame.image.load("")
bg = pygame.transform.smoothscale(bg, screen.get_size())

KEYMAP = {
    pygame.K_w: "w",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
}
FrameInput = namedtuple("FrameInput", ["keys"])

inputs_log = []
recording = True


def apply_inputs(keys_list, pos):
    if "w" in keys_list: pos.y -= speed
    if "s" in keys_list: pos.y += speed
    if "a" in keys_list: pos.x -= speed
    if "d" in keys_list: pos.x += speed


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if recording and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            recording = False
            running = False  # stop after pressing Enter

    pressed = pygame.key.get_pressed()
    keys_this_frame = [label for k, label in KEYMAP.items() if pressed[k]]
    apply_inputs(keys_this_frame, player_pos)
    inputs_log.append(FrameInput(keys_this_frame))

    screen.fill((18, 18, 24))
    screen.blit(bg, (0, 0))
    pygame.draw.circle(screen, (235, 90, 90), (int(player_pos.x), int(player_pos.y)), 10)

    font = pygame.font.Font(None, 24)
    screen.blit(font.render("RECORDING — press Enter to stop", True, (220, 220, 220)), (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# Save to JSON
with open("inputs_log.json", "w") as f:
    json.dump([fi.keys for fi in inputs_log], f)
print("Inputs saved to inputs_log.json")

""" client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(('', 60001))
client.connect(('0.0.0.0', 60000))
with open('inputs_log.json','r') as file:
    json_bytes = file.read().encode("utf-8")

#client.sendall(len(json_bytes))
client.sendall(json_bytes)"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind(('', 60001))
# Connect to the server (replace with server's IP or '127.0.0.1' for local)
client.connect(('127.0.0.1', 60000))

# Read the JSON file into bytes
with open('inputs_log.json', 'rb') as file:
   json_bytes = file.read()

# Send the JSON data
client.sendall(json_bytes)

# Close the connection to signal EOF
client.close()