import redis
from ServerCommands import CommandHandlers
import json

from Config import YAMLConfig

redis_config = YAMLConfig("redis.cfg.yaml", {'db_host': "localhost", 'db_port': 6379, 'db_id': 0, 'db_pass': ''})

def plugin_handler(message):
    print("[PLUGINMSG] Got plugin message on channel %s: %s" % (message['channel'], message['data']))


def servercomm_handler(message):
    msgobj = json.loads(message['data'])
    if 'command' in msgobj and msgobj['command'] in CommandHandlers:
        CommandHandlers[msgobj['command']](msgobj)
    else:
        print("[SERVERCOMM] Got unknown data on channel %s: %s" % (message['channel'], message['data']))

if redis_config['db_pass'] == '':
    r = redis.StrictRedis(host=redis_config['db_host'], port=redis_config['db_port'], db=redis_config['db_id'])
else:
    r = redis.StrictRedis(host=redis_config['db_host'], port=redis_config['db_port'], db=redis_config['db_id'], password=redis_config['db_pass'])

p = r.pubsub(ignore_subscribe_messages=True)

p.psubscribe(**{"proxy-server-*": servercomm_handler})
p.psubscribe(**{'plugin-message-*': plugin_handler})