import logging
import time

from slackclient import SlackClient

from plugins.base import init_plugins, plugins
import settings

def get_responses(event):
  for plugin in plugins:
    try:
      yield plugin.handle(event)
    except Exception:
      logging.exception('plugin failed to handle event: %s' % plugin)

def run_bot(client):
  while True:
    logging.debug('rtm_read')
    for event in client.rtm_read():
      if 'ok' in event:
        if event['ok']:
          logging.debug('response confirmation: %s' % event['reply_to'])
        else:
          logging.error('bad response confirmation: %s' % event)
        continue

      logging.info('event: %s' % event['type'])
      response = '\n'.join(filter(None, get_responses(event)))
      if response:
        logging.info('response: %s' % response)
        client.rtm_send_message(event['channel'], response)

    time.sleep(settings.LOOP_INTERVAL)

def main():
  logging.basicConfig(filename=settings.LOGFILE,
                      format=settings.LOGFORMAT,
                      level=settings.LOGLEVEL)

  client = SlackClient(settings.TOKEN)
  logging.info('rtm_connect')
  if not client.rtm_connect():
    logging.critical('failed to connect')
    return

  init_plugins(client)
  run_bot(client)

if __name__ == '__main__':
  main()
