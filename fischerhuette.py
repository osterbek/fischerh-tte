# !/usr/bin/python
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import random
from copy import deepcopy
import os
import pickle

### parameters
monty_click_at_player = True
all_guys = ['Billy', 'Oliver', 'Axel W', 'Olav', 'Dirk', 'Thomsky']
default_player_if_no_backup_exists = [0, 1, 1, 1, 0, 1]
fullscreen_mode = True
scaling_factor_to_screenheight = 90
font_size = int(scaling_factor_to_screenheight / 10)
typo = 'Verdana'


positions_cards = [[[3, 1], [5, 1], [5, 13], [3, 13]], [[3, 1], [5, 1], [7, 7], [5, 13], [3, 13], [1, 7]]]
positions_player_name = [[[3, 7], [5, 7], [5, 11], [3, 11]], [[3, 7], [5, 7], [5, 9], [5, 11], [3, 11], [3, 9]]]
sticky_names_1 = [['S', 'S', 'S', 'S'],['S', 'S', 'SE', 'S', 'S', 'SW']]
sticky_names_2 = [['N', 'N', 'N', 'N'],['N', 'N', 'NE', 'N', 'N', 'NW']]
filename_pkl = 'fischerhuette.pkl'
hand_quality_categories = [0, 'schlecht'], [17, 'schwach'], [23, 'mittel'], [30, 'gut'], [39, 'stark']
score_parameter = [[5.5, "Herz 10"],
                   [2.5, "Trumpf-Dame"],
                   [2.0, "Fehlfarben-Ass"],
                   [5.0, "Trumpf ab fünf"],
                   [6.5, "Hochzeit"],
                   [6.0, "blanke Fehlfarbe"],
                   [7.0, "Schwein"],
                   [1.5, "PikDame und KreuzBube"],
                   [1.0, "erstes schwarzes Ass"],
                   [2.0, "Trumpf ab acht"]]
