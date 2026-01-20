import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- REPRESENTASI OBJEK 3D (Nomor 1 & 5) ---
# Karena menggunakan asset luar (mobiltank.png), kita merepresentasikannya 
# dalam bentuk Plane 3D yang bertekstur agar transformasi 3D terlihat jelas.
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = ((0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7))

def LoadTexture():
    textureSurface = pygame.image.load('mobiltank.png')
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return texid

def TankModel():
    # --- NOMOR 1: Representasi Polygon & NOMOR 4: Warna/Tekstur ---
    glBegin(GL_QUADS)
    glTexCoord2f(0,0); glVertex3f(-1.5, -1, 0)
    glTexCoord2f(1,0); glVertex3f(1.5, -1, 0)
    glTexCoord2f(1,1); glVertex3f(1.5, 1, 0)
    glTexCoord2f(0,1); glVertex3f(-1.5, 1, 0)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # --- NOMOR 3: Viewing & Proyeksi 3D (Perspektif) ---
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Variabel Transformasi
    tx, ty = 0, 0
    rot_x, rot_y = 0, 0
    scale = 1.0
    reflection = 1.0

    LoadTexture()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # --- NOMOR 2: Transformasi Geometris 3D ---
        keys = pygame.key.get_pressed()
        
        # Translasi (Tombol A dan D)
        if keys[K_a]: tx -= 0.1
        if keys[K_d]: tx += 0.1
        
        # Skala (Tombol W dan S)
        if keys[K_w]: scale += 0.02
        if keys[K_s]: scale -= 0.02
        
        # Rotasi (Tombol Panah)
        if keys[K_LEFT]: rot_y -= 2
        if keys[K_RIGHT]: rot_y += 2
        if keys[K_UP]: rot_x -= 2
        if keys[K_DOWN]: rot_x += 2

        # Refleksi (Tombol R) - Membalik sumbu X
        if keys[K_r]: reflection *= -1; pygame.time.wait(200)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        # Eksekusi Transformasi
        glTranslatef(tx, ty, 0) # Translasi
        glRotatef(rot_x, 1, 0, 0) # Rotasi X
        glRotatef(rot_y, 0, 1, 0) # Rotasi Y
        glScalef(scale * reflection, scale, scale) # Skala & Refleksi

        # --- NOMOR 4: Ilusi Kedalaman (Enable Depth Test) ---
        glEnable(GL_DEPTH_TEST)
        
        TankModel()
        
        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

main()