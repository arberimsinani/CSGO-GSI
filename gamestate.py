import map
import player
import bomb
import time
import threading
import sys
from pythonosc import udp_client

class GameStateManager:
    def __init__(self):
        self.gamestate = GameState()


class GameState:
    def __init__(self):
        self.left_team = ''
        self.right_team = ''
        self.map = map.Map()
        self.player = player.Player()
        self.bomb = bomb.Bomb()
        self.round_phase = ''
        self.bomb.state = ''
        self.resolume_ip = "192.168.200.241"
        self.resolume_port = 7000
        self.client = udp_client.SimpleUDPClient(self.resolume_ip,self.resolume_port)
        self.last_winner_name = ''
        self.to_reset = True
        self.reset_thread = threading.Thread(target=self.worker)
        self.reset_thread.setDaemon(True)
        self.reset_thread.start()
    
    def reset(self):
        time.sleep(5)
        print('reset done!')
        self.client.send_message('/composition/layers/2/clips/1/video/source/blocktextgenerator/text/params/lines',self.left_team.upper())
        self.client.send_message('/composition/layers/3/clips/1/video/source/blocktextgenerator/text/params/lines',self.right_team.upper())
        self.client.send_message('/composition/layers/2/clips/1/connect',1)
        self.client.send_message('/composition/layers/3/clips/1/connect',1)
        self.to_reset = False
        
    def worker(self):
        while True:
            if self.to_reset:
                self.reset()

    def update_round_phase(self, phase):
        self.round_phase = phase
        print('Round phase: ' + phase)

    def update_round_kills(self, kills):
        if self.player.state.round_kills != kills and kills != 0:
            self.player.state.round_kills = kills
            print(self.player.name + ' got a kill.')

        if kills == 5:
            print(self.player.name + ' got an ace!')

    def update_bomb_state(self, state):
        print('update_bomb_state 1')
        self.bomb.state = state
        if self.bomb.state == 'planted':
            print('update_bomb_state 2')
            print('u montu baboooo!!!')
            self.client.send_message('/composition/layers/2/clips/2/video/source/blocktextgenerator/text/params/lines', 'BOMB')
            self.client.send_message('/composition/layers/3/clips/2/video/source/blocktextgenerator/text/params/lines', 'PLANTED')
            self.client.send_message('/composition/layers/2/clips/2/connect', 1)
            self.client.send_message('/composition/layers/3/clips/2/connect', 1)
            self.to_reset = True

    def update_round_win(self, team_side, team_name):
        if self.bomb.state == 'defused':
            print('update_bomb_state 3')
            self.client.send_message('/composition/layers/2/clips/2/video/source/blocktextgenerator/text/params/lines', 'BOMB')
            self.client.send_message('/composition/layers/3/clips/2/video/source/blocktextgenerator/text/params/lines', 'DEFUSED')
            self.client.send_message('/composition/layers/2/clips/2/connect', 1)
            self.client.send_message('/composition/layers/3/clips/2/connect', 1)
            time.sleep(5)
            
        if self.bomb.state == 'exploded':
            print('update_bomb_state 4')
            self.client.send_message('/composition/layers/4/clips/2/connect',1)
            self.client.send_message('/composition/layers/3/clips/3/connect',1)
            self.client.send_message('/composition/layers/2/clips/3/connect',1)
            time.sleep(1)
        
        if self.map.phase == 'gameover':
            self.client.send_message('/composition/layers/2/clips/2/video/source/blocktextgenerator/text/params/lines','WINNER')
            self.client.send_message('/composition/layers/3/clips/2/video/source/blocktextgenerator/text/params/lines',team_name.upper())
            self.client.send_message('/composition/layers/2/clips/2/connect',1)
            self.client.send_message('/composition/layers/3/clips/2/connect',1)
            time.sleep(20)
            self.client.send_message('/composition/columns/9/connect',1)
            sys.exit("Game over")
        
        self.client.send_message('/composition/layers/2/clips/2/video/source/blocktextgenerator/text/params/lines',team_name.upper())
        self.client.send_message('/composition/layers/3/clips/2/video/source/blocktextgenerator/text/params/lines','round win'.upper())
        self.client.send_message('/composition/layers/2/clips/2/connect',1)
        self.client.send_message('/composition/layers/3/clips/2/connect',1)
        self.to_reset = True
