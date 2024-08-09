import tkinter as tk
from tkinter import messagebox
import sqlite3
import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 80
PIPE_GAP = 150

# Database functions
def init_db():
    conn = sqlite3.connect('users.db')
    return conn.cursor(), conn

def register_user(username, password):
    cursor, conn = init_db()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    cursor, conn = init_db()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def register_page():
    def submit_registration():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        if register_user(username, password):
            messagebox.showinfo("Registration", "Registration Successful! You can now log in.")
            registration_window.destroy()
        else:
            messagebox.showerror("Registration", "Username already exists or registration failed.")
    
    registration_window = tk.Tk()
    registration_window.title("Register")

    tk.Label(registration_window, text="Username").pack()
    entry_reg_username = tk.Entry(registration_window)
    entry_reg_username.pack()

    tk.Label(registration_window, text="Password").pack()
    entry_reg_password = tk.Entry(registration_window, show='*')
    entry_reg_password.pack()

    tk.Button(registration_window, text="Register", command=submit_registration).pack()

    registration_window.mainloop()

def login_page():
    def check_login():
        username = entry_username.get()
        password = entry_password.get()
        if authenticate_user(username, password):
            messagebox.showinfo("Login", "Login Successful!")
            login_window.destroy()
            start_game()
        else:
            messagebox.showerror("Login", "Invalid Credentials")
    
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username").pack()
    entry_username = tk.Entry(login_window)
    entry_username.pack()

    tk.Label(login_window, text="Password").pack()
    entry_password = tk.Entry(login_window, show='*')
    entry_password.pack()

    tk.Button(login_window, text="Login", command=check_login).pack()
    tk.Button(login_window, text="Register", command=register_page).pack()

    login_window.mainloop()

# Game classes and functions
class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.velocity = 0

    def flap(self):
        self.velocity += FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, 450)

    def update(self):
        self.x -= 5

    def draw(self):
        # Top pipe
        screen.blit(pipe_image, (self.x, self.height - SCREEN_HEIGHT))
        # Bottom pipe
        screen.blit(pipe_image, (self.x, self.height + PIPE_GAP))

def start_game():
    global screen, bird_image, pipe_image
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load images
    bird_image = pygame.Surface((30, 30))
    bird_image.fill((255, 0, 0))
    pipe_image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
    pipe_image.fill((0, 255, 0))

    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((135, 206, 235))  # Sky color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        # Check for pipe generation
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()

        # Draw the bird
        screen.blit(bird_image, (bird.x, bird.y))

        # Check for collisions
        for pipe in pipes:
            if bird.x + 30 > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                if bird.y < pipe.height or bird.y + 30 > pipe.height + PIPE_GAP:
                    running = False

        # If the bird falls below the screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Start the application with the login page
login_page()
