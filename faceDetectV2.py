import cv2
import pygame
import numpy as np

face_cascade = cv2.CascadeClassifier('/Users/ksubram2/Documents/Data/Work/Projects/python/sandbox/haarcascade_frontalface_default.xml')

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

# Define the colors to use
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

menu_items = [
    {'label': 'Connect', 'action': lambda: start_camera(), 'rect': pygame.Rect(0, 0, 0, 0)},
    {'label': 'About', 'action': lambda: print('Designed by Karthik'), 'rect': pygame.Rect(0, 0, 0, 0)},
    {'label': 'Exit', 'action': lambda: exit(0), 'rect': pygame.Rect(0, 0, 0, 0)},
]

menu_bar_rect = pygame.Rect(0, 0, 640, 30)

x_pos = 10
for item in menu_items:
    text = font.render(item['label'], True, white)
    item['rect'] = text.get_rect()
    item['rect'].x = x_pos
    item['rect'].centery = menu_bar_rect.centery
    x_pos += item['rect'].width + 20

screen = pygame.display.set_mode((640, 480+menu_bar_rect.height))

splash = pygame.image.load('splash.png')
play_rect = pygame.Rect(200, 200, 240, 80)
play_text = font.render('PLAY', True, white)

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def show_play_button():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_rect.collidepoint(event.pos):
                        return

        screen.blit(splash, (0, 0))

        # Draw play button
        pygame.draw.rect(screen, blue, play_rect, 2)
        screen.blit(play_text, (play_rect.x + 80, play_rect.y + 25))

        # Check if mouse is hovering over button
        if play_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, blue, play_rect, 3)
            screen.blit(play_text, (play_rect.x + 80, play_rect.y + 25))
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)

        pygame.display.flip()
        clock.tick(60)

    # Start the camera
    start_camera()

show_play_button()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for item in menu_items:
                    if item['rect'].collidepoint(event.pos):
                        item['action']()

    screen.fill(white)
    pygame.draw.rect(screen, black, menu_bar_rect)

    for item in menu_items:
        text = font.render(item['label'], True, white)
        screen.blit(text, item['rect'])

    if 'cap' in globals():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                frame = np.rot90(frame, k=1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = pygame.surfarray.make_surface(frame)
                screen.blit(frame, (0, 30))
    else:
        message = font.render('Please press connect to start camera', True, black)  # change color to white
        message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(message, message_rect)


    pygame.display.flip()
    clock.tick(60)
