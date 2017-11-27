#!/usr/bin/env python
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import time
import logging
import numpy as np
import torchcraft_py.proto as proto
import torchcraft_py.torchcraft as torchcraft
import torchcraft_py.utils as utils

'''
@brief:  base class for torchcraft_py AI bot
@auhtor: cqy
@date:   20171120
'''
class AIBotBase(object):
    def __init__(self, args):
        self.nloop = 0
        self.battles_won = 0
        self.battles_game = 0
        self.BATTLES_NUM = 500
        self.EPISODES_NUM = 50
        self.episodes = 0
        self.args = args
        self.client = None
        self.actions = []

    def _reset(self):
        self.nloop = 0
        self.battles_won = 0
        self.battles_game = 0
        self.actions = []
        logging.info('game start')

        # create a client and connect to the TorchCraft server
        self.client = torchcraft.Client(self.args.ip, self.args.port)
        init_info = self.client.connect()
        logging.debug('received init: %s', init_info)

        # setup the game
        setup_list = [proto.concat_cmd(proto.commands['set_speed'], self.args.speed),
                      proto.concat_cmd(proto.commands['set_gui'], 1),
                      proto.concat_cmd(proto.commands['set_frameskip'], 1),
                      proto.concat_cmd(proto.commands['set_cmd_optim'], 1)]

        logging.debug('setting up the game: %s', ':'.join(setup_list))
        self.client.send(setup_list)
        utils.progress(self.nloop, self.battles_won, self.battles_game, self.episodes)
        self.episodes += 1

        return 0

    # protected, should be overrided by SubClasses
    def _execute_strategy(self):
        return 0

    def run(self):
        while self.episodes < self.EPISODES_NUM:
            if 0 != self._reset():
                logging.error('reset failed!')
                continue
            while True:
                update_info = self.client.receive()
                logging.debug('received state: %s', update_info)
                self.nloop += 1
                self.actions = []
                if bool(self.client.state.d['game_ended']):
                    logging.info('game over')
                    break
                elif self.client.state.d['battle_just_ended']:
                    utils.progress(self.nloop, self.battles_won,
                                   self.battles_game, self.episodes)
                    self.battles_game += 1
                    if bool(self.client.state.d['battle_won']):
                        self.battles_won += 1
                    if self.battles_game >= self.BATTLES_NUM:
                        self.actions = [proto.concat_cmd(proto.commands['restart'])]
                elif self.client.state.d['waiting_for_restart']:
                    logging.info('waiting for restart')
                elif 0 != self._execute_strategy():
                    logging.error('execute strategy failed!')
                logging.debug('sending actions: %s', str(self.actions))
                self.client.send(self.actions)
            self.client.close()
        return 0
