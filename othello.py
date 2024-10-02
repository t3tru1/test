import numpy as np
import time

def othello():
    player_num = 1 #player番号は計算しやすいように１とー１
    count = 0
    game_list = np.zeros((9,9))
    game_list[3,3] = game_list[4,4] = 1
    game_list[4,3] = game_list[3,4] = -1 #ボード準備
    
    while True:
        if(count == 2): #両方置けないとき終わり
            end(sum)
            break
        
        put = can_put(game_list, player_num) #置く場所あるか
        
        sum = np.sum(game_list) #合計が+ならplayer1,-ならplayer2,0なら引き分け
        
        while True:
            board_display(game_list) #ボード表示
            if(put == 0): #置けないときの表示
                print("\n\n################")
                print("##置く場所なし##")
                print("################\n\n")
                count += 1
                time.sleep(1)
                break
            y,x = xy_entry(player_num) #入力
            if(y == 99): #テスト用 s が入力されたらスキップ
                count += 1
                break
            error_num = is_space(game_list, x, y, player_num, 0) #スペースなかったり、おいても返せないときはエラー
            if(error_num != 0):
                count = 0
                break
        
        player_num *= -1
    

def board_display(game_list): #ボードを表示
    print("  ",end="")
    for i in range(1,9):
        print(i, end=(" "))
    
    print()

    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            if(game_list[i][j] == 0):
                print("-", end=" ")
            elif(game_list[i][j] == 1):
                print("O", end=" ")
            elif(game_list[i][j] == -1):
                print("X",end=" ")
        print()

def xy_entry(player_num): #座標入力 テストを簡単にやるためsでスキップ
    while True:
        piece = {1 : 'O', -1 : 'X'}
        print("Player", player_num, "[",piece[player_num],"]", "座標(行、列)を入力！例(3 5)")
        #y,x = input().split()
        A = input()
        
        A_list = list(A) #置き間違えのエラー対策
        if(len(A_list) != 3):
            continue
        
        if(A_list[0] == 's'):#sが入力されたらスキップ(99返す)
            return 99,99
        # elif(A_list[2] == 9):
        #     continue

        y = int(A_list[0])
        x = int(A_list[2])
        break
    return y - 1, x - 1
#入力エラー対策はちゃんとできてないyo

def is_space(game_list, x, y, player_num, n): #入力した場所が開いているか
    y_n = y
    x_n = x
    error_num = 0
    
    direction = np.array([ #8方向のベクトル
        [-1,0],#top
        [-1,1],#top_right
        [0,1],#right
        [1,1],#bottom_right
        [1,0],#bottom
        [1,-1],#bottom_left
        [0,-1],#left
        [-1,-1]#top_left
    ])
    
    for i in range(8):#全方向見て相手の駒あるか見る
        d_y = direction[i][0]
        d_x = direction[i][1]
        y += d_y
        x += d_x
        if(game_list[y][x] == (player_num * -1)):
            l = is_turn_over(game_list, x, y, player_num,d_y, d_x, 0) #相手の駒あったらひっくりかえせるか見る
            if(l != 0 and l != None and n == 0):
                    turn_over(game_list, y_n, x_n, d_y, d_x, l, player_num) #ひっくりかえせるときひっくりかえす
                    error_num = 1
            elif(l != 0 and l != None and n == 1):
                error_num = 1

        y = y_n
        x = x_n

    return error_num

def is_turn_over(game_list, x, y, player_num, d_y, d_x, l): #ひっくりかえせるか見る
    while True:
        y += d_y
        x += d_x
        l += 1
        if(game_list[y][x] == player_num):
            return l
        elif(game_list[y][x] == (player_num * -1)):
            continue
        return 0

def turn_over(game_list, y_n, x_n, d_y, d_x, l, player_num): #ひっくり返す
    game_list[y_n][x_n] = player_num
    for i in range(l):
        y_n += d_y
        x_n += d_x
        game_list[y_n][x_n] = player_num

def can_put(game_list, player_num): #置ける場所があるかみる(勝敗判定用)
    result = 0
    for i in range(8):
        for j in range(8):
            x = i
            y = j
            result += is_space(game_list, x, y, player_num, 1)
    
    if(result != 0):
        return 1
    return 0

def end(sum): #勝敗表示
    if(sum > 0):
        print("WINNER PLAYER1 O")
    elif(sum < 0):
        print("WINNER PLAYER2 X")
    else:
        print("DRAW")

othello() #実行!!v(・3・)v