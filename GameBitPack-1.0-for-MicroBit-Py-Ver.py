from microbit import *
import random
import music

game = 1


# ==================================================
# QUIET SOUNDS
# ==================================================

def start_sound():
    music.pitch(523, 40)
    music.pitch(659, 40)
    music.pitch(784, 50)

def point_sound():
    music.pitch(880, 30)
    music.pitch(1175, 40)

def lose_sound():
    music.pitch(300, 60)
    music.pitch(220, 80)

def jump_sound():
    music.pitch(600, 25)

def shoot_sound():
    music.pitch(700, 20)

def hit_sound():
    music.pitch(1000, 25)

def wrong_sound():
    music.pitch(250, 60)


# ==================================================
# HELPERS
# ==================================================

def release_buttons():
    while button_a.is_pressed() or button_b.is_pressed():
        sleep(20)


def logo_touched():
    if pin_logo.is_touched():
        while pin_logo.is_touched():
            sleep(20)
        sleep(150)
        return True
    return False


# ==================================================
# GAME SELECT MENU
# ==================================================

def select_game():
    global game

    display.scroll("SELECT", delay=70)
    display.show(str(game))
    sleep(500)

    while True:

        # A = previous game
        if button_a.was_pressed():
            game -= 1

            if game < 1:
                game = 10

            music.pitch(400, 25)
            display.show(str(game))
            sleep(250)

        # B = next game
        if button_b.was_pressed():
            game += 1

            if game > 10:
                game = 1

            music.pitch(500, 25)
            display.show(str(game))
            sleep(250)

        # A + B = start
        if button_a.is_pressed() and button_b.is_pressed():
            release_buttons()
            start_sound()
            display.clear()
            sleep(300)
            return

        sleep(20)


# ==================================================
# GAME 1 - DODGE
# ==================================================

def game1():
    while True:

        score = 0
        player = 2
        enemy_x = random.randint(0, 4)
        enemy_y = 0

        while True:

            if logo_touched():
                return

            if button_a.was_pressed():
                if player > 0:
                    player -= 1

            if button_b.was_pressed():
                if player < 4:
                    player += 1

            enemy_y += 1

            display.clear()
            display.set_pixel(player, 4, 9)

            if enemy_y <= 4:
                display.set_pixel(enemy_x, enemy_y, 9)

            if enemy_y >= 4:

                if enemy_x == player:
                    lose_sound()
                    sleep(300)

                    # RESTART GAME
                    break

                score += 1
                point_sound()

                enemy_x = random.randint(0, 4)
                enemy_y = 0

            sleep(350)


# ==================================================
# GAME 2 - REACTION
# ==================================================

def game2():
    while True:

        score = 0

        while True:

            display.clear()
            sleep(random.randint(800, 2000))

            display.show(Image.SURPRISED)

            while True:

                if logo_touched():
                    return

                if button_a.is_pressed() or button_b.is_pressed():
                    score += 1
                    point_sound()

                    display.show(Image.YES)
                    sleep(250)
                    break

                sleep(10)

            if score >= 5:
                display.show(Image.HAPPY)
                sleep(500)
                break

        # Restart automatically


# ==================================================
# GAME 3 - TARGET
# ==================================================

def game3():
    while True:

        score = 0

        while True:

            target_x = random.randint(0, 4)
            target_y = random.randint(0, 4)

            display.clear()
            display.set_pixel(target_x, target_y, 9)

            while True:

                if logo_touched():
                    return

                if button_a.is_pressed() and button_b.is_pressed():
                    release_buttons()

                    score += 1
                    hit_sound()

                    display.show(Image.HAPPY)
                    sleep(200)
                    break

                sleep(20)

            if score >= 5:
                display.show(Image.YES)
                sleep(500)
                break

        # Restart automatically


# ==================================================
# GAME 4 - SPACE SHOOTER
# ==================================================

def game4():
    while True:

        score = 0
        player = 2

        bullet_x = -1
        bullet_y = -1

        enemy_x = random.randint(0, 4)
        enemy_y = 0

        timer = 0

        while True:

            if logo_touched():
                return

            # Move left
            if button_a.was_pressed():
                if player > 0:
                    player -= 1

            # Move right
            if button_b.was_pressed():
                if player < 4:
                    player += 1

            # Shoot
            if button_a.is_pressed() and button_b.is_pressed():
                bullet_x = player
                bullet_y = 3
                shoot_sound()
                release_buttons()

            timer += 1

            # Enemy moves slowly
            if timer >= 5:
                enemy_y += 1
                timer = 0

            # Bullet moves
            if bullet_y >= 0:
                bullet_y -= 1

            if bullet_y < 0:
                bullet_x = -1

            # Hit enemy
            if bullet_x == enemy_x and bullet_y == enemy_y:

                score += 1
                hit_sound()

                bullet_x = -1
                bullet_y = -1

                enemy_x = random.randint(0, 4)
                enemy_y = 0

            # Enemy reaches bottom
            if enemy_y >= 4:

                if enemy_x == player:
                    lose_sound()

                    # Only show score
                    display.scroll(str(score))
                    sleep(500)

                    # RESTART
                    break

                enemy_x = random.randint(0, 4)
                enemy_y = 0

            display.clear()

            # Player
            display.set_pixel(player, 4, 9)

            # Bullet
            if bullet_y >= 0:
                display.set_pixel(bullet_x, bullet_y, 9)

            # Enemy
            display.set_pixel(enemy_x, enemy_y, 9)

            sleep(80)


# ==================================================
# GAME 5 - MEMORY
# ==================================================

