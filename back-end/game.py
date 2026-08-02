import random
import numpy as np
from config import CONFIG
class Board:
    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', CONFIG['BOARD_WIDTH']))
        self.height = int(kwargs.get('height', CONFIG['BOARD_HEIGHT']))
        self.n_in_row = int(kwargs.get('n_in_row', CONFIG['N_IN_ROW']))
        self.players = (1, 2)
        self.states = {}
        self.current_player = None
        self.available = []
        self.last_move = -1
        self.last_move_player = 0
        self.history = []

    # 粘贴到 Board 类内部任意位置
    def auto_deed(self, over_pos, num, info):
        result_h = []
        result_b = []
        count1 = 0
        count2 = 0
        tmp1 = 1
        tmp2 = 1
        mp = np.zeros([17, 17], dtype=int)
        mp[0] = -1;mp[-1] = -1;mp[:,0] = -1;mp[:,-1] = -1
        for val in over_pos:
            x = int(((val[0][1] - 27) / 44)+1)
            y = int(((val[0][0] - 27) / 44)+1)
            if val[1] == 2:
                mp[x][y] = 2
            else:
                mp[x][y] = 1
        # 横向判断
        for i in range(1,16):
            pos1 = []
            pos2 = []
            tmp1 = 1
            tmp2 = 1
            for j in range(1,16):
                if mp[i][j] == 1:
                    pos1.append([i, j])
                elif mp[i][j] == 0 and tmp1 == 1:
                    while tmp1 + j < 15:
                        if mp[i][j+tmp1] == 1 and pos1:
                            tmp1 += 1
                        else:
                            break
                else:
                    pos1 = []
                    tmp1 = 1
                if mp[i][j] == 2:
                    pos2.append([i, j])
                elif mp[i][j] == 0 and tmp2 == 1:
                    while tmp2 + j < 15:
                        if mp[i][j+tmp2] == 2 and pos2:
                            tmp2 += 1
                        else:
                            break
                else:
                    pos2 = []
                    tmp2 = 1
                if len(pos1) >= num:
                    while num+count1+count2<5:
                        if j+count1+1<15:
                            if mp[i][j+count1+1] != 2:
                                count1 += 1
                            else:
                                if j-count2-num>=0:
                                    if mp[i][j-count2-num] != 2:
                                        count2 += 1
                                    else:
                                        break
                                else:
                                    break
                        elif j-count2-num>=0:
                            if mp[i][j-count2-num] != 2:
                                count2 += 1
                            else:
                                break
                        else:
                            break
                    if num+count1+count2>=5:
                        if tmp1 == 1:
                            if mp[i][j+1] == 0 and mp[i][j-num] == 0:
                                if j+2<15 and j-num-1>=0:
                                    if mp[i][j+2] != 2 and mp[i][j-num-1] != 2:
                                        result_h.append([1, random.choice(([i,j+1],[i,j-num])),0])
                                elif j+2<15:
                                    if mp[i][j+2] != 2:
                                        result_h.append([1,[i,j+1],0])
                                elif j-num-1>=0:
                                    if mp[i][j-1-num] != 2:
                                        result_h.append([1,[i,j-num],0])
                            elif mp[i][j+1] == 0:
                                result_h.append([1,[i,j+1],1])
                            elif mp[i][j-num] == 0:
                                result_h.append([1,[i,j-num],1])
                        else:
                            if mp[i][j+1] == 0 and mp[i][j-num-1] == 0:
                                result_h.append([1,[i,j-tmp1+1],0])
                            else:
                                result_h.append([1,[i,j-tmp1+1],1])
                        pos1 = []
                        count1 = 0
                        count2 = 0
                if len(pos2) >= num:
                    while num+count1+count2<5:
                        if j+count1+1<15:
                            if mp[i][j+count1+1] != 1:
                                count1 += 1
                            else:
                                if j-count2-num>=0:
                                    if mp[i][j-count2-num] != 1:
                                        count2 += 1
                                    else:
                                        break
                                else:
                                    break
                        elif j-count2-num>=0:
                            if mp[i][j-count2-num] != 1:
                                count2 += 1
                            else:
                                break
                        else:
                            break
                    if num+count1+count2>=5:
                        if tmp2 == 1:
                            if mp[i][j+1] == 0 and mp[i][j-num] == 0:
                                if j+2<15 and j-num-1>=0:
                                    if mp[i][j+2] != 1 and mp[i][j-num-1] != 1:
                                        result_b.append([1, random.choice(([i,j+1],[i,j-num])),0])
                                elif j+2<15:
                                    if mp[i][j+2] != 1:
                                        result_b.append([1,[i,j+1],0])
                                elif j-num-1>=0:
                                    if mp[i][j-1-num] != 1:
                                        result_b.append([1,[i,j-num],0])
                            elif mp[i][j+1] == 0:
                                result_b.append([1,[i,j+1],1])
                            elif mp[i][j-num] == 0:
                                result_b.append([1,[i,j-num],1])
                        else:
                            if mp[i][j+1] == 0 and mp[i][j-num-1] == 0:
                                result_b.append([1,[i,j-tmp2+1],0])
                            else:
                                result_b.append([1,[i,j-tmp2+1],1])
                        pos2 = []
                        count1 = 0
                        count2 = 0
        # 纵向
        tmp1 = 1
        tmp2 = 1
        for j in range(1,16):
            pos1 = []
            pos2 = []
            tmp1 = 1
            tmp2 = 1
            for i in range(1,16):
                if mp[i][j] == 1:
                    pos1.append([i, j])
                elif mp[i][j] == 0 and tmp1 == 1:
                    while i+tmp1<15:
                        if mp[i+tmp1][j] == 1 and pos1:
                            tmp1 += 1
                        else:
                            break
                else:
                    pos1 = []
                    tmp1 = 1
                if mp[i][j] == 2:
                    pos2.append([i, j])
                elif mp[i][j] == 0 and tmp2 == 1:
                    while i+tmp2<15:
                        if mp[i+tmp2][j] == 2 and pos2:
                            tmp2 += 1
                        else:
                                break
                else:
                    pos2 = []
                    tmp2 = 1
                if len(pos1) >= num:
                    while num+count1+count2<5:
                        if i+count1+1<15:
                            if mp[i+count1+1][j] != 2:
                                count1 += 1
                            else:
                                if i-num-count2>=0:
                                    if mp[i-num-count2][j] != 2:
                                        count2 += 1
                                    else:
                                        break
                                else:
                                    break
                        elif i-count2-num>=0:
                            if mp[i-count2-num][j] != 2:
                                count2 += 1
                            else:
                                break
                        else:
                            break
                    if num+count1+count2>=5:
                        if tmp1 ==1:
                            if mp[i+1][j] == 0 and mp[i-num][j] == 0:
                                if i+2<15 and i-num-1>=0:
                                    if mp[i+2][j] != 2 and mp[i-1-num][j] != 2:
                                        result_h.append([1, random.choice(([i+1,j],[i-num,j])),0])
                                elif i+2<15:
                                    if mp[i+2][j] != 2:
                                        result_h.append([1,[i+1,j],0])
                                elif i-num-1>=0:
                                    if mp[i-1-num][j] != 2:
                                        result_h.append([1,[i-num,j],0])
                            elif mp[i+1][j] == 0:
                                result_h.append([1,[i+1,j],1])
                            elif mp[i-num][j] == 0:
                                result_h.append([1,[i-num,j],1])
                        else:
                            if mp[i+1][j] == 0 and mp[i-num-1][j] == 0:
                                result_h.append([1, [i-tmp1+1,j],0])
                            else:
                                result_h.append([1, [i-tmp1+1,j],1])
                        pos1 = []
                        count1 = 0
                        count2 = 0
                if len(pos2) >= num:
                    while num+count1+count2<5:
                        if i+count1+1<15:
                            if mp[i+count1+1][j] != 1:
                                count1 += 1
                            else:
                                if i-num-count2>=0:
                                    if mp[i-num-count2][j] != 1:
                                        count2 += 1
                                    else:
                                        break
                                else:
                                    break
                        elif i-count2-num>=0:
                            if mp[i-count2-num][j] != 1:
                                count2 += 1
                            else:
                                break
                        else:
                            break
                    if num+count1+count2>=5:
                        if tmp2 == 1:
                            if mp[i+1][j] == 0 and mp[i-num][j] == 0:
                                if i+2<15 and i-num-1>=0:
                                    if mp[i+2][j] != 1 and mp[i-1-num][j] != 1:
                                        result_b.append([1, random.choice(([i+1,j],[i-num,j])),0])
                                elif i+2<15:
                                    if mp[i+2][j] != 1:
                                        result_b.append([1,[i+1,j],0])
                                elif i-num-1>=0:
                                    if mp[i-1-num][j] != 1:
                                        result_b.append([1,[i-num,j],0])
                            elif mp[i+1][j] == 0:
                                result_b.append([1,[i+1,j],1])
                            elif mp[i-num][j] == 0:
                                result_b.append([1,[i-num,j],1])
                        else:
                            if mp[i+1][j] == 0 and mp[i-num-1][j] == 0:
                                result_b.append([1, [i-tmp2+1,j],0])
                            else:
                                result_b.append([1, [i-tmp2+1,j],1])
                        pos2 = []
                        count1 = 0
                        count2 = 0
        # 右下斜线
        tmp1 = 1
        tmp2 = 1
        for i in range(1,16):
            tmp1 = 1
            tmp2 = 1
            for j in range(1,16):
                pos1 = []
                pos2 = []
                tmp1 = 1
                tmp2 = 1
                for k in range(num):
                    if i + k >= 15 or j + k >= 15:
                        break
                    if mp[i + k][j + k] == 1:
                        pos1.append([i + k, j + k])
                    elif mp[i+k][j+k] == 0 and tmp1 == 1:
                        while i+tmp1+k < 15 and j+k+tmp1 < 15:
                            if mp[i+k+tmp1][j+k+tmp1] == 1 and pos1:
                                tmp1 += 1
                            else:
                                break
                    else:
                        pos1 = []
                        tmp1 = 1
                    if mp[i + k][j + k] == 2:
                        pos2.append([i + k, j + k])
                    elif mp[i+k][j+k] == 0 and tmp2 == 1:
                        while i+tmp2+k < 15 and j+k+tmp2 < 15:
                            if mp[i+k+tmp2][j+k+tmp2] == 2 and pos2:
                                tmp2 += 1
                            else:
                                break
                    else:
                        pos2 = []
                        tmp2 = 1
                    if k == (num-1) and tmp1 != 1 and mp[i+num][j+num] == 1:
                        pos1.append([i+num,j+num])
                    if k == (num-1) and tmp2 != 1 and mp[i+num][j+num] == 2:
                        pos2.append([i+num,j+num])
                    if len(pos1) >=num:
                        while num+count1+count2<5:
                            if i+num+count1<15 and j+num+count1<15:
                                if mp[i+count1+num][j+num+count1] != 2:
                                    count1 += 1
                                else:
                                    if i-count2-1>=0 and j-count2-1>=0:
                                        if mp[i-count2-1][j-count2-1] != 2:
                                            count2 += 1
                                        else:
                                            break
                                    else:
                                        break
                            elif i-count2-1>=0 and j-count2-1>=0:
                                if mp[i-count2-1][j-count2-1] != 2:
                                    count2 += 1
                                else:
                                    break
                            else:
                                break
                        if num+count1+count2>=5:
                            if tmp1 == 1:
                                if mp[i+num][j+num] == 0 and mp[i-1][j-1] == 0:
                                    if i+num+1<15 and j+num+1<15 and i-2 >=0 and j-2>=0:
                                        if mp[i+num+1][j+num+1] != 2 and mp[i-2][j-2] != 2:
                                            result_h.append([1, random.choice(([i+num,j+num],[i-1,j-1])),0])
                                    elif i+num+1<15 and j+num+1<15:
                                        if mp[i+num+1][j+num+1] != 2:
                                            result_h.append([1,[i+num,j+num],0])
                                    elif i-2 >=0 and j-2>=0:
                                        if mp[i-2][j-2] != 2:
                                            result_h.append([1,[i-1,j-1],0])
                                elif mp[i+num][j+num] == 0:
                                    result_h.append([1,[i+num,j+num],1])
                                elif mp[i-1][j-1] == 0:
                                    result_h.append([1,[i-1,j-1],1])
                            else:
                                if mp[i+num+1][j+num+1] == 0 and mp[i-1][j-1] == 0:
                                    result_h.append([1,[i+num-tmp1+1,j+num-tmp1+1],0])
                                else:
                                    result_h.append([1,[i+num-tmp1+1,j+num-tmp1+1],1])
                        pos1 = []
                        count1 = 0
                        count2 = 0
                    if len(pos2) >= num:
                        while num+count1+count2<5:
                            if i+num+count1<15 and j+num+count1<15:
                                if mp[i+count1+num][j+num+count1] != 1:
                                    count1 += 1
                                else:
                                    if i-count2-1>=0 and j-count2-1>=0:
                                        if mp[i-count2-1][j-count2-1] != 1:
                                            count2 += 1
                                        else:
                                            break
                                    else:
                                        break
                            elif i-count2-1>=0 and j-count2-1>=0:
                                if mp[i-count2-1][j-count2-1] != 1:
                                    count2 += 1
                                else:
                                    break
                            else:
                                break
                        if num+count1+count2>=5:
                            if tmp2 == 1:
                                if mp[i+num][j+num] == 0 and mp[i-1][j-1] == 0:
                                    if i+num+1<15 and j+num+1<15 and i-2 >=0 and j-2>=0:
                                        if mp[i+num+1][j+num+1] != 1 and mp[i-2][j-2] != 1:
                                                result_b.append([1, random.choice(([i+num,j+num],[i-1,j-1])),0])
                                    elif i+num+1<15 and j+num+1<15:
                                        if mp[i+num+1][j+num+1] != 1:
                                                result_b.append([1,[i+num,j+num],0])
                                    elif i-2 >=0 and j-2>=0:
                                        if mp[i-2][j-2] != 1:
                                                result_b.append([1,[i-1,j-1],0])
                                elif mp[i+num][j+num] == 0:
                                        result_b.append([1,[i+num,j+num],1])
                                elif mp[i-1][j-1] == 0:
                                        result_b.append([1,[i-1,j-1],1])
                            else:
                                if mp[i+num+1][j+num+1] == 0 and mp[i-1][j-1] == 0:
                                    result_b.append([1,[i+num+1-tmp2,j+num+1-tmp2],0])
                                else:
                                    result_b.append([1,[i+num+1-tmp2,j+num+1-tmp2],1])
                        pos2 = []
                        count1 = 0
                        count2 = 0
        # 左上斜线
        tmp1 = 1
        tmp2 = 1
        for i in range(1,16):
            tmp1 = 0
            tmp2 = 0
            for j in range(1,16):
                pos1 = []
                pos2 = []
                tmp1 = 1
                tmp2 = 1
                for k in range(num):
                    if i + k >= 15 or j - k < 0:
                        break
                    if mp[i + k][j - k] == 1:
                        pos1.append([i + k, j - k])
                    elif mp[i + k][j - k] == 0 and tmp1 == 1:
                        while i+k+tmp1<15 and j-k-tmp1>=0:
                            if mp[i+k+tmp1][j-k-tmp1] == 1 and pos1:
                                tmp1 += 1
                            else:
                                break
                    else:
                        pos1 = []
                        tmp1 = 1
                    if mp[i + k][j - k] == 2:
                        pos2.append([i + k, j - k])
                    elif mp[i + k][j - k] == 0 and tmp2 == 1:
                        while i+k+tmp2<15 and j-k-tmp2>=0:
                            if mp[i+k+tmp2][j-k-tmp2] == 2 and pos2:
                                tmp2 += 1
                            else:
                                break
                    else:
                        pos2 = []
                        tmp2 = 1
                    if k == (num-1) and tmp1 != 1 and mp[i+num][j-num] == 1:
                        pos1.append([i+num,j-num])
                    if k == (num-1) and tmp2 != 1 and mp[i+num][j-num] == 2:
                        pos2.append([i+num,j-num])
                    if len(pos1) >= num:
                        while num+count1+count2<5:
                            if i+num+count1<15 and j-num-count1>=0:
                                if mp[i+num+count1][j-num-count1] != 2:
                                    count1 += 1
                                else:
                                    if i-count2-1>=0 and j+count2+1<15:
                                        if mp[i-count2-1][j+count2+1] != 2:
                                            count2 += 1
                                        else:
                                            break
                                    else:
                                        break
                            elif i-count2-1>=0 and j+count2+1<15:
                                if mp[i-count2-1][j+count2+1] != 2:
                                    count2 += 1
                                else:
                                    break
                            else:
                                break
                        if num+count1+count2>=5:
                            if tmp1 == 1:
                                if mp[i+num][j-num] == 0 and mp[i-1][j+1] == 0:
                                    if i+num+1<15 and j-num-1>=0 and i-2 >=0 and j+2<15:
                                        if mp[i+num+1][j-num-1] != 2 and mp[i-2][j+2] != 2:
                                            result_h.append([1, random.choice(([i+num,j-num],[i-1,j+1])),0])
                                    elif i+num+1<15 and j-num-1>=0:
                                        if mp[i+num+1][j-num-1] != 2:
                                            result_h.append([1,[i+num,j-num],0])
                                    elif i-2 >=0 and j+2<15:
                                        if mp[i-2][j+2] != 2:
                                            result_h.append([1,[i-1,j+1],0])
                                elif mp[i+num][j-num] == 0:
                                    result_h.append([1,[i+num,j-num],1])
                                elif mp[i-1][j+1] == 0:
                                    result_h.append([1,[i-1,j+1],1])
                            else:
                                if mp[i+num+1][j-num-1] == 0 and mp[i-1][j+1] == 0:
                                    result_h.append([1,[i+num-tmp1+1,j-num+tmp1-1],0])
                                else:
                                    result_h.append([1,[i+num-tmp1+1,j-num+tmp1-1],1])
                        pos1 = []
                        count1 = 0
                        count2 = 0
                    if len(pos2) >= num:
                        while num+count1+count2<5:
                            if i+num+count1<15 and j-num-count1>=0:
                                if mp[i+num+count1][j-num-count1] != 1:
                                    count1 += 1
                                else:
                                    if i-count2-1>=0 and j+count2+1<15:
                                        if mp[i-count2-1][j+count2+1] != 1:
                                            count2 += 1
                                        else:
                                            break
                                    else:
                                        break
                            elif i-count2-1>=0 and j+count2+1<15:
                                if mp[i-count2-1][j+count2+1] != 1:
                                    count2 += 1
                                else:
                                    break
                            else:
                                break
                        if num+count1+count2>=5:
                            if tmp2 == 1:
                                if mp[i+num][j-num] == 0 and mp[i-1][j+1] == 0:
                                    if i+num+1<15 and j-num-1>=0 and i-2 >=0 and j+2<15:
                                        if mp[i+num+1][j-num-1] != 1 and mp[i-2][j+2] != 1:
                                            result_b.append([1, random.choice(([i+num,j-num],[i-1,j+1])),0])
                                    elif i+num+1<15 and j-num-1>=0:
                                        if mp[i+num+1][j-num-1] != 1:
                                            result_b.append([1,[i+num,j-num],0])
                                    elif i-2 >=0 and j+2<15:
                                        if mp[i-2][j+2] != 1:
                                            result_b.append([1,[i-1,j+1],0])
                                elif mp[i+num][j-num] == 0:
                                    result_b.append([1,[i+num,j-num],1])
                                elif mp[i-1][j+1] == 0:
                                    result_b.append([1,[i-1,j+1],1])
                            else:
                                if mp[i+num+1][j-num-1] == 0 and mp[i-1][j+1] == 0:
                                    result_b.append([1,[i+num-tmp2+1,j-num+tmp2-1],0])
                                else:
                                    result_b.append([1,[i+num-tmp2+1,j-num+tmp2-1],1])
                        pos2 = []
                        count1 = 0
                        count2 = 0
        result_h.sort(key=lambda x:x[2])
        result_b.sort(key=lambda x:x[2])
        if result_b == [] and result_h == []:
            return [0, []]
        else:
            if info == "h":
                if result_h:
                    result_h.sort(key=lambda x:x[2])
                    return list(map(lambda x:x[1],result_h))
                else:
                    result_b.sort(key=lambda x:x[2])
                    return list(map(lambda x:x[1],result_b))
            else:
                if result_b:
                    result_b.sort(key=lambda x:x[2])
                    return list(map(lambda x:x[1],result_b))
                else:
                    result_h.sort(key=lambda x:x[2])
                    return list(map(lambda x:x[1],result_h))

    def init_board(self, start_player=0):
        if self.width < self.n_in_row or self.height < self.n_in_row:
            raise Exception('board width and height can not be less than {}'.format(self.n_in_row))
        self.current_player = self.players[start_player]
        self.available = list(range(self.width * self.height))
        self.states = {}
        self.last_move = -1
        self.last_move_player = 0
        self.history = []

    def force_to_state(self, states, current_player, last_move):
        self.states = states
        self.current_player = current_player
        self.available = list(range(self.width * self.height))
        for move in self.states:
            if move in self.available:
                self.available.remove(move)
        self.last_move = last_move
        if self.states:
            self.last_move_player = self.states.get(last_move, 0)
        else:
            self.last_move_player = 0

    def move_to_location(self, move):
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def do_move(self, move, player=None):
        # 兼容两种调用：
        # 1. AI/MCTS：只传 move，自动取 self.current_player
        # 2. 联机双人：传 move, player，优先使用外部传入玩家
        if player is None:
            player = self.current_player
        if move not in self.available:
            return False
        self.states[move] = player
        self.available.remove(move)
        self.last_move = move
        self.last_move_player = player
        self.history.append((move, player))
        return True

    def get_current_player(self):
        return self.current_player

    def current_state(self):
        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0
            square_state[2][self.last_move // self.width, self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0
        return square_state[:, ::-1, :]

    def has_a_winner(self):
        # 棋盘完全空白，直接判定没有胜利者，杜绝空棋盘判赢
        if len(self.states) == 0:
            return False, -1
        # 落子少于5颗棋子，五子连线不可能达成，直接跳过判定
        if len(self.states) < 5:
            return False, -1
        move = self.last_move
        player = self.states[move]
        row, col = self.move_to_location(move)
        w = self.width
        h = self.height
        dir_list = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in dir_list:
            cnt = 1
            r, c = row + dr, col + dc
            while 0 <= r < h and 0 <= c < w:
                idx = r * w + c
                if self.states.get(idx, 0) == player:
                    cnt += 1
                    r += dr
                    c += dc
                else:
                    break
            r, c = row - dr, col - dc
            while 0 <= r < h and 0 <= c < w:
                idx = r * w + c
                if self.states.get(idx, 0) == player:
                    cnt += 1
                    r -= dr
                    c -= dc
                else:
                    break
            if cnt >= self.n_in_row:
                return True, player
        return False, -1

    def undo_last_move(self):
        if not self.history:
            return False, -1
        move, player = self.history.pop()
        self.states.pop(move, None)
        if move not in self.available:
            self.available.append(move)
        self.last_move = self.history[-1][0] if self.history else -1
        self.last_move_player = self.history[-1][1] if self.history else 0
        return True, player

    def game_end(self):
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.available):
            return True, -1
        return False, -1

