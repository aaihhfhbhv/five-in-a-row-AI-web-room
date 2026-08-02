import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import main
from game import Board


class OnlineRoomLogicTestCase(unittest.TestCase):
    def setUp(self):
        main.room_dict.clear()

    def test_15x15_auto_play_returns_legal_center_move(self):
        room_id = 'room-15'
        board = Board(width=15, height=15, n_in_row=5)
        board.init_board(start_player=0)
        main.room_dict[room_id] = {
            'player1': 'p1',
            'player2': 'p2',
            'board': board,
            'width': 15,
            'height': 15,
            'current_player': 1,
            'game_over': False,
            'pending_undo_request': None,
            'auto_play': {'p1': True},
            'auto_play_calculating': False,
            'can_undo': True,
            'last_move': -1,
            'last_move_player': 0,
        }

        client = main.app.test_client()
        response = client.post('/room/auto-play-move', json={
            'room_id': room_id,
            'client_id': 'p1'
        })

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn('move', payload)
        move = payload['move']
        self.assertTrue(0 <= move < 15 * 15)

    def test_8x8_auto_play_uses_current_player_for_model_state(self):
        room_id = 'room-8'
        board = Board(width=8, height=8, n_in_row=5)
        board.init_board(start_player=0)
        board.do_move(0, 1)
        main.room_dict[room_id] = {
            'player1': 'p1',
            'player2': 'p2',
            'board': board,
            'width': 8,
            'height': 8,
            'current_player': 2,
            'game_over': False,
            'pending_undo_request': None,
            'auto_play': {'p2': True},
            'auto_play_calculating': False,
            'can_undo': True,
            'last_move': -1,
            'last_move_player': 0,
        }

        class StubMCTSPlayer:
            def __init__(self):
                self.board = None

            def get_action(self, board):
                self.board = board
                return 0

        stub_player = StubMCTSPlayer()
        with patch.object(main, 'mcts_player', stub_player):
            client = main.app.test_client()
            response = client.post('/room/auto-play-move', json={
                'room_id': room_id,
                'client_id': 'p2'
            })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(stub_player.board.current_player, 2)

    def test_undo_accept_resets_state_and_blocks_immediate_replay(self):
        room_id = 'room-undo'
        board = Board(width=8, height=8, n_in_row=5)
        board.init_board(start_player=0)
        board.do_move(0, 1)
        main.room_dict[room_id] = {
            'player1': 'p1',
            'player2': 'p2',
            'board': board,
            'width': 8,
            'height': 8,
            'current_player': 2,
            'game_over': False,
            'pending_undo_request': None,
            'auto_play': {},
            'auto_play_calculating': False,
            'can_undo': True,
            'last_move': 0,
            'last_move_player': 1,
        }

        client = main.app.test_client()
        request_response = client.post('/room/undo/request', json={
            'room_id': room_id,
            'client_id': 'p1'
        })
        self.assertEqual(request_response.status_code, 200)

        reply_response = client.post('/room/undo/reply', json={
            'room_id': room_id,
            'client_id': 'p2',
            'accept': True
        })
        self.assertEqual(reply_response.status_code, 200)

        room = main.room_dict[room_id]
        self.assertFalse(room['can_undo'])
        self.assertEqual(room['last_move_player'], 0)

        repeat_response = client.post('/room/undo/request', json={
            'room_id': room_id,
            'client_id': 'p1'
        })
        self.assertEqual(repeat_response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
