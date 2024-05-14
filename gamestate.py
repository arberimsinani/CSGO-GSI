import map
import player
from pythonosc import udp_client

class GameStateManager:
    def __init__(self):
        self.gamestate = GameState()


class GameState:
    def __init__(self):
        self.map = map.Map()
        self.player = player.Player()
        self.round_phase = ''
        self.bomb_state = ''
        self.resolume_ip = "127.0.0.1"
        self.resolume_port = 7000
        self.client = udp_client.SimpleUDPClient(self.resolume_ip,self.resolume_port)

    def update_round_phase(self, phase):
        self.round_phase = phase
        if self.round_phase == 'over':
            self.bomb_state = ''
        print('Round phase: ' + phase)

    def update_round_kills(self, kills):
        if self.player.state.round_kills != kills and kills != 0:
            self.player.state.round_kills = kills
            print(self.player.name + ' got a kill.')

        if kills == 5:
            print(self.player.name + ' got an ace!')

    def update_bomb_state(self, state):
        self.bomb_state = state
        if self.bomb_state == 'planted':
            self.client.send_message('/composition/layers/1/clips/1/connect',2)
        if self.bomb_state == 'defused':
            self.client.send_message('/composition/layers/1/clips/1/connect',3)
        if self.bomb_state == 'exploded':
            self.client.send_message('/composition/layers/1/clips/1/connect',4)
        print('Bomb state: ' + state)