class Game:
    def __init__(self, board: Board):
        self.board = board

    def start_self_play(self, player, is_shown=False, temp=1e-3):
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            self.board.do_move(move)
            self.board.current_player = p2 if self.board.current_player == p1 else p1
            if is_shown:
                self.graphic(self.board, p1, p2)
            end, winner = self.board.game_end()
            if end:
                winner_z = np.zeros(len(current_players))
                if winner != -1:
                    winner_z[np.array(current_players) == winner] = 1.0
                    winner_z[np.array(current_players) != winner] = -1.0
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player: ", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winner_z)

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        if start_player not in (0, 1):
            raise Exception('start_player should be either 0 or 1')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:
            self.graphic(self.board, player1.player, player2.player)
        while True:
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            self.board.current_player = p2 if self.board.current_player == p1 else p1
            if is_shown:
                self.graphic(self.board, player1.player, player2.player)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is ", players[winner])
                    else:
                        print("Game end. Tie")
                return winner

    def graphic(self, board, player1, player2):
        width = board.width
        height = board.height

        print("Player", player1, "with X".rjust(3))
        print("Player", player2, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:4}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:2d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    print('x'.center(4), end='')
                elif p == player2:
                    print('O'.center(4), end='')
                else:
                    print('_'.center(4), end='')
            print('\r\n')
