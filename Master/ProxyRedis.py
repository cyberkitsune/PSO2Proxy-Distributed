import redis

def gchat_handler(message):
    pass


def servercomm_handler(message):
    msgobj = json.loads(message['data'])
    if 'command' in msgobj and msgobj['command'] in CommandHandlers:
        CommandHandlers[msgobj['command']](msgobj)
    else:
        print("Got unknown data on channel %s: %s" % (message['channel'], message['data']))


r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub(ignore_subscribe_messages=True)

p.psubscribe("proxy-server-*")
p.subscribe(**{'gchat': gchat_handler})