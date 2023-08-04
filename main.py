from tkinter import *
import random

# initialize the window
window = Tk()
window.title("Space Invaders")
window.geometry("500x600")

# initialize the canvas
canvas = Canvas(window, bg="black", height=600, width=500)
canvas.pack()



# initialize the bullet
bullets = []

enemies = []
enemy_count = 1
for i in range(enemy_count):
    x = random.randint(0, 500)
    y = random.randint(0, 100)
    enemy = canvas.create_oval(x, y, x+50, y+50, fill="red")
    enemies.append(enemy)

# game settings
HEIGHT = 500
ENEMY_SPEED = 1
ENEMY_SPEED_INTERVAL = 20

# initialize score
score = 0
game_over = False
import os

def get_high_score():
    if os.path.exists("high_score.txt"):
        # File exists, read and return the high score
        with open("high_score.txt", "r") as file:
            return int(file.read())
    else:
        # File doesn't exist, create it and return 0 as the high score
        with open("high_score.txt", "w") as file:
            file.write("0")
        return 0


# initialize high score
high_score = get_high_score()

def move_bullet():
    global enemies, bullets, score, high_score, game_over
    # Check if the game is over
    if game_over:
        return
    canvas.delete("score_display")
    canvas.delete("high_score_display")
    canvas.create_text(10, 10, text="Score: {}".format(score), fill="white", anchor="nw", tags="score_display")
    canvas.create_text(10, 30, text="High Score: {}".format(high_score), fill="white", anchor="nw", tags="high_score_display")
    for bullet in bullets:
        if canvas.itemcget(bullet, 'fill') != '':
            canvas.move(bullet, 0, -10)
            x1, y1, x2, y2 = canvas.coords(bullet)
            if y1 < 0:
                canvas.delete(bullet)
                bullets.remove(bullet)
            else:
                for enemy in enemies:
                    ex1, ey1, ex2, ey2 = canvas.coords(enemy)
                    if x2 >= ex1 and x1 <= ex2 and y2 >= ey1 and y1 <= ey2:
                        canvas.delete(bullet)
                        bullets.remove(bullet)
                        canvas.delete(enemy)
                        enemies.remove(enemy)
                        score += 1
                        if score > high_score:
                            high_score = score
                            update_high_score(high_score)
                        if not enemies:
                            canvas.create_text(250, 250, text="You win!", fill="white", font=("Helvetica", 36))
                            return
    window.after(50, move_bullet)

def move_player(event):
    x1, y1, x2, y2, x3, y3 = canvas.coords(player)
    if event.keysym == "Left" and x1 > 0:
        canvas.move(player, -10, 0)
    elif event.keysym == "Right" and x3 < 500:
        canvas.move(player, 10, 0)

def shoot(event):
    x, y = canvas.coords(player)[0], canvas.coords(player)[1]
    bullet = canvas.create_rectangle(x, y, x+5, y-10, fill="white", tags="bullet")
    bullets.append(bullet)

def move_enemy():
    global enemies, game_over  # add game_over to the global variables
    if game_over:  # check if the game is over
        return
    for enemy in enemies:
        x1, y1, x2, y2 = canvas.coords(enemy)
        if y2 >= HEIGHT+10:
            canvas.delete(enemy)
            enemies.remove(enemy)
            canvas.create_text(250, 250, text="Game Over", fill="white", font=("Arial", 30))
            end_screen()
        else:
            canvas.move(enemy, 0, ENEMY_SPEED)
            for bullet in bullets:
                bx1, by1, bx2, by2 = canvas.coords(bullet)
                if x2 >= bx1 and x1 <= bx2 and y2 >= by1 and y1 <= by2:
                    canvas.delete(bullet)
                    bullets.remove(bullet)
                    canvas.delete(enemy)
                    enemies.remove(enemy)
                    break
    if len(enemies) < 3:
        x = random.randint(0, 500)
        y = random.randint(0, 100)
        enemy = canvas.create_oval(x, y, x+50, y+50, fill="red")
        enemies.append(enemy)
    canvas.after(ENEMY_SPEED_INTERVAL, move_enemy)

def update_high_score(new_high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(new_high_score))

def end_screen():
    global score, high_score, game_over
    game_over = True  # Set the game over flag to True
    if score > high_score:
        high_score = score
        update_high_score(high_score)
    retry_button = Button(window, text="Retry", command=restart_game)
    retry_button.pack()
    canvas.create_window(250, 300, window=retry_button)

def restart_game():
    global score, bullets, enemies, game_over, ENEMY_SPEED_INTERVAL
    game_over = False  # Reset the game over flag to False
    ENEMY_SPEED_INTERVAL = 20  # Reset the enemy speed interval
    canvas.delete('all')
    score = 0
    bullets = []
    enemies = []
    start_game()

def start_game():
    global player
    # Recreate the player
    player = canvas.create_polygon(250, 550, 260, 570, 240, 570, fill="blue")
    # bind the keys to the functions
    canvas.bind("<Left>", move_player)
    canvas.bind("<Right>", move_player)
    canvas.bind("<space>", shoot)

    # start moving the enemies and the bullets
    move_bullet()

    # gradually increase the number of enemies
    def increase_enemies():
        if len(enemies) < 3:
            x = random.randint(0, 500)
            y = random.randint(0, 100)
            enemy = canvas.create_oval(x, y, x+50, y+50, fill="red")
            enemies.append(enemy)
        canvas.after(2000, increase_enemies)

    increase_enemies()
    move_enemy()

    # set focus to the canvas
    canvas.focus_set()


start_game()
window.mainloop()