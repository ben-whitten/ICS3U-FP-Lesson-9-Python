#!/usr/bin/env python3

# Created by: Ben Whitten
# Created on: November 2019
# Makes a game on circuit python

import ugame
import stage
import time
import random

import constants


def splash_scene():
    # this function is the splash scene game loop

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, 160, 120)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic

        # Wait for 1 seconds
        time.sleep(1.0)
        menu_scene()

        # redraw sprite list

def menu_scene():
    # this function is a scene

    # an image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # used this program to split the iamge into tile: https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # a list of sprites
    sprites = []

    # add text objects
    text = []

    text1 = stage.Text(width=29, height=14, font=None, palette=constants.NEW_PALETTE, buffer=None)
    text1.move(20, 10)
    text1.text("BALL BREAKER!")
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None, palette=constants.NEW_PALETTE, buffer=None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers, items show up in order
    game.layers = text + sprites + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input

        # update game logic
        keys = ugame.buttons.get_pressed()
        #print(keys)

        if keys & ugame.K_START != 0:  # Start button
            game_scene()
            #break


def game_scene():

    image_bank_1 = stage.Bank.from_bmp16("ball.bmp")
    sprites = []
    image_bank_2 = stage.Bank.from_bmp16("space_aliens.bmp")
    sprites = []

    attack = []
    for attack_number in range(constants.TOTAL_ATTACKS):
        a_single_attack = stage.Sprite(image_bank_1, 2, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        attack.append(a_single_attack)

    # this sets the background
    a_button = constants.button_state["button_up"]

    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # this is the background
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1,3)
            background.tile(x_location, y_location, tile_picked)

    # create a sprite
    # parameters (image_bank_1, image # in bank, x, y)
    ball_one = stage.Sprite(image_bank_1, 3, 64, 56)
    sprites.append(ball_one)
    ball_two = stage.Sprite(image_bank_1, 2, 75, 56)
    sprites.insert(0, ball_two)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = sprites + attack + [background]

    game.render_block()

    while True:
        # get user inputs
        keys = ugame.buttons.get_pressed()
        # print(keys)
        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_UP != 0:
            if ball_one.y < 0:
                ball_one.move(ball_one.x, 0)
            else:
                ball_one.move(ball_one.x, ball_one.y -
                              constants.SPRITE_MOVEMENT_SPEED)
            pass
        if keys & ugame.K_DOWN != 0:
            if ball_one.y > constants.SCREEN_Y - constants.SCREEN_GRID_Y:
                ball_one.move(ball_one.x, constants.SCREEN_Y -
                              constants.SPRITE_SIZE)
            else:
                ball_one.move(ball_one.x, ball_one.y +
                              constants.SPRITE_MOVEMENT_SPEED)
            pass
        if keys & ugame.K_LEFT != 0:
            if ball_one.x < 0:
                ball_one.move(0, ball_one.y)
            else:
                ball_one.move(ball_one.x - constants.SPRITE_MOVEMENT_SPEED,
                              ball_one.y)
            pass
        if keys & ugame.K_RIGHT != 0:
            if ball_one.x > constants.SCREEN_X - constants.SCREEN_GRID_X:
                ball_one.move(constants.SCREEN_X - constants.SPRITE_SIZE,
                              ball_one.y)
            else:
                ball_one.move(ball_one.x + constants.SPRITE_MOVEMENT_SPEED,
                              ball_one.y)
            pass
        # update game logic
        if a_button == constants.button_state["button_just_pressed"]:
            for attack_number in range(len(attack)):
                if attack[attack_number].x < 0:
                    attack[attack_number].move(ball_one.x, ball_one.y)
                    sound.play(pew_sound)
                    break
        for attack_number in range(len(attack)):
            if attack[attack_number].x > 0:
                attack[attack_number].move(attack[attack_number].x,
                                           attack[attack_number].y -
                                           constants.ATTACK_SPEED)
                if attack[attack_number].y < constants.OFF_TOP_SCREEN:
                   attack[attack_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)

        # redraw sprtie list
        game.render_sprites(sprites + attack)
        game.tick()  # wait until refresh rate finishes


if __name__ == "__main__":
    menu_scene()
