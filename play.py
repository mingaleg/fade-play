#!/usr/bin/env python3
#-*- coding: utf-8 -*-

MAX_VOLUME = 100
BACK_FADE_VOLUME = 20
BACK_VOLUME = 30
FRONT_VOLUME = 120

import subprocess
from time import sleep

PWD = '/home/shhdup/fade_play/'


BACK_MUSIC = (
    'back2.mp3',
    'back1.mp3',
)

FRONT_MUSIC = (
    ('01.mp3', 'Чтобы стать настоящим'),
    ('02.mp3', 'Это непросто делай то'),
    ('03.mp3', 'То что я тебе даю'),
    ('04.mp3', 'А теперь лезь под верёвку'),
    ('05.mp3', 'Я вручаю тебе зачарованные чернила'),
    ('06.mp3', 'Иди сюда!'),
    ('07.mp3', 'Осторожно Перед тобой дверь'),
    ('0751.mp3','Скрип'),
    ('0752.mp3','Летучие мыши'),
    ('09.mp3', 'Стой и не двигайся'),
    ('10.mp3', 'Ну и где тебя носит'),
    ('11.mp3', 'Перед тобой пески времени'),
    ('12.mp3', 'Ищи быстрее'),
    ('13.mp3', 'Прекрасно Этот ключ'),
    ('14.mp3', 'Вот оно Я предупреждал'),
    ('15.mp3', 'Не бойся я прогнал'),
    ('16.mp3', 'Спасибо Теперь я могу достать'),
    ('17.mp3', 'Я вижу Великому Порядку опять'),
    ('20.mp3', 'Разверни свиток который'),
    ('21.mp3', 'Теперь полей этот свиток'),
    ('22.mp3', 'Из свитка который тебе дал Порядок'),
    ('23.mp3', 'Иди сюда и держи питона'),
    ('24.mp3', 'Чувствуешь Питон начал извиваться'),
    ('25.mp3', 'ПОРЯДОК Да Я чувствую'),
    ('26.mp3', 'ХАОС Да Я чувствую Сделай два шага'),
    ('27.mp3', 'Но тебе пока рано есть его'),
    ('28.mp3', 'Съешь его и ты уже завтра'),
    ('29.mp3', 'Я знаю что в душе ты стремишься'),
    ('30.mp3', 'Подойди ко мне. На самом деле ты хочешь'),
    ('31.mp3', 'Пришла пора сделать окончательный выбор'),
    ('32.mp3', 'Что ж выбор сделан Чтобы завершить обряд'),
    ('33.mp3', 'Теперь выпей этот напиток'),
    ('34.mp3', 'Не забывай что здесь произошло'),
    ('35.mp3', 'И помни что нет ничего окончательного'),
    ('355.mp3', 'Гром'),
)


BACK_MUSIC = [PWD + foo for foo in BACK_MUSIC]
FRONT_MUSIC = [(PWD + foo, desc) for foo, desc in FRONT_MUSIC]


back = subprocess.Popen(['mplayer', '-softvol', '-loop', '0', '-slave', '-quiet'] + BACK_MUSIC, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
back.stdin.write(bytes('volume %d %d\n' % (BACK_VOLUME, MAX_VOLUME), 'utf-8'))
back.stdin.flush()


def play_front(snd):
    back.stdin.write(bytes('volume %d %d\n' % (BACK_FADE_VOLUME, MAX_VOLUME), 'utf-8'))
    back.stdin.flush()
    front = subprocess.Popen(['mplayer', '-softvol', '-slave', '-quiet', snd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        front.stdin.write(bytes('volume %d %d\n' % (FRONT_VOLUME, MAX_VOLUME), 'utf-8'))
        front.stdin.flush()
        front.wait()
    except:
        print('FRONT INTERUPTED')
        front.kill()
    back.stdin.write(bytes('volume %d %d\n' % (BACK_VOLUME, MAX_VOLUME), 'utf-8'))
    back.stdin.flush()

try:
    while True:
        cur = 0
        while cur < len(FRONT_MUSIC):
            snd, desc = FRONT_MUSIC[cur]
            print('%2d: READY %s - %s' % (cur+1, snd, desc), end='? ')
            inp = input()
            if inp:
                if inp.isnumeric():
                    inp = PWD + inp + '.mp3'
                    changed = False
                    for i in range(len(FRONT_MUSIC)):
                        if FRONT_MUSIC[i][0] == inp:
                            cur = i
                            changed = True
                            break
                    if not changed:
                        print('WARNING! "%s" not found' % inp)
                elif inp[1:].isnumeric():
                    inp = int(inp[1:]) - 1
                    if 0 <= inp < len(FRONT_MUSIC):
                        cur = inp
                    else:
                        print('WARNING! Number should be between 1 and %d' % len(FRONT_MUSIC))
                else:
                    foo = []
                    for i in range(len(FRONT_MUSIC)):
                        if inp.upper() in FRONT_MUSIC[i][1].upper():
                            foo.append((i+1, FRONT_MUSIC[i][0], FRONT_MUSIC[i][1]))
                    if len(foo) == 0:
                        print('WARNING! "%s" not found' % inp)
                    elif len(foo) == 1:
                        cur = foo[0][0] - 1
                    else:
                        print('WARNING! Too many variantes:')
                        for bar in foo:
                            print('%3d %s %s' % bar)
            else:
                play_front(snd)
                print('OK %s - %s' % (snd, desc))
                cur += 1
        print('LOOP FINISHED')
except Exception as E:
    print(str(E))
    back.kill()