card_categories = ['Dulle', 'Re', 'Trumpf', 'Kreuz', 'Pik', 'Herz', 'Neunen', 'Fuchs', 'Karo-9', 'Dame', 'Fehl-Ass', 'Pik Dame oder Kreuz Bube', 'schwarzes Ass']
c = [
    ['Herz 10',     1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Kreuz Dame',  0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ['Pik Dame',    0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    ['Herz Dame',   0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ['Karo Dame',   0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    ['Kreuz Bube',  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    ['Pik Bube',    0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Herz Bube',   0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Karo Bube',   0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Karo Ass',    0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    ['Karo 10',     0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Karo König',  0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Karo 9',      0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    ['Kreuz Ass',   0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    ['Kreuz 10',    0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Kreuz König', 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Kreuz 9',     0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    ['Pik Ass',     0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    ['Pik 10',      0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Pik König',   0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    ['Pik 9',       0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    ['Herz Ass',    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    ['Herz König',  0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    ['Herz 9',      0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]]


def card_image(card, size):
    pre = ['he_10', 'kr_da', 'pi_da', 'he_da', 'ka_da', 'kr_bu', 'pi_bu', 'he_bu', 'ka_bu', 'ka_as', 'ka_10', 'ka_ko',
           'ka_09', 'kr_as', 'kr_10', 'kr_ko', 'kr_09', 'pi_as', 'pi_10', 'pi_ko', 'pi_09', 'he_as', 'he_ko', 'he_09']
    return ImageTk.PhotoImage(Image.open('cardimages\\' + pre[card] + '.png').resize((size[0], size[1])))


def init():
    global mainWin, mainFrame, gamecode_entry, playercount_entry, subFrame
    mainWin = Tk()
    mainFrame = ttk.Frame(mainWin)
    mainWin.title('Fischerhütte 21')
    menubar = Menu(mainWin)
    menubar.add_command(label="quit", command=mainWin.quit)
    menubar.add_command(label="new game", command=new_start)
    menubar.add_command(label="hands", command=show_hands)
    menubar.add_command(label="turn hand", command=show_hand_of_player)
    menubar.add_command(label="moves", command=show_moves)
    menubar.add_command(label="monty round", command=monty_round)
    menubar.add_command(label="monty move", command=monty_move_from_bar)
    menubar.add_command(label="undo", command=undo_from_bar)
    menubar.add_command(label="kiosk mode", command=fullscreen_toggle)
    mainWin.config(menu=menubar)
    mainFrame.grid()
    mainWin.rowconfigure(0, weight=1)
    mainWin.columnconfigure(0, weight=1)
    gamecode_entry_label = Label(mainFrame , text="Code:", font=('typo', font_size+4), fg='black', height=1, width=6)
    gamecode_entry_label.grid(column=1, row=14, rowspan=1, columnspan=1, sticky='W')
    gamecode_entry = Entry(mainFrame, font=('typo', font_size+4), width=5, name='gamecodeentry')
    gamecode_entry.bind("<Return>", click_handling)
    gamecode_entry.grid(column=2, row=14, rowspan=1, columnspan=1, sticky='W')
    show_player_selection()
    scaling_image_preparation()
    init_player()


def fullscreen_toggle():
    destroy_subframe()
    global fullscreen_mode
    if fullscreen_mode:
        fullscreen_mode = False
    else:
        fullscreen_mode = True
    scaling_image_preparation()
    init_player()
    arrange_tablecards()
    update_shown_content()


def scaling_image_preparation():
    global card_sizes_table, card_sizes_select, card_sizes_hands, select_card_pix, thrown_card_pix, hand_card_pix
    x = mainWin.winfo_screenwidth()
    y = mainWin.winfo_screenheight()
    scale = 241 / 768 * y * scaling_factor_to_screenheight / 100
    card_sizes_table  = [int(scale * 175 / 267), int(scale)]
    card_sizes_select = [int(scale * 175 / 267 * 0.5), int(scale * 0.5)]
    card_sizes_hands  = [int(scale * 175 / 267 * 0.48), int(scale * 0.48)]
    mainWin.attributes('-fullscreen', fullscreen_mode)
    select_card_pix = []
    thrown_card_pix = []
    hand_card_pix = []
    for c in range(0, 24):
        select_card_pix.append(card_image(c, card_sizes_select))
        thrown_card_pix.append(card_image(c, card_sizes_table))
        hand_card_pix.append(card_image(c, card_sizes_hands))
        image_selectcard = ttk.Label(mainFrame, name='selectcard {:0>2}'.format(c), image=select_card_pix[c])
        image_selectcard.grid(column=11+c%4, row=1+(c//4)*3, rowspan=3)
        image_selectcard.bind('<Button-1>', click_handling)


def derive_player_count(selected_players):
    global ppp
    if sum([value for value in selected_players]) < 6:
        ppp = 4
    else:
        ppp = 6


def init_player():
    global black_card_pix, ppp, selected_players, dummy_pix
    for i in range(0, len(selected_players)):
        selected_players[i] = int(str(selectplayervalue[i].get()))
    derive_player_count(selected_players)
    black_card_pix = []
    for p in range(0, 6):
        Label(mainFrame, name='player {:0>2}'.format(p)).destroy()
        Label(mainFrame, name='teamtoggle {:0>2}'.format(p)).destroy()
    for p in range(0, ppp):
        black_card_pix.append(ImageTk.PhotoImage(Image.open('cardimages\\black.png').resize((card_sizes_table[0], card_sizes_table[1]))))
        image_blackcard = ttk.Label(mainFrame, name='blackcard {:0>2}'.format(p), image=black_card_pix[p])
        image_blackcard.grid(column=positions_cards[ppp//2-2][p][0], row=positions_cards[ppp//2-2][p][1], rowspan=6,columnspan=2)
        if monty_click_at_player:
            image_blackcard.bind('<Button-1>', click_handling)
        sticker_names = Label(mainFrame, text=names(p), font=('typo', font_size+4), fg='white', height=1 , width=7, bg='blue', name='player {:0>2}'.format(p))
        sticker_names.grid(column=positions_player_name[ppp//2-2][p][0], row=positions_player_name[ppp//2-2][p][1], columnspan=2, sticky=sticky_names_1[ppp//2-2][p])
        sticker_names.bind('<Button-1>', click_handling)
    if ppp < 6:
        dummy_pix = []
        for i in (2, 5):
            dummy_pix.append(ImageTk.PhotoImage(Image.open('cardimages\\dummy.png').resize((card_sizes_table[0], card_sizes_table[1]))))
            image = ttk.Label(mainFrame, name='blackcard_dummy {:0>2}'.format(i), image=dummy_pix[-1])
            image.grid(column=positions_cards[1][i][0], row=positions_cards[1][i][1], rowspan=6,columnspan=2)


def init_player_from_run():
    init_player()
    new_start()


def click_handling(event):
    global player_toggle_object, gamecode, hands, ev, ppp
    command = str(event.widget).split('.')[-1].split(' ')
    if command[0] == 'selectcard':
        if not fool_block[0]:
            throw_card(int(command[1]))
    if command[0] == 'player':
        if not fool_block[0]:
            that_player(int(command[1]))
    if command[0] == 'tablecard':
        undo_tablecard(int(command[1]), int(command[2]))
    if command[0] == 'blackcard':
        if int(command[1]) == whos_turn():
            if monty_reasonable():
                card = monty_move()
                throw_card(card)
    if command[0] == 'teamtoggle':
        contra_or_re[int(command[1])] += 1
        if contra_or_re[int(command[1])] == 3:
            contra_or_re[int(command[1])] = 0
    if command[0] == 'playertoggle':
        player_toggle_object[int(command[1])] += 1
        if player_toggle_object[int(command[1])] >= ppp:
            player_toggle_object[int(command[1])] = -1
    if command[0] == 'gamecodeentry':
        gamecode = 0
        if gamecode_entry.get().isdecimal():
            gamecode = int(gamecode_entry.get())
        gamecode_entry.delete(0, 999)
        new_start()
    if command[0] == 'playercard':
        if not fool_block[0]:
            destroy_subframe()
            throw_card(int(command[2]))
        else:
            return
    update_shown_content()


def whos_turn():
    if len(moves) == 0:
        return -2
    elif moves[-1][1] < 0:
        return moves[-1][0]
    elif (len(moves)-1)%(ppp+1) >= ppp:
        return -1
    else:
        temp = moves[-1][0] + 1
        if temp >= ppp:
            temp = 0
        return temp


def clear_away_tablecards():
    for i in range(0, min(len(moves), ppp + 1)):
        if moves[-1-i][1] >= 0:
            image = ttk.Label(mainFrame, name='tablecard {:d} {:0>2}'.format(moves[-1-i][0], moves[-1-i][1]), image=thrown_card_pix[moves[-1-i][1]])
            image.destroy()


def arrange_tablecards():
    for i in range(0, min(len(moves), ppp + 1)):
        if moves[-1-i][1] >= 0:
            p = moves[-1-i][0]
            c = moves[-1-i][1]
            image = ttk.Label(mainFrame, name='tablecard {:d} {:0>2}'.format(p, c), image=thrown_card_pix[c])
            image.grid(column=positions_cards[ppp//2-2][p][0], row=positions_cards[ppp//2-2][p][1],rowspan=6,columnspan=2)
            image.bind('<Button-1>', click_handling)
        else:
            break


def undo_tablecard(player, card):
    global moves, fool_block
    if (moves[-1][1] == card) and (moves[-1][0] == player):
        del moves[-1]
        ttk.Label(mainFrame, name='tablecard {:d} {:0>2}'.format(player, card), image=thrown_card_pix[card]).destroy()
        fool_block = (False, 'alles okay')


def undo_from_bar():
    destroy_subframe()
    if len(moves) == 1:
        del moves[-1]
    if len(moves) > 1:
        if moves[-1][1] >= 0:
            undo_tablecard(moves[-1][0], moves[-1][1])
        else:
            del moves[-1]
            arrange_tablecards()
    update_shown_content()


def that_player(player):
    global moves
    if len(moves) == 0:                     # noch kein Startspieler festgelegt
        moves.append((player, -2))
    elif len(moves) == 1:                   # Startspieler festgelegt aber kein Zug
        if moves[0][0] == player:
            del moves[-1]
        else:
            moves[0] = (player, -2)
    elif whos_turn() == -1:                 # Runde abgeschlossen aber kein Gewinner festgelegt => Tisch leer räumen
        moves.append((player, -1))
        clear_away_tablecards()
    elif moves[-1][1] == -1:                # Runde abgeschlossen und Gewinner festgelegt => undo und letzter Tisch zeigen
        if moves[-1][0] == player:
            del moves[-1]
            arrange_tablecards()


def throw_card(card):
    global moves, fool_block
    if (len(moves)-1)%(ppp+1) >= ppp or whos_turn() < 0:
        return
    image = ttk.Label(mainFrame, name='tablecard {:d} {:0>2}'.format(whos_turn(), card), image=thrown_card_pix[card])
    image.grid(column=positions_cards[ppp//2-2][whos_turn()][0], row=positions_cards[ppp//2-2][whos_turn()][1],rowspan=6,columnspan=2)
    image.bind('<Button-1>', click_handling)
    fool_block = fool_checker(card)
    contra_re_check(card)
    moves.append((whos_turn(), card))


def contra_re_check(card):
    global contra_or_re
    if card == 1:
        contra_or_re[whos_turn()] = 1
    if sum(contra_or_re) >= ppp//2:
        for i in range(0, ppp):
            if contra_or_re[i] == 0:
                contra_or_re[i] = 2


def fool_checker(card):
    answer = (False, names(whos_turn()) + '\nalles okay')
    if card not in remaining_cards_on_hand(whos_turn()):
        answer = (True, names(whos_turn()) + '\n' + c[card][0] + '\nhast Du nicht')
    elif requested_card() != card_type(card) and requested_card() != 'Anspiel':
        has_requested = False
        for i in remaining_cards_on_hand(whos_turn()):
            if card_type(i) == requested_card():
                has_requested = True
        if has_requested:
            answer = (True, names(whos_turn()) + '\n' + requested_card() + ' bitte\nbedienen')
    return answer


def monty_reasonable():
    if fool_block[0]:
        return False
    if len(moves) == 0:
        return False
    if (len(moves)-1)%(ppp+1) == ppp:
        return False
    if len(moves) == 1 + 12 * (ppp + 1):
        return False
    return True


def monty_move():
        possible = []
        for card in remaining_cards_on_hand(whos_turn()):
            if card_type(card) == requested_card():
                possible.append(card)
        if len(possible) == 0:
            possible = deepcopy(remaining_cards_on_hand(whos_turn()))
        if possible[0] == 0:
            trumps_without_dulle = [card for card in possible if card>=1 and card<=12]
            if len (trumps_without_dulle) > 0:
                return trumps_without_dulle[0]
        return possible[0]


def monty_move_from_bar():
    destroy_subframe()
    if monty_reasonable():
        throw_card(monty_move())
        update_shown_content()


def monty_round():
    destroy_subframe()
    if not fool_block[0] and (len(moves) > 0):
        while monty_reasonable():
            throw_card(monty_move())
        update_shown_content()


def current_round():
    return (len(moves)-1)//(ppp+1)


def winner_of_round(r):
    if r >= current_round():
        return -1
    else:
        return moves[(r+1)*(ppp+1)][0]


def points_of_round(r):
    pt = [10, 3, 3, 3, 3, 2, 2, 2, 2, 11, 10, 4, 0, 11, 10, 4, 0, 11, 10, 4, 0, 11, 4, 0]
    if r >= current_round():
        return -1
    else:
        return sum([pt[moves[(r+1)*(ppp+1)-i][1]] for i in range(1, ppp+1)])


def points_of_player(p):
    answer = 0
    for r in range(0, current_round()):
        answer += points_of_round(r) * bool(winner_of_round(r)==p)
    return answer


def points_of_parties():
    answer = [0 for i in range(0, 3)]
    for p in range(0, ppp):
        answer[contra_or_re[p]] += points_of_player(p)
    return answer


def team_scores(ev, ppp):
    txt = 'RE-Spieler sind:\n' + str(teams(ev, ppp)[0])
    if hochzeit(ev, ppp):
        txt += '\nHochzeit\n'
    else:
        txt += '\n        \n'
    txt += 'Scores (Avg):\nRe = {:d}\nContra = {:d}'.format(contra_re_scores(ev, ppp)[0], contra_re_scores(ev, ppp)[1])
    txt += '\nAdvantage = {:d}'.format(contra_re_scores(ev, ppp)[2])
    return txt


def hochzeit(ev, player_count):
    answer = False
    for p in range(0, player_count):
        if ev[1][p] > 1:
            answer = True
    return answer


def contra_re_scores(ev, player_count):
    re, co, rc, cc = 0, 0, 0, 0
    for p in range(0, player_count):
        if ev[1][p] > 0:
            re += hand_score(ev, p)
            rc += 1
        else:
            co += hand_score(ev, p)
            cc += 1
    return [int(re//rc), int(co//cc), int(re//rc - co//cc)]


def teams(ev, player_count):
    re, co = [],[]
    for p in range(0, player_count):
        if ev[1][p] > 0:
            re.append(all_guys[p])
        else:
            co.append(all_guys[p])
    return [re, co]



def show_information():
    if fool_block[0]:
        content = fool_block[1]
        bg = 'orange'
        fg='black'
    elif len(moves) == 0:
        content = 'Wer ist der \n Startspieler?'
        bg='gray85'
        fg='black'
    elif len(moves) > 12 * (ppp + 1):
        content = 'Game Over'
        bg='green'
        fg='white'
    elif (len(moves)-1)%(ppp+1) < ppp:
        content = names(whos_turn()) + '\ngefordert\n' + requested_card()
        bg='gray70'
        fg='black'
    else:
        content = 'Runde ' + str((len(moves)-1)//(ppp+1) + 1) + '\nStich geht\n an wen?'
        bg='gray90'
        fg='black'
    infobox = Label(mainFrame, text=content, font=('typo', font_size+8), fg=fg, height=4, width=11, bg=bg, name='showinformation', anchor='center')
    infobox.grid(column=1, row=1, rowspan=6, columnspan=2)
    for p in range(0, ppp):
        sticker_2 = Label(mainFrame, text=('-', 'Re', 'Contra')[contra_or_re[p]], font=('typo', font_size+3), fg='black', height=1, width=7, bg='lightgrey', name='teamtoggle {:0>2}'.format(p))
        sticker_2.grid(column=positions_player_name[ppp//2-2][p][0], row=positions_player_name[ppp//2-2][p][1]+1, columnspan=2, sticky=sticky_names_2[ppp//2-2][p])
        sticker_2.bind('<Button-1>', click_handling)
    show_points()


def show_points():
    content_1, content_2 = '', ''
    for r in range(0, 12):
        if current_round() > r:
            content_1 += str(r+1) + ' ' + names(winner_of_round(r)) + ' (' + ('-', 'Re', 'Contra')[contra_or_re[winner_of_round(r)]] + ')' + '\n'
            content_2 += str(points_of_round(r)) + '\n'
        else:
            content_1 += str(r+1) + ' ' + '<offen>' + '\n'
            content_2 += '0' + '\n'
    content_1 += '\n'
    content_2 += '\n'
    for p in range(0, ppp):
        content_1 += names(p) + ' (' + ('-', 'Re', 'Contra')[contra_or_re[p]] + ')' + '\n'
        content_2 += str(points_of_player(p)) + '\n'
    content_1 += '\n'
    content_2 += '\n'
    for i in range(0, 3):
        content_1 += ('unbekannt', 'Re', 'Contra')[i] + '\n'
        content_2 += str(points_of_parties()[i]) + '\n'
    info_1 = Label(mainFrame, text=content_1, font=('typo', font_size+2), fg='black', height=24, width=15, bg='gray90', name='points_1', justify=LEFT)
    info_1.grid(column=16, row=1, rowspan=12, columnspan=2, sticky='nw')
    info_2 = Label(mainFrame, text=content_2, font=('typo', font_size+2), fg='black', height=24, width=4, bg='gray90', name='points_2', justify=RIGHT)
    info_2.grid(column=18, row=1, rowspan=12, columnspan=1, sticky='nw')
    win_text = 'Nach ' + str(max(0, current_round())) + ' Runden \n' + str(points_of_parties()[1]) + ' zu ' \
               + str(points_of_parties()[2]) + '\n' + str(points_of_parties()[1] - (30 * ppp + 1)) \
               + ' zu ' + str(points_of_parties()[2] - (30 * ppp))
    win_bg = 'grey90'
    if decided() != 'keiner':
        win_text = 'Nach ' + str(current_round()) + ' Runden\n' + decided() + '\n' + str(points_of_parties()[1]) + ' zu ' + str(points_of_parties()[2])
        win_bg = 'yellow'
    win_label = Label(mainFrame, text=win_text, font=('typo', font_size+5), fg='black', height=5, width=15, bg=win_bg, justify=CENTER)
    win_label.grid(column=7, row=1, rowspan=6, columnspan=4)


def decided():
    answer = 'keiner'
    if points_of_parties()[1] > 30 * ppp:
        answer = 'entschieden für\nRe'
    if points_of_parties()[1] > 37.5 * ppp:
        answer = 'entschieden für\nRe <90'
    if points_of_parties()[1] > 45 * ppp:
        answer = 'entschieden für\nRe <60'
    if points_of_parties()[1] > 52.5 * ppp:
        answer = 'entschieden für\nRe <30'
    if points_of_parties()[2] >= 30 * ppp:
        answer = 'entschieden für\nContra'
    if points_of_parties()[2] >= 37.5 * ppp:
        answer = 'entschieden für\nContra <90'
    if points_of_parties()[1] >= 45 * ppp:
        answer = 'entschieden für\nContra <60'
    if points_of_parties()[1] >= 52.5 * ppp:
        answer = 'entschieden für\nContra <30'
    return answer


def shuffle_iterator(gamecode, player_count):
    random.seed(gamecode)
    while True:
        h = shuffle(player_count)
        e = evaluate_hands(h, player_count)
        if (max(e[:][6]) < 5) and (min(e[:][2]) > 3):   # keine fünf Neunen und keine drei Trümpfe
            break
    return [h, e]


def shuffle(player_count):
    mixed = [i%24 for i in range(0, 48)]
    if player_count == 6:
        mixed.extend([i for i in range(0, 24)])
    random.shuffle(mixed)
    hands = [mixed[(i * 12):((i + 1) * 12)] for i in range(0, player_count)]
    for i in range(0, player_count):
        hands[i].sort()
    return hands


def evaluate_hands(ha, player_count):
    ev = [[0 for i in range(player_count)] for j in range(len(c[0]) - 1)]
    for i in range(0, player_count):
        for j in range(0, len(c[0]) - 1):
            for k in range(0, 12):
                ev[j][i] = ev[j][i] + c[ha[i][k]][j+1]
    return ev


def show_gamecode():
    gamecode_info = Label(mainFrame , text="Seed = " + str(gamecode), font=('typo', font_size+2), fg='black', height=1, width=12, justify=LEFT)
    gamecode_info.grid(column=1, row=15, rowspan=1, columnspan=2, sticky='W')


def party(p, ev):
    if ev[1][p] > 1:
        return 'Hochzeit'
    elif ev[1][p]  > 0:
        return 'Re'
    else:
        return 'Contra'


def relative_quality_of_hand(value):
    answer = ''
    for i in range(0, len(hand_quality_categories)):
        if value >= hand_quality_categories[i][0]:
            answer = hand_quality_categories[i][1]
    return answer


def hand_score(ev, player):
    score = [0 for i in range(0, len(score_parameter))]
    score[0] = ev[0][player] * score_parameter[0][0]                     # Herz 10
    score[1] = ev[9][player] * score_parameter[1][0]                   # Trumpf-Dame
    score[2] = ev[10][player] * score_parameter[2][0]                  # Fehlfarben-Ass
    score[3] = max((ev[2][player] - 4) * score_parameter[3][0], 0)             # Trumpf ab dem fünften Stück
    if ev[1][player] > 1:
        score[4] = score_parameter[4][0] * (ev[1][player] - 1)         # Kreuz Dame mehr als 1 (also Hochzeit)
    for i in range(3, 6):
        if ev[i][player] == 0:
            score[5] = score_parameter[5][0]                  # blanke Fehlfarbe
    if ev[7][player] > 1:
        score[6] = score_parameter[6][0] * (ev[7][player] - 1)         # jedes Karo Ass mehr als 1 (also Schwein)
    total  = 0
    score[7] = ev[11][player] * score_parameter[7][0]                     # Pik Dame und Kreuz Bauer
    if ev[12][player] > 0:
        score[8] = 1* score_parameter[8][0]                     # erstes schwarzes Ass
    score[9] = max((ev[2][player] - 7) * score_parameter[9][0], 0)        # Trumpf ab dem achten Stück
    for i in range(0, len(score_parameter)):
        total += score[i]
    return total


def show_hands():
    if len(hands) > 0:
        global subFrame
        destroy_subframe()
        subFrame = ttk.Frame(mainFrame)
        subFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        for p in range(0, ppp):
            sc = hand_score(ev, p)
            txt = names(p) + '\n' + str(sc) + '\n' + relative_quality_of_hand(sc)  + '\n' + party(p, ev)
            ttk.Label(subFrame, text=txt, anchor='w', width=8, font=('typo', font_size+4)).grid(column=1, row=p+1)
            for i in range(0, 12):
                image = ttk.Label(subFrame, image=hand_card_pix[hands[p][i]])
                image.grid(column=i+2, row=p+1)
        b = ttk.Button(subFrame, text="close")
        b.grid(column=14, row=3, sticky='N')
        b.bind('<Button-1>', clear_subframe)
        c = ttk.Label(subFrame, text=team_scores(ev, ppp), anchor='c', width=20, font=('typo', font_size+4))
        c.grid(column=14, row=1, rowspan=2, columnspan=1)


def show_hand_of_player():
    if len(hands) > 0 and not fool_block[0] and whos_turn() >= 0:
        remain = deepcopy(remaining_cards_on_hand(whos_turn()))
        global subFrame
        destroy_subframe()
        subFrame = ttk.Frame(mainFrame, borderwidth = 20, relief='ridge')
        subFrame.place(relx=0.58, rely=0.1, relwidth=0.35, relheight=0.65)
        txt = names(whos_turn()) + ' ist am Zug:'
        Label(subFrame, text=txt, anchor='w', width=40, font=('typo', font_size+2)).grid(column=1, columnspan=4, row=1)
        for i in range(0, 12):
            co = 1+i%4
            ro = 3+i//4
            card = hands[whos_turn()][i]
            image = ttk.Label(subFrame, image=select_card_pix[card], name='playercard {:0>2} {:0>2}'.format(i, card))
            image.grid(column=co, row=ro)
            if card in remain:
                remain.remove(card)
                image.bind('<Button-1>', click_handling)
            else:
                Label(subFrame, text='gelegt', fg='black', bg='yellow', height=1, width=6, font=('typo', font_size)).grid(column=co, row=ro)
        b = ttk.Button(subFrame, text="close")
        b.grid(column=3, columnspan=2, row=1, sticky='N')
        b.bind('<Button-1>', clear_subframe)


def show_moves():
    global subFrame
    destroy_subframe()
    subFrame = ttk.Frame(mainFrame)
    subFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
    for i in range(1, len(moves)):
        if moves[i][1] >= 0:
            co = 1+i%(3*ppp+3)
            ro = 4*(1+i//(3*ppp+3))-2
            ttk.Label(subFrame, image=hand_card_pix[moves[i][1]]).grid(row=ro, column=co)
            bg = 'gray94'
            if i%(ppp+1) == 1:
                bg = 'yellow'
                x = Label(subFrame, text='Runde {:d}'.format(1+i//(ppp+1)), fg='black', height=1, width=10, font=('typo', font_size-1))
                x.grid(column=co, row=ro-2, columnspan=2, sticky='SW')
            Label(subFrame, text=names(moves[i][0]), fg='black', bg=bg, height=1, width=8, font=('typo', font_size-1)).grid(column=co, row=ro-1)
        else:
            j = 1
            while moves[i-j][0] != moves[i][0]:
                j += 1
            co = 1+(i-j)%(3*ppp+3)
            ro = 4*(1+(i-j)//(3*ppp+3))-1
            Label(subFrame, text='Stich', fg='black', bg='yellow', height=1, width=5, font=('typo', font_size)).grid(column=co, row=ro-1)
    for i in range(0, 4):
        Label(subFrame, text='.', fg='gray', height=1, width=1, font=('typo', font_size-1)).grid(column=2+ppp, row=4*i+3)
        Label(subFrame, text='.', fg='gray', height=1, width=1, font=('typo', font_size-1)).grid(column=3+2*ppp, row=4*i+3)
    b = ttk.Button(subFrame, text="close")
    b.grid(column=20, row=0, columnspan=2)
    b.bind('<Button-1>', clear_subframe)


def clear_subframe(event):
    destroy_subframe()


def destroy_subframe():
    try:
        subFrame.destroy()
    except:
        pass


def requested_card():
    if len(moves) == 0:
        return 'Anspiel'
    elif moves[-1][1] < 0:
        return 'Anspiel'
    else:
        return card_type(moves[-((len(moves)-1)%(ppp+1))][1])


def card_type(card):
    if card <= 12:
        return 'Trumpf'
    elif card <= 16:
        return 'Kreuz'
    elif card <= 20:
        return 'Pik'
    else:
        return 'Herz'


def remaining_cards_on_hand(player):
    answer = deepcopy(hands[player])
    for m in moves:
        if m[0] == player and m[1] >= 0:
            answer.remove(m[1])
    return answer


def show_player_toggle_objects():
    global subFrameToggle
    objects = [[1, 1, ' Fuchs:'], [3, 1, 'von'], [1, 2, ' Fuchs:'], [3, 2, 'von'], [1, 3, ' Doko:'], [1, 4, ' Karlchen'], [1, 5, ' Re ang.'], [1, 6, ' Contra ang'], [1, 7, ' <90 ang.']]
    subFrameToggle = ttk.Frame(mainFrame)
    subFrameToggle.grid(column=7, row=14, rowspan=5, columnspan=4, sticky='nw')
    for i in range(0, len(objects)):
        x = Label(subFrameToggle, text=objects[i][2], font=('typo', font_size+2), fg='black', height=1, width=len(objects[i][2]), name='playertoggle_text {:0>2}'.format(i), justify=LEFT)
        x.grid(column=objects[i][0], row=objects[i][1], sticky='nw')
        if player_toggle_object[i] == -1:
            txt = '-'
        else:
            txt = names(player_toggle_object[i])
        y = Label(subFrameToggle, text=txt, font=('typo', font_size+2), fg='black', height=1, width=7, name='playertoggle {:0>2}'.format(i), justify=LEFT)
        y.grid(column=objects[i][0]+1, row=objects[i][1], sticky='nw')
        y.bind('<Button-1>', click_handling)


def show_player_selection():
    global subFramePlayer, selectplayervalue
    subFrameToggle = ttk.Frame(mainFrame)
    subFrameToggle.grid(column=18, row=13, rowspan=6, columnspan=2, sticky='w')
    selectplayervalue = [IntVar for i in range(0, 6)]
    for i in range(0, len(all_guys)):
        selectplayervalue[i] = Variable()
        bg='gray' + str(75+10*(i%2))
        x = Checkbutton(subFrameToggle, text=all_guys[i], variable=selectplayervalue[i], height=1, width=15, command=init_player_from_run,
                        font=('typo', font_size+3), fg='black', bg=bg, name='playerselect {:0>2}'.format(i), justify=LEFT)
        x.grid(column=1, columnspan=3, row=i, sticky='w')
        if selected_players[i] == 1:
            x.select()
        else:
            x.deselect()


def names(player):
    answer = []
    for i in range(0, len(all_guys)):
        if int(str(selectplayervalue[i].get())) == 1:
            answer.append(all_guys[i])
    answer.extend(['???' for i in range(0, 6)])
    return answer[player]


def dump_game(filename):
    fileobject = open(filename, "bw")
    pickle.dump([ppp, gamecode, moves, hands, ev, fool_block, contra_or_re, player_toggle_object, selected_players], fileobject)
    fileobject.close()


def load_game(filename):
    global ppp, gamecode, moves, hands, ev, fool_block, contra_or_re, player_toggle_object, selected_players
    if not(os.path.isfile(filename)):
        set_fresh_game_data(default_player_if_no_backup_exists, 0)
    else:
        fileobject = open(filename, "rb")
        game_instance = pickle.load(fileobject)
        ppp = game_instance[0]
        gamecode = game_instance[1]
        moves = game_instance[2]
        hands = game_instance[3]
        ev = game_instance[4]
        fool_block = game_instance[5]
        contra_or_re = game_instance[6]
        player_toggle_object = game_instance[7]
        selected_players = game_instance[8]


def set_fresh_game_data(player, seed):
    global ppp, gamecode, moves, hands, ev, fool_block, contra_or_re, player_toggle_object, selected_players
    selected_players = player
    derive_player_count(selected_players)
    gamecode = seed
    [hands, ev] = shuffle_iterator(gamecode, ppp)
    moves = []
    fool_block = (False, 'alles okay')
    contra_or_re = [0 for i in range(0, ppp)]
    player_toggle_object = [-1 for i in range(0, 99)]


def new_start():
    destroy_subframe()
    clear_away_tablecards()
    set_fresh_game_data(selected_players, gamecode)
    update_shown_content()


def update_shown_content():
    show_player_toggle_objects()
    show_gamecode()
    show_information()
    dump_game(filename_pkl)


if __name__ == '__main__':
    load_game(filename_pkl)
    init()
    arrange_tablecards()
    update_shown_content()
    mainFrame.mainloop()


## Ideen
# Anzeige letzte Züge im Hauptscreen (Migration)
# Anzahl verbleibende Karten auf der Hand im Hauptscreen (Migration)
# Sizing im Dialog (neu, aber nachrangig)
