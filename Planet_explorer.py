import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# -------------------- OpenGL Utility --------------------
def load_texture(filename):
    # Load the image with per-pixel alpha and flip it vertically
    textureSurface = pygame.image.load(filename).convert_alpha()
    textureSurface = pygame.transform.flip(textureSurface, False, True)
    width, height = textureSurface.get_rect().size

    # Convert surface to string in RGBA format
    textureData = pygame.image.tostring(textureSurface, "RGBA", True)

    # Generate and bind a texture ID
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    
    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Create the texture with RGBA data
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    return textureID

# -------------------- Improved Home Screen --------------------
def home_screen(planets):
    # Set display mode to 2D
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Planet Explorer")
    font_title = pygame.font.SysFont("Arial", 48)
    font_button = pygame.font.SysFont("Arial", 28)
    font_instr = pygame.font.SysFont("Arial", 24)
    
    # Load thumbnails for each planet (scale to thumbnail size)
    thumbnail_size = (150, 150)
    for planet in planets:
        image = pygame.image.load(planet["texture"]).convert_alpha()
        thumbnail = pygame.transform.smoothscale(image, thumbnail_size)
        planet["thumbnail"] = thumbnail

    # Calculate layout: center thumbnails horizontally
    num_planets = len(planets)
    margin = 50
    total_width = num_planets * thumbnail_size[0] + (num_planets - 1) * margin
    start_x = (800 - total_width) // 2
    y = 250  # Vertical position for thumbnails
    for i, planet in enumerate(planets):
        x = start_x + i * (thumbnail_size[0] + margin)
        rect = pygame.Rect(x, y, thumbnail_size[0], thumbnail_size[1])
        planet["rect"] = rect

    # Main loop for home screen
    while True:
        screen.fill((10, 10, 40))  # Dark blue background

        # Draw Title and Instructions
        title_surf = font_title.render("Planet Explorer", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(400, 100))
        screen.blit(title_surf, title_rect)

        instr_surf = font_instr.render("Click a planet to explore", True, (200, 200, 200))
        instr_rect = instr_surf.get_rect(center=(400, 170))
        screen.blit(instr_surf, instr_rect)

        # Draw each planet thumbnail with a border and label
        mouse_pos = pygame.mouse.get_pos()
        for planet in planets:
            rect = planet["rect"]
            # Highlight border on hover
            if rect.collidepoint(mouse_pos):
                border_color = (255, 255, 0)
            else:
                border_color = (255, 255, 255)
            pygame.draw.rect(screen, border_color, rect, 3)
            screen.blit(planet["thumbnail"], rect)

            label_surf = font_button.render(planet["name"], True, (255, 255, 255))
            label_rect = label_surf.get_rect(center=(rect.centerx, rect.bottom + 20))
            screen.blit(label_surf, label_rect)

        pygame.display.flip()

        # Event handling for clicks and quitting
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = event.pos
                for planet in planets:
                    if planet["rect"].collidepoint(pos):
                        return planet  # Return the selected planet
        pygame.time.wait(10)

# -------------------- 3D Planet View --------------------
def planet_view(planet):
    # Reinitialize display mode with OpenGL
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Viewing " + planet["name"])
    
    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
    # Load the planet texture and create a quadric sphere
    texture = load_texture(planet["texture"])
    sphere = gluNewQuadric()
    gluQuadricTexture(sphere, GL_TRUE)
    
    # Rotation and zoom control variables
    rotate_x, rotate_y = 0, 0
    mouse_down = False
    last_mouse_pos = (0, 0)
    zoom = -8  # Initial zoom level
    MIN_ZOOM = -20  # Maximum zoom out
    MAX_ZOOM = -3   # Maximum zoom in
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Press ESC to return to home screen
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button for rotation
                    mouse_down = True
                    last_mouse_pos = event.pos
                elif event.button == 4:  # Scroll up to zoom in
                    zoom = min(zoom + 1, MAX_ZOOM)
                elif event.button == 5:  # Scroll down to zoom out
                    zoom = max(zoom - 1, MIN_ZOOM)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            if event.type == MOUSEMOTION and mouse_down:
                x, y = event.pos
                dx = x - last_mouse_pos[0]
                dy = y - last_mouse_pos[1]
                rotate_y += dx * 0.5  # Rotate around y-axis
                rotate_x += dy * 0.5  # Rotate around x-axis
                last_mouse_pos = (x, y)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply zoom and rotations
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        
        # Bind texture and draw the sphere
        glBindTexture(GL_TEXTURE_2D, texture)
        gluSphere(sphere, 2, 50, 50)
        
        pygame.display.flip()
        clock.tick(60)

# -------------------- Main Application --------------------
def main():
    pygame.init()
    
    # List of planets with their display names and texture filenames.
    planets = [
      {"name": "Earth", "texture": "textures/earth.jpg"},
      {"name": "Mars", "texture": "textures/mars.jpg"}
    ]


    
    while True:
        # Show enhanced home UI and wait for user to select a planet
        selected_planet = home_screen(planets)
        # Switch to planet view for the selected planet
        planet_view(selected_planet)

if __name__ == '__main__':
    main()
