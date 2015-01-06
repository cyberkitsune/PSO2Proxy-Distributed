import redis
from ServerCommands import CommandHandlers
import json


def plugin_handler(message):
    print("[PLUGINMSG] Got plugin message on channel %s: %s" % (message['channel'], message['data']))


def servercomm_handler(message):
    msgobj = json.loads(message['data'])
    if 'command' in msgobj and msgobj['command'] in CommandHandlers:
        CommandHandlers[msgobj['command']](msgobj)
    else:
        print("[SERVERCOMM] Got unknown data on channel %s: %s" % (message['channel'], message['data']))


r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub(ignore_subscribe_messages=True)

p.psubscribe(**{"proxy-server-*": servercomm_handler})
p.psubscribe(**{'plugin-message-*': plugin_handler})