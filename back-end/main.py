from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from flask_cors import CORS
import traceback
import uuid
import time
import random

from config import CONFIG
from game import Board
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet
from utils import get_model_path
from auto_deed import get_auto_move

app = Flask(__name__, static_folder='static')
CORS(app, supports_credentials=True)
api = Api(app)

room_dict = {}


def clear_timeout_room():
    now = time.time()
    del_list = []
    for rid, info in room_dict.items():
        has_two_players = bool(info.get("player2"))
        if has_two_players:
            continue
        if now - info.get("create_time", now) > 300:
            del_list.append(rid)
    for rid in del_list:
        del room_dict[rid]

policy = None
mcts_player = None
try:
    policy = PolicyValueNet(
        CONFIG['BOARD_WIDTH'],
        CONFIG['BOARD_HEIGHT'],
        get_model_path(CONFIG['MODEL_NAME'])
    )
    mcts_player = MCTSPlayer(
        policy.policy_value_fn,
        c_puct=CONFIG['C_PUCT'],
        n_playout=CONFIG['N_PLAYOUT']
    )
except Exception as e:
    print('Warning: failed to initialize global PolicyValueNet/MCTSPlayer:', e)
    policy = None
    mcts_player = None

class AiChess(Resource):
    def post(self):
        try:
            data = request.get_json()
            player = int(data['player'])
            states = {int(k): int(v) for k, v in data['states'].items()}
            last_move = int(data.get('last_move', -1))
            width = int(data.get('width', CONFIG['BOARD_WIDTH']))
            height = int(data.get('height', CONFIG['BOARD_HEIGHT']))
            model_name = data.get('model_name')
            if not model_name:
                if width == 15 and height == 15:
                    model_name = '202202281205_15_15_5_1.0_5_400'
                else:
                    model_name = CONFIG.get('MODEL_NAME')

            board = Board(
                width=width,
                height=height,
                n_in_row=CONFIG['N_IN_ROW']
            )
            board.force_to_state(states, 3 - player, last_move)

            policy_tmp = PolicyValueNet(width, height, get_model_path(model_name))
            mcts_tmp = MCTSPlayer(policy_tmp.policy_value_fn,
                                  c_puct=CONFIG['C_PUCT'],
                                  n_playout=CONFIG['N_PLAYOUT'])
            move = mcts_tmp.get_action(board)
            return {"move": int(move)}, 200
        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500

api.add_resource(AiChess, '/aichess')

class CreateRoom(Resource):
    def post(self):
        clear_timeout_room()
        room_id = str(uuid.uuid4())[:6]
        client_id = request.json.get("client_id", "")
        width = int(request.json.get('width', CONFIG['BOARD_WIDTH']))
        height = int(request.json.get('height', CONFIG['BOARD_HEIGHT']))
        board = Board(
            width=width,
            height=height,
            n_in_row=CONFIG['N_IN_ROW']
        )
        board.init_board(start_player=0)
        owner_color = random.choice([1, 2])
        black_player = 1 if owner_color == 1 else 2
        room_dict[room_id] = {
            "player1": client_id,
            "player2": None,
            "player1_color": owner_color,
            "player2_color": 3 - owner_color,
            "board": board,
            "width": width,
            "height": height,
            "current_player": black_player,
            "game_over": False,
            "winner": 0,
            "ended_by_surrender": False,
            "create_time": time.time(),
            "match_ready": False,
            "pending_undo_request": None,
            "can_undo": True,
            "last_move": -1,
            "last_move_player": 0,
            "auto_play": {},
            "auto_play_player": None,
            "auto_play_calculating": False
        }
        return {
            "code": 200,
            "roomId": room_id,
            "msg": "房间创建成功，等待第二名玩家加入"
        }, 200

class JoinRoom(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id", "")
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]
        if room["game_over"]:
            return {"code": 400, "msg": "房间已结束"}, 400
        if room["player2"] is not None:
            return {"code": 400, "msg": "房间已满"}, 400
        if room["player1"] == client_id:
            return {"code": 400, "msg": "不能自己加入自己房间"}, 400
        room["player2"] = client_id
        room["match_ready"] = True
        return {
            "code": 200,
            "msg": "成功加入房间，等待匹配跳转",
            "roomId": room_id
        }, 200

class OnlineMove(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id")
        move = int(data.get("move"))
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]
        if room["game_over"]:
            return {"code": 400, "msg": "对局已结束"}, 400
        if room["pending_undo_request"] is not None:
            return {"code": 400, "msg": "有待处理的悔棋申请，请先处理"}, 400
        current_p = room["current_player"]
        p1 = room["player1"]
        p2 = room["player2"]
        print(f"请求客户端:{client_id}，房主:{p1}，访客:{p2}，本轮玩家编号:{current_p}")
        if current_p == 1 and client_id != p1:
            return {"code": 400, "msg": "还没轮到你落子"}, 400
        if current_p == 2 and client_id != p2:
            return {"code": 400, "msg": "还没轮到你落子"}, 400
        success = room["board"].do_move(move, current_p)
        if not success:
            return {"code": 400, "msg": "落子位置非法"}, 400
        end, winner = room["board"].game_end()
        if end:
            room["game_over"] = True
            room["winner"] = winner
            room["ended_by_surrender"] = False
        else:
            room["current_player"] = 2 if current_p == 1 else 1
        room["pending_undo_request"] = None
        room["last_move"] = room["board"].last_move
        room["last_move_player"] = current_p
        room["can_undo"] = True
        states = {}
        board = room["board"]
        for idx, val in board.states.items():
            states[idx] = val
        return {
            "code": 200,
            "states": states,
            "currentPlayer": room["current_player"],
            "gameOver": room["game_over"],
            "winner": room["winner"]
        }, 200


class ToggleAutoPlay(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id")
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]
        if client_id not in (room["player1"], room["player2"]):
            return {"code": 400, "msg": "你不在这个房间中"}, 400
        if room["game_over"]:
            return {"code": 200, "msg": "对局已结束"}, 200
        player_num = 1 if client_id == room["player1"] else 2
        room.setdefault("auto_play", {})
        room["auto_play"][client_id] = not room["auto_play"].get(client_id, False)
        room["auto_play_player"] = player_num
        return {"code": 200, "enabled": room["auto_play"].get(client_id, False), "player": player_num}, 200


def calc_ai_point(over_pos, board_size, info_tag):
    n_in_row = CONFIG["N_IN_ROW"]
    for num_threshold in [4, 3, 2, 1]:
        temp_board = Board(width=board_size, height=board_size, n_in_row=n_in_row)
        ret = temp_board.auto_deed(over_pos, num_threshold, info_tag)
        if ret[0] != 0:
            return ret[0]
    return []
        
def find_pos(x, y):
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            L1 = i - 22
            L2 = i + 22
            R1 = j - 22
            R2 = j + 22
            if x >= L1 and x <= L2 and y >= R1 and y <= R2:
                return i, j
    return x, y

class AutoPlayMove(Resource):
    def post(self):
        clear_timeout_room()
        json_data = request.get_json()
        room_id = json_data.get("room_id")
        client_id = json_data.get("client_id")

        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]
        if room["game_over"]:
            return {"code": 400, "msg": "对局已结束"}, 400
        if room["pending_undo_request"] is not None:
            return {"code": 400, "msg": "有待处理的悔棋申请，请先处理"}, 400
        if client_id not in (room["player1"], room["player2"]):
            return {"code": 400, "msg": "你不在当前房间内"}, 400

        if room["auto_play_calculating"]:
            return {"code": 400, "msg": "AI正在思考，请稍后重试"}, 400

        current_player = room["current_player"]
        expected_client = room["player1"] if current_player == 1 else room["player2"]
        if client_id != expected_client:
            return {"code": 400, "msg": "当前不是你的落子回合"}, 400

        player_flag = 1 if client_id == room["player1"] else 2
        room.setdefault("auto_play", {})
        if not room["auto_play"].get(client_id, False):
            return {"code": 400, "msg": "托管功能未开启"}, 400

        width = room.get("width", CONFIG["BOARD_WIDTH"])
        height = room.get("height", CONFIG["BOARD_HEIGHT"])
        board_states = room["board"].states
        target_move = -1

        all_empty_index = [idx for idx in range(width * height) if idx not in board_states]
        if not all_empty_index:
            return {"code": 400, "msg": "棋盘无空位可落子"}, 400

        try:
            room["auto_play_calculating"] = True

            over_pos_list = []
            for idx, color in board_states.items():
                r, c = divmod(idx, width)
                if width == 15 and height == 15 and 0 <= r < 15 and 0 <= c < 15:
                    px = (c - 1) * 44 + 27
                    py = (r - 1) * 44 + 27
                    over_pos_list.append([[px, py], color])
            if not over_pos_list:
                mid_r = height // 2
                mid_c = width // 2
                target_move = mid_r * width + mid_c
                return {"code": 200, "move": target_move}, 200
            if width == 15 and height == 15:
                info_tag = "h" if player_flag == 1 else "b"
                coord_result = calc_ai_point(over_pos_list, width, info_tag)
                print(f"【AI计算】房间:{room_id}，玩家:{client_id}，棋盘尺寸:{width}x{height}，落子点位:{coord_result}")
                if not coord_result:
                    return {"code": 400, "msg": "暂无合适落子点位"}, 400
                best_r, best_c = coord_result
                target_move = best_r * width + best_c
            else:
                # 8x8分支修复
                global policy, mcts_player
                # 校验全局模型是否加载成功
                if mcts_player is None:
                    return {"code": 500, "msg": "AI模型加载失败，无法自动落子"}, 500

                mcts_player_num = player_flag
                last_move = room["board"].last_move

                # 新建独立棋盘，不污染房间原棋盘
                temp_board = Board(width=width, height=height, n_in_row=CONFIG['N_IN_ROW'])
                temp_board.force_to_state(board_states, 3 - mcts_player_num, last_move)

                target_move = mcts_player.get_action(temp_board)
                print(f"【MCTS-AI计算】房间:{room_id}，玩家:{client_id}，棋盘尺寸:{width}x{height}，落子move:{target_move}")
        finally:
            room["auto_play_calculating"] = False
        room["can_undo"] = True
        return {"code": 200, "move": target_move}, 200
    
class SurrenderRoom(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id")
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]
        if room["game_over"]:
            return {"code": 400, "msg": "对局已结束"}, 400
        if client_id not in (room["player1"], room["player2"]):
            return {"code": 400, "msg": "你不在房间内"}, 400
        room["pending_undo_request"] = None
        if client_id == room["player1"]:
            room["game_over"] = True
            room["winner"] = 2
        else:
            room["game_over"] = True
            room["winner"] = 1
        room["ended_by_surrender"] = True
        return {"code": 200, "msg": "你已认输"}, 200

class UndoRequest(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id")

        if not room_id or not client_id:
            return {"code": 400, "msg": "参数不能为空"}, 400
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]

        if not room.get("can_undo", False):
            return {"code": 400, "msg": "刚完成悔棋，需要落子后才能再次申请悔棋"}, 400

        if client_id not in (room["player1"], room["player2"]):
            return {"code": 400, "msg": "你不在这个房间中"}, 400

        if room["game_over"]:
            return {"code": 400, "msg": "对局已结束，无法申请悔棋"}, 400

        if len(room["board"].states) == 0:
            return {"code": 400, "msg": "棋盘暂无棋子，无法悔棋"}, 400

        requester_val = 1 if client_id == room["player1"] else 2
        last_player = room.get("last_move_player", 0)
        if last_player != requester_val:
            return {"code": 400, "msg": "仅上一手落子的玩家可申请悔棋"}, 400

        if room.get("pending_undo_request") is not None:
            return {"code": 400, "msg": "已有待处理的悔棋申请，请等待对方答复"}, 400

        room["pending_undo_request"] = client_id
        return {"code": 200, "msg": "悔棋申请已发送，请等待对方确认"}, 200

class UndoReply(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        room_id = data.get("room_id")
        client_id = data.get("client_id")
        accept = bool(data.get("accept"))

        if not room_id or not client_id:
            return {"code": 400, "msg": "参数不能为空"}, 400
        if room_id not in room_dict:
            return {"code": 400, "msg": "房间不存在"}, 400
        room = room_dict[room_id]

        pending = room.get("pending_undo_request")
        if pending is None:
            return {"code": 400, "msg": "没有待处理的悔棋申请"}, 400
        if client_id == pending:
            return {"code": 400, "msg": "你不能处理自己的悔棋申请"}, 400
        if client_id not in (room["player1"], room["player2"]):
            return {"code": 400, "msg": "你不在这个房间中"}, 400

        requester_client = pending
        requester_val = 1 if requester_client == room["player1"] else 2
        last_player = room.get("last_move_player", 0)
        if last_player != requester_val:
            room["pending_undo_request"] = None
            return {"code": 400, "msg": "非法悔棋，仅上一手落子玩家可申请"}, 400

        room["pending_undo_request"] = None

        if not accept:
            return {"code": 200, "msg": "已拒绝对方悔棋申请"}, 200

        success, player = room["board"].undo_last_move()
        if not success:
            return {"code": 400, "msg": "无可撤销的棋子"}, 400
        if success:
            room["current_player"] = player
            room["game_over"] = False
            room["winner"] = 0
            room["ended_by_surrender"] = False
            room["last_move"] = room["board"].last_move
            room["last_move_player"] = room["board"].last_move_player
            room["can_undo"] = False

        states = {idx: val for idx, val in room["board"].states.items()}
        return {
            "code": 200,
            "msg": "悔棋成功",
            "states": states,
            "currentPlayer": room["current_player"],
            "gameOver": room["game_over"],
            "winner": room["winner"],
            "lastMove": room["board"].last_move
        }, 200


class GetRoomState(Resource):
    def post(self):
        clear_timeout_room()
        data = request.get_json()
        if not data or "room_id" not in data:
            print("【400】请求缺少 room_id 参数")
            return {"code": 400, "msg": "请求缺少room_id参数"}, 400
        room_id = data.get("room_id")
        if room_id not in room_dict:
            print(f"【400】房间不存在/已过期 room_id={room_id}")
            return {"code": 400, "msg": "房间不存在或已超时清理"}, 400
        room = room_dict[room_id]
        board = room["board"]
        width = room.get('width', CONFIG['BOARD_WIDTH'])
        height = room.get('height', CONFIG['BOARD_HEIGHT'])
        full_board = []
        for i in range(height):
            row = []
            for j in range(width):
                idx = i * width + j
                val = board.states.get(idx, 0)
                row.append(val)
            full_board.append(row)
        one_dim_states = {}
        for idx, val in board.states.items():
            one_dim_states[idx] = val
        return {
            "code": 200,
            "fullBoard": full_board,
            "states": one_dim_states,
            "currentPlayer": room["current_player"],
            "gameOver": room["game_over"],
            "winner": room["winner"],
            "player1": room["player1"],
            "player2": room["player2"],
            "player1Color": room["player1_color"],
            "player2Color": room["player2_color"],
            "matchReady": room["match_ready"],
            "undoRequester": room["pending_undo_request"] or "",
            "width": width,
            "height": height,
            "endedBySurrender": room.get('ended_by_surrender', False),
            "lastMove": room["board"].last_move,
            "lastMovePlayer": room.get("last_move_player", 0),
            "autoPlay": room.get("auto_play", {})
        }, 200

api.add_resource(CreateRoom, "/room/create")
api.add_resource(JoinRoom, "/room/join")
api.add_resource(OnlineMove, "/room/move")
api.add_resource(ToggleAutoPlay, "/room/auto-play")
api.add_resource(AutoPlayMove, "/room/auto-play-move")
api.add_resource(SurrenderRoom, "/room/surrender")
api.add_resource(UndoRequest, "/room/undo/request")
api.add_resource(UndoReply, "/room/undo/reply")
api.add_resource(GetRoomState, "/room/state")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)