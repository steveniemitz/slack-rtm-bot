from handlers.base import MessageHandler

class EchoHandler(MessageHandler):

  TRIGGERS = ['echo']
  HELP = 'echo the given text'

  def handle_message(self, event, query):
    return query