def game5():
    while True:

        score = 0

        while True:

            answer = random.randint(0, 1)

            if answer == 0:
                display.show(Image.ARROW_W)
            else:
                display.show(Image.ARROW_E)

            sleep(500)

            while True:

                if logo_touched():
                    return

                if button_a.was_pressed():
                    choice = 0
                    break

                if button_b.was_pressed():
                    choice = 1
                    break

            if choice == answer:

                score += 1
                point_sound()

                display.show(Image.YES)
                sleep(200)

                if score >= 5:
                    display.show(Image.HAPPY)
                    sleep(500)
                    break

            else:

                wrong_sound()
                display.show(Image.NO)
                sleep(300)

                # RESTART
                break


# ==================================================
# GAME 6 - CATCH
# ==================================================

def game6():
    while True:

        score = 0
        player = 2

        item_x = random.randint(0, 4)
        item_y = 0

        while True:

            if logo_touched():
                return

            if button_a.was_pressed():
                if player > 0:
                    player -= 1

            if button_b.was_pressed():
                if player < 4:
                    player += 1

            item_y += 1

            display.clear()

            display.set_pixel(player, 4, 9)

            if item_y <= 4:
                display.set_pixel(item_x, item_y, 9)

            if item_y >= 4:

                if item_x == player:

                    score += 1
                    point_sound()

                    item_x = random.randint(0, 4)
                    item_y = 0

                else:

                    lose_sound()
                    display.scroll(str(score))
                    sleep(500)

                    # RESTART
                    break

            sleep(300)


# ==================================================
# GAME 7 - LEFT OR RIGHT
# ==================================================

def game7():
    while True:

        score = 0

        while True:

            answer = random.randint(0, 1)

            if answer == 0:
                display.show(Image.ARROW_W)
            else:
                display.show(Image.ARROW_E)

            sleep(400)

            while True:

                if logo_touched():
                    return

                if button_a.was_pressed():
                    choice = 0
                    break

                if button_b.was_pressed():
                    choice = 1
                    break

            if choice == answer:

                score += 1
                point_sound()

                display.show(Image.YES)
                sleep(200)

                if score >= 5:
                    display.show(Image.HAPPY)
                    sleep(500)
                    break

            else:

                wrong_sound()
                display.show(Image.NO)
                sleep(300)

                # RESTART
                break


# ==================================================
# GAME 8 - FLAPPY BIRD
# ==================================================

def game8():
    while True:

        score = 0
        bird_y = 2

        pipe_x = 4
        gap_y = random.randint(1, 3)

        timer = 0

        while True:

            if logo_touched():
                return

            # Flap
            if button_a.was_pressed():
                bird_y -= 1
                jump_sound()

            timer += 1

            if timer >= 4:

                bird_y += 1
                pipe_x -= 1

                timer = 0

            # New pipe
            if pipe_x < 0:

                pipe_x = 4
                gap_y = random.randint(1, 3)

                score += 1
                point_sound()

            # Keep bird on screen
            if bird_y < 0:
                bird_y = 0

            # Hit floor
            if bird_y > 4:

                lose_sound()
                display.scroll(str(score))
                sleep(500)

                # RESTART
                break

            # Hit pipe
            if pipe_x == 0:

                if bird_y != gap_y:

                    lose_sound()
                    display.scroll(str(score))
                    sleep(500)

                    # RESTART
                    break

            display.clear()

            # Bird
            display.set_pixel(0, bird_y, 9)

            # Pipe
            for y in range(5):

                if y != gap_y:
                    display.set_pixel(pipe_x, y, 5)

            sleep(120)


# ==================================================
# GAME 9 - LIGHT REACTION
# ==================================================

def game9():
    while True:

        score = 0

        while True:

            sleep(random.randint(500, 2000))

            display.show(Image.SQUARE_SMALL)

            while True:

                if logo_touched():
                    return

                if button_a.is_pressed() or button_b.is_pressed():

                    score += 1
                    point_sound()

                    display.show(Image.YES)
                    sleep(250)

                    break

                sleep(10)

            if score >= 5:

                display.show(Image.HAPPY)
                sleep(500)

                break


# ==================================================
# GAME 10 - MINI RUNNER
# ==================================================

def game10():
    while True:

        score = 0

        player_y = 4
        obstacle_x = 4
        jumping = 0

        while True:

            if logo_touched():
                return

            # Jump
            if button_a.was_pressed():

                if jumping == 0:
                    jumping = 4
                    jump_sound()

            if jumping > 0:

                player_y = 2
                jumping -= 1

            else:

                player_y = 4

            obstacle_x -= 1

            if obstacle_x < 0:

                obstacle_x = 4
                score += 1

                point_sound()

            # Collision
            if obstacle_x == 0 and player_y == 4:

                lose_sound()
                display.scroll(str(score))
                sleep(500)

                # RESTART
                break

            display.clear()

            display.set_pixel(0, player_y, 9)
            display.set_pixel(obstacle_x, 4, 9)

            sleep(180)


# ==================================================
# MAIN PROGRAM
# ==================================================

display.show(Image.HAPPY)
sleep(500)

while True:

    # Wait for logo
    while not pin_logo.is_touched():
        sleep(20)

    # Wait for release
    while pin_logo.is_touched():
        sleep(20)

    sleep(200)

    # Open SELECT GAME menu
    select_game()

    # Start selected game

    if game == 1:
        game1()

    elif game == 2:
        game2()

    elif game == 3:
        game3()

    elif game == 4:
        game4()

    elif game == 5:
        game5()

    elif game == 6:
        game6()

    elif game == 7:
        game7()

    elif game == 8:
        game8()

    elif game == 9:
        game9()

    elif game == 10:
        game10()
