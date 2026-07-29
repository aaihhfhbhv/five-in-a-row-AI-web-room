import random


def get_auto_move(states, player, width, height, n_in_row=5):
    if not states:
        return 0

    available_moves = [move for move in range(width * height) if move not in states]
    if not available_moves:
        return -1

    # 1) 优先下赢棋
    for move in available_moves:
        next_states = dict(states)
        next_states[move] = player
        if _has_winning_line(next_states, move, player, width, height, n_in_row):
            return move

    # 2) 拦截对手的即刻胜招
    opponent = 3 - player
    for move in available_moves:
        next_states = dict(states)
        next_states[move] = opponent
        if _has_winning_line(next_states, move, opponent, width, height, n_in_row):
            return move

    # 3) 选择最中心的空位，避免边缘
    best_moves = sorted(available_moves, key=lambda m: abs((m // width) - (height // 2)) + abs((m % width) - (width // 2)))
    return best_moves[0]


def _has_winning_line(states, move, player, width, height, n_in_row):
    row, col = divmod(move, width)
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in range(1, n_in_row):
            nr = row + dr * step
            nc = col + dc * step
            if 0 <= nr < height and 0 <= nc < width and states.get(nr * width + nc) == player:
                count += 1
            else:
                break
        for step in range(1, n_in_row):
            nr = row - dr * step
            nc = col - dc * step
            if 0 <= nr < height and 0 <= nc < width and states.get(nr * width + nc) == player:
                count += 1
            else:
                break
        if count >= n_in_row:
            return True
    return False


# def auto_deed(self, over_pos, num, info):
#     print(111111111111111111111)
#     result_h = []
#     result_b = []
#     count1 = 0
#     count2 = 0
#     tmp1 = 1
#     tmp2 = 1
#     mp = np.zeros([17, 17], dtype=int)
#     mp[0] = -1;mp[-1] = -1;mp[:,0] = -1;mp[:,-1] = -1
#     for val in over_pos:
#         x = int(((val[0][1] - 27) / 44)+1)
#         y = int(((val[0][0] - 27) / 44)+1)
#         if val[1] == self.white_color:
#             mp[x][y] = 2  # 表示白子
#         else:
#             mp[x][y] = 1  # 表示黑子
#     for i in range(1,16):
#         pos1 = []
#         pos2 = []
#         tmp1 = 1
#         tmp2 = 1
#         for j in range(1,16):
#             if mp[i][j] == 1:
#                 pos1.append([i, j])
#             elif mp[i][j] == 0 and tmp1 == 1:
#                 while tmp1 + j < 15:
#                     if mp[i][j+tmp1] == 1 and pos1:
#                         tmp1 += 1
#                     else:
#                         break
#             else:
#                 pos1 = []
#                 tmp1 = 1
#             if mp[i][j] == 2:
#                 pos2.append([i, j])
#             elif mp[i][j] == 0 and tmp2 == 1:
#                 while tmp2 + j < 15:
#                     if mp[i][j+tmp2] == 2 and pos2:
#                         tmp2 += 1
#                     else:
#                         break
#             else:
#                 pos2 = []
#                 tmp2 = 1
#             if len(pos1) >= num:
#                 while num+count1+count2<5:
#                     if j+count1+1<15:
#                         if mp[i][j+count1+1] != 2:
#                             count1 += 1
#                         else:
#                             if j-count2-num>=0:
#                                 if mp[i][j-count2-num] != 2:
#                                     count2 += 1
#                                 else:
#                                     break
#                             else:
#                                 break
#                     elif j-count2-num>=0:
#                         if mp[i][j-count2-num] != 2:
#                             count2 += 1
#                         else:
#                             break
#                     else:
#                         break
#                 if num+count1+count2>=5:    # 有下棋的意义
#                     if tmp1 == 1:
#                         if mp[i][j+1] == 0 and mp[i][j-num] == 0:
#                             if j+2<15 and j-num-1>=0:
#                                 if mp[i][j+2] != 2 and mp[i][j-num-1] != 2:
#                                     result_h.append([1, random.choice(([i,j+1],[i,j-num])),0])
#                             elif j+2<15:
#                                 if mp[i][j+2] != 2:
#                                     result_h.append([1,[i,j+1],0])                                        
#                             elif j-num-1>=0:
#                                 if mp[i][j-1-num] != 2:
#                                     result_h.append([1,[i,j-num],0])                                        
#                         elif mp[i][j+1] == 0:
#                             result_h.append([1,[i,j+1],1])                                
#                         elif mp[i][j-num] == 0:
#                             result_h.append([1,[i,j-num],1])
#                     else:
#                         if mp[i][j+1] == 0 and mp[i][j-num-1] == 0:
#                             result_h.append([1,[i,j-tmp1+1],0])
#                         else:
#                             result_h.append([1,[i,j-tmp1+1],1])
#                 pos1 = []
#                 count1 = 0
#                 count2 = 0

#             if len(pos2) >= num:
#                 while num+count1+count2<5:
#                     if j+count1+1<15:
#                         if mp[i][j+count1+1] != 1:
#                             count1 += 1
#                         else:
#                             if j-count2-num>=0:
#                                 if mp[i][j-count2-num] != 1:
#                                     count2 += 1
#                                 else:
#                                     break
#                             else:
#                                 break
#                     elif j-count2-num>=0:
#                         if mp[i][j-count2-num] != 1:
#                             count2 += 1
#                         else:
#                             break
#                     else:
#                         break
#                 if num+count1+count2>=5:    # 有下棋的意义
#                     if tmp2 == 1:
#                         if mp[i][j+1] == 0 and mp[i][j-num] == 0:
#                             if j+2<15 and j-num-1>=0:
#                                 if mp[i][j+2] != 1 and mp[i][j-num-1] != 1:
#                                     result_b.append([1, random.choice(([i,j+1],[i,j-num])),0])
#                             elif j+2<15:
#                                 if mp[i][j+2] != 1:
#                                     result_b.append([1,[i,j+1],0])
#                             elif j-num-1>=0:
#                                 if mp[i][j-1-num] != 1:
#                                     result_b.append([1,[i,j-num],0])     
#                         elif mp[i][j+1] == 0:
#                             result_b.append([1,[i,j+1],1])
#                         elif mp[i][j-num] == 0:
#                             result_b.append([1,[i,j-num],1])
#                     else:
#                         if mp[i][j+1] == 0 and mp[i][j-num-1] == 0:
#                             result_b.append([1,[i,j-tmp2+1],0])
#                         else:
#                             result_b.append([1,[i,j-tmp2+1],1])

#                 pos2 = []
#                 count1 = 0
#                 count2 = 0
    
    
#     tmp1 = 1
#     tmp2 = 1
#     for j in range(1,16):
#         pos1 = []
#         pos2 = []
#         tmp1 = 1
#         tmp2 = 1
#         for i in range(1,16):
#             if mp[i][j] == 1:
#                 pos1.append([i, j])
#             elif mp[i][j] == 0 and tmp1 == 1:
#                 while tmp1 + i < 15:
#                     if mp[i+tmp1][j] == 1 and pos1:
#                         tmp1 += 1
#                     else:
#                         break
#             else:
#                 pos1 = []
#                 tmp1 = 1
#             if mp[i][j] == 2:
#                 pos2.append([i, j])
#             elif mp[i][j] == 0 and tmp2 == 1:
#                 while i+tmp2<15:
#                     if mp[i+tmp2][j] == 2 and pos2:
#                         tmp2 += 1
#                     else:
#                             break
#             else:
#                 pos2 = []
#                 tmp2 = 1
#             if len(pos1) >= num:
#                 while num+count1+count2<5:
#                     if i+count1+1<15:
#                         if mp[i+count1+1][j] != 2:
#                             count1 += 1
#                         else:
#                             if i-num-count2>=0:
#                                 if mp[i-num-count2][j] != 2:
#                                     count2 += 1
#                                 else:
#                                     break
#                             else:
#                                 break
#                     elif i-count2-num>=0:
#                         if mp[i-count2-num][j] != 2:
#                             count2 += 1
#                         else:
#                             break
#                     else:
#                         break
#                 if num+count1+count2>=5:    # 有下棋的意义
#                     if tmp1 ==1:
#                         if mp[i+1][j] == 0 and mp[i-num][j] == 0:
#                             if i+2<15 and i-num-1>=0:
#                                 if mp[i+2][j] != 2 and mp[i-1-num][j] != 2:
#                                     result_h.append([1, random.choice(([i+1,j],[i-num,j])),0])
#                             elif i+2<15:
#                                 if mp[i+2][j] != 2:
#                                     result_h.append([1,[i+1,j],0])  
#                             elif i-num-1>=0:
#                                 if mp[i-1-num][j] != 2:
#                                     result_h.append([1,[i-num,j],0])
#                         elif mp[i+1][j] == 0:
#                             result_h.append([1,[i+1,j],1])
#                         elif mp[i-num][j] == 0:
#                             result_h.append([1,[i-num,j],1])
#                     else:
#                         if mp[i+1][j] == 0 and mp[i-num-1][j] == 0:
#                             result_h.append([1, [i-tmp1+1,j],0])
#                         else:
#                             result_h.append([1, [i-tmp1+1,j],1])
#                 pos1 = []
#                 count1 = 0
#                 count2 = 0
#             if len(pos2) >= num:
#                 while num+count1+count2<5:
#                     if i+count1+1<15:
#                         if mp[i+count1+1][j] != 1:
#                             count1 += 1
#                         else:
#                             if i-num-count2>=0:
#                                 if mp[i-num-count2][j] != 1:
#                                     count2 += 1
#                                 else:
#                                     break
#                             else:
#                                 break
#                     elif i-count2-num>=0:
#                         if mp[i-count2-num][j] != 1:
#                             count2 += 1
#                         else:
#                             break
#                     else:
#                         break
#                 if num+count1+count2>=5:    # 有下棋的意义
#                     if tmp2 == 1:
#                         if mp[i+1][j] == 0 and mp[i-num][j] == 0:
#                             if i+2<15 and i-num-1>=0:
#                                 if mp[i+2][j] != 1 and mp[i-1-num][j] != 1:
#                                     result_b.append([1, random.choice(([i+1,j],[i-num,j])),0])
#                             elif i+2<15:
#                                 if mp[i+2][j] != 1:
#                                     result_b.append([1,[i+1,j],0])
#                             elif i-num-1>=0:
#                                 if mp[i-1-num][j] != 1:
#                                     result_b.append([1,[i-num,j],0])
#                         elif mp[i+1][j] == 0:
#                             result_b.append([1,[i+1,j],1])
#                         elif mp[i-num][j] == 0:
#                             result_b.append([1,[i-num,j],1])
#                     else:
#                         if mp[i+1][j] == 0 and mp[i-num-1][j] == 0:
#                             result_b.append([1, [i-tmp2+1,j],0])
#                         else:
#                             result_b.append([1, [i-tmp2+1,j],1])
#                 pos2 = []
#                 count1 = 0
#                 count2 = 0

#     tmp1 = 1
#     tmp2 = 1
#     for i in range(1,16):
#         tmp1 = 1
#         tmp2 = 1
#         for j in range(1,16):
#             pos1 = []
#             pos2 = []
#             tmp1 = 1
#             tmp2 = 1
#             for k in range(num):
#                 if i + k >= 15 or j + k >= 15:
#                     break
#                 if mp[i + k][j + k] == 1:
#                     pos1.append([i + k, j + k])
#                 elif mp[i+k][j+k] == 0 and tmp1 == 1:
#                     while i+tmp1+k < 15 and j+k+tmp1 < 15:
#                         if mp[i+k+tmp1][j+k+tmp1] == 1 and pos1:
#                             tmp1 += 1
#                         else:
#                             break
#                 else:
#                     pos1 = []
#                     tmp1 = 1
#                 if mp[i + k][j + k] == 2:
#                     pos2.append([i + k, j + k])
#                 elif mp[i+k][j+k] == 0 and tmp2 == 1:
#                     while i+tmp2+k < 15 and j+k+tmp2 < 15:
#                         if mp[i+k+tmp2][j+k+tmp2] == 2 and pos2:
#                             tmp2 += 1
#                         else:
#                             break
#                 else:
#                     pos2 = []
#                     tmp2 = 1
#                 if k == (num-1) and tmp1 != 1 and mp[i+num][j+num] == 1:
#                     pos1.append([i+num,j+num])
#                 if k == (num-1) and tmp2 != 1 and mp[i+num][j+num] == 2:
#                     pos2.append([i+num,j+num])
#                 if len(pos1) >=num:
#                     while num+count1+count2<5:
#                         if i+num+count1<15 and j+num+count1<15:
#                             if mp[i+count1+num][j+num+count1] != 2:
#                                 count1 += 1
#                             else:
#                                 if i-count2-1>=0 and j-count2-1>=0:
#                                     if mp[i-count2-1][j-count2-1] != 2:
#                                         count2 += 1
#                                     else:
#                                         break
#                                 else:
#                                     break
#                         elif i-count2-1>=0 and j-count2-1>=0:
#                             if mp[i-count2-1][j-count2-1] != 2:
#                                 count2 += 1
#                             else:
#                                 break
#                         else:
#                             break
#                     if num+count1+count2>=5:    # 有下棋的意义
#                         if tmp1 == 1:
#                             if mp[i+num][j+num] == 0 and mp[i-1][j-1] == 0:
#                                 if i+num+1<15 and j+num+1<15 and i-2 >=0 and j-2>=0:
#                                     if mp[i+num+1][j+num+1] != 2 and mp[i-2][j-2] != 2:
#                                         result_h.append([1, random.choice(([i+num,j+num],[i-1,j-1])),0])
#                                 elif i+num+1<15 and j+num+1<15:
#                                     if mp[i+num+1][j+num+1] != 2:
#                                         result_h.append([1,[i+num,j+num],0])
#                                 elif i-2 >=0 and j-2>=0:
#                                     if mp[i-2][j-2] != 2:
#                                         result_h.append([1,[i-1,j-1],0])
#                             elif mp[i+num][j+num] == 0:
#                                 result_h.append([1,[i+num,j+num],1])
#                             elif mp[i-1][j-1] == 0:
#                                 result_h.append([1,[i-1,j-1],1])
#                         else:
#                             if mp[i+num+1][j+num+1] == 0 and mp[i-1][j-1] == 0:
#                                 result_h.append([1,[i+num-tmp1+1,j+num-tmp1+1],0])
#                             else:
#                                 result_h.append([1,[i+num-tmp1+1,j+num-tmp1+1],1])
#                     pos1 = []
#                     count1 = 0
#                     count2 = 0
#                 if len(pos2) >= num:
#                     while num+count1+count2<5:
#                         if i+num+count1<15 and j+num+count1<15:
#                             if mp[i+count1+num][j+num+count1] != 1:
#                                 count1 += 1
#                             else:
#                                 if i-count2-1>=0 and j-count2-1>=0:
#                                     if mp[i-count2-1][j-count2-1] != 1:
#                                         count2 += 1
#                                     else:
#                                         break
#                                 else:
#                                     break
#                         elif i-count2-1>=0 and j-count2-1>=0:
#                             if mp[i-count2-1][j-count2-1] != 1:
#                                 count2 += 1
#                             else:
#                                 break
#                         else:
#                             break
#                     if num+count1+count2>=5:    # 有下棋的意义
#                         if tmp2 == 1:
#                             if mp[i+num][j+num] == 0 and mp[i-1][j-1] == 0:
#                                 if i+num+1<15 and j+num+1<15 and i-2 >=0 and j-2>=0:
#                                     if mp[i+num+1][j+num+1] != 1 and mp[i-2][j-2] != 1:
#                                             result_b.append([1, random.choice(([i+num,j+num],[i-1,j-1])),0])
#                                 elif i+num+1<15 and j+num+1<15:
#                                     if mp[i+num+1][j+num+1] != 1:
#                                             result_b.append([1,[i+num,j+num],0])
#                                 elif i-2 >=0 and j-2>=0:
#                                     if mp[i-2][j-2] != 1:
#                                             result_b.append([1,[i-1,j-1],0])
#                             elif mp[i+num][j+num] == 0:
#                                     result_b.append([1,[i+num,j+num],1])
#                             elif mp[i-1][j-1] == 0:
#                                     result_b.append([1,[i-1,j-1],1])
#                         else:
#                             if mp[i+num+1][j+num+1] == 0 and mp[i-1][j-1] == 0:
#                                 result_b.append([1,[i+num+1-tmp2,j+num+1-tmp2],0])
#                             else:
#                                 result_b.append([1,[i+num+1-tmp2,j+num+1-tmp2],1])
#                     pos2 = []
#                     count1 = 0
#                     count2 = 0

#     tmp1 = 1
#     tmp2 = 1
#     for i in range(1,16):
#         tmp1 = 0
#         tmp2 = 0
#         for j in range(1,16):
#             pos1 = []
#             pos2 = []
#             tmp1 = 1
#             tmp2 = 1
#             for k in range(num):
#                 if i + k >= 15 or j - k < 0:
#                     break
#                 if mp[i + k][j - k] == 1:
#                     pos1.append([i + k, j - k])
#                 elif mp[i + k][j - k] == 0 and tmp1 == 1:
#                     while i+k+tmp1<15 and j-k-tmp1>=0:
#                         if mp[i+k+tmp1][j-k-tmp1] == 1 and pos1:
#                             tmp1 += 1
#                         else:
#                             break
#                 else:
#                     pos1 = []
#                     tmp1 = 1
#                 if mp[i + k][j - k] == 2:
#                     pos2.append([i + k, j - k])
#                 elif mp[i + k][j - k] == 0 and tmp2 == 1:
#                     while i+k+tmp2<15 and j-k-tmp2>=0:
#                         if mp[i+k+tmp2][j-k-tmp2] == 2 and pos2:
#                             tmp2 += 1
#                         else:
#                             break
#                 else:
#                     pos2 = []
#                     tmp2 = 1
#                 if k == (num-1) and tmp1 != 1 and mp[i+num][j-num] == 1:
#                     pos1.append([i+num,j-num])
#                 if k == (num-1) and tmp2 != 1 and mp[i+num][j-num] == 2:
#                     pos2.append([i+num,j-num])
#                 if len(pos1) >= num:
#                     while num+count1+count2<5:
#                         if i+num+count1<15 and j-num-count1>=0:
#                             if mp[i+num+count1][j-num-count1] != 2:
#                                 count1 += 1
#                             else:
#                                 if i-count2-1>=0 and j+count2+1<15:
#                                     if mp[i-count2-1][j+count2+1] != 2:
#                                         count2 += 1
#                                     else:
#                                         break
#                                 else:
#                                     break
#                         elif i-count2-1>=0 and j+count2+1<15:
#                             if mp[i-count2-1][j+count2+1] != 2:
#                                 count2 += 1
#                             else:
#                                 break
#                         else:
#                             break
#                     if num+count1+count2>=5:    # 有下棋的意义
#                         if tmp1 == 1:
#                             if mp[i+num][j-num] == 0 and mp[i-1][j+1] == 0:
#                                 if i+num+1<15 and j-num-1>=0 and i-2 >=0 and j+2<15:
#                                     if mp[i+num+1][j-num-1] != 2 and mp[i-2][j+2] != 2:
#                                         result_h.append([1, random.choice(([i+num,j-num],[i-1,j+1])),0])
#                                 elif i+num+1<15 and j-num-1>=0:
#                                     if mp[i+num+1][j-num-1] != 2:
#                                         result_h.append([1,[i+num,j-num],0])
#                                 elif i-2 >=0 and j+2<15:
#                                     if mp[i-2][j+2] != 2:
#                                         result_h.append([1,[i-1,j+1],0])
#                             elif mp[i+num][j-num] == 0:
#                                 result_h.append([1,[i+num,j-num],1])
#                             elif mp[i-1][j+1] == 0:
#                                 result_h.append([1,[i-1,j+1],1])
#                         else:
#                             if mp[i+num+1][j-num-1] == 0 and mp[i-1][j+1] == 0:
#                                 result_h.append([1,[i+num-tmp1+1,j-num+tmp1-1],0])
#                             else:
#                                 result_h.append([1,[i+num-tmp1+1,j-num+tmp1-1],1])
#                     pos1 = []
#                     count1 = 0
#                     count2 = 0
#                 if len(pos2) >= num:
#                     while num+count1+count2<5:
#                         if i+num+count1<15 and j-num-count1>=0:
#                             if mp[i+num+count1][j-num-count1] != 1:
#                                 count1 += 1
#                             else:
#                                 if i-count2-1>=0 and j+count2+1<15:
#                                     if mp[i-count2-1][j+count2+1] != 1:
#                                         count2 += 1
#                                     else:
#                                         break
#                                 else:
#                                     break
#                         elif i-count2-1>=0 and j+count2+1<15:
#                             if mp[i-count2-1][j+count2+1] != 1:
#                                 count2 += 1
#                             else:
#                                 break
#                         else:
#                             break
#                     if num+count1+count2>=5:    # 有下棋的意义
#                         if tmp2 == 1:
#                             if mp[i+num][j-num] == 0 and mp[i-1][j+1] == 0:
#                                 if i+num+1<15 and j-num-1>=0 and i-2 >=0 and j+2<15:
#                                     if mp[i+num+1][j-num-1] != 1 and mp[i-2][j+2] != 1:
#                                         result_b.append([1, random.choice(([i+num,j-num],[i-1,j+1])),0])
#                                 elif i+num+1<15 and j-num-1>=0:
#                                     if mp[i+num+1][j-num-1] != 1:
#                                         result_b.append([1,[i+num,j-num],0])
#                                 elif i-2 >=0 and j+2<15:
#                                     if mp[i-2][j+2] != 1:
#                                         result_b.append([1,[i-1,j+1],0])
#                             elif mp[i+num][j-num] == 0:
#                                 result_b.append([1,[i+num,j-num],1])
#                             elif mp[i-1][j+1] == 0:
#                                 result_b.append([1,[i-1,j+1],1])
#                         else:
#                             if mp[i+num+1][j-num-1] == 0 and mp[i-1][j+1] == 0:
#                                 result_b.append([1,[i+num-tmp2+1,j-num+tmp2-1],0])
#                             else:
#                                 result_b.append([1,[i+num-tmp2+1,j-num+tmp2-1],1])
#                     pos2 = []
#                     count1 = 0
#                     count2 = 0
#     result_h.sort(key=lambda x:x[2])
#     result_b.sort(key=lambda x:x[2])
#     if result_b == [] and result_h == []:
#         return [0, []]
#     else:
#         if info == "h":
#             if result_h:
#                 result_h.sort(key=lambda x:x[2])
#                 return list(map(lambda x:x[1],result_h))
#             else:
#                 result_b.sort(key=lambda x:x[2])
#                 return list(map(lambda x:x[1],result_b))
#         else:
#             if result_b:
#                 result_b.sort(key=lambda x:x[2])
#                 return list(map(lambda x:x[1],result_b))
#             else:
#                 result_h.sort(key=lambda x:x[2])
#                 return list(map(lambda x:x[1],result_h))
