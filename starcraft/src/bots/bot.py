#!/usr/bin/env python
import time
import logging
import argparse
import torchcraft_py.proto as proto
import torchcraft_py.torchcraft as torchcraft
import torchcraft_py.utils as utils
import ai_bot_base

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s : %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')

'''
@brief:  self-defined AI bot
@auhtor: cqy
@date:   20171120
'''
class MyBot(ai_bot_base.AIBotBase):
    def __init__(self, args):
        super(MyBot, self).__init__(args)

    # override
    def _execute_strategy(self):
        for (uid, ut) in self.client.state.d['units_myself'].iteritems():
            target_uid = utils.get_weakest_uid(self.client.state.d['units_enemy'])
            if -1 == target_uid:
                #logging.warning('can not get the weakest unit!')
                continue
            self.actions.append(
                proto.concat_cmd(
                    proto.commands['command_unit_protected'], uid,
                    proto.unit_command_types['Attack_Unit'], target_uid
                )
            )
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='server ip', default='192.168.11.1')
    parser.add_argument('--port', help='server port', default='11111')
    parser.add_argument('--speed', help='game speed', default=0)
    args = parser.parse_args()

    if 0 != MyBot(args).run():
        logging.error('bot run failed!')
        sys.exit(-1)
    sys.exit(0)
