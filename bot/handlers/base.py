import fnmatch
import importlib
import logging
import os
import re

import settings

_handler_classes = set()
handlers = set()

def init_handlers(client):
  handlers_dir = os.path.dirname(__file__)
  for filename in fnmatch.filter(os.listdir(handlers_dir), '[!_]*.py'):
    module = filename[:-3]
    try:
      importlib.import_module('handlers.%s' % module)
      logging.info('loaded handler module: %s' % module)
    except Exception:
      logging.exception('failed to load handler module: %s' % module)

  handlers.update(cls(settings, client) for cls in _handler_classes)

class HandlerRegistry(type):

  def __init__(cls, name, bases, namespace):
    super(HandlerRegistry, cls).__init__(name, bases, namespace)
    _handler_classes.add(cls)
    _handler_classes.difference_update(bases)

class Handler(object):

  __metaclass__ = HandlerRegistry

  def __init__(self, settings, client):
    self.settings = settings
    self.client = client

  def handle(self, event):
    raise NotImplementedError

class MessageHandler(Handler):

  TRIGGERS = []
  TRIGGER_FLAGS = re.IGNORECASE
  HELP = None

  def __init__(self, *args, **kwargs):
    super(MessageHandler, self).__init__(*args, **kwargs)
    self.TRIGGER_RE = re.compile(
        r'^!(?:%s)(?!\S)' % '|'.join(self.TRIGGERS), flags=self.TRIGGER_FLAGS)

  def handle(self, event):
    if event['type'] == 'message' and 'subtype' not in event:
      text = event['text']
      for trigger in self.TRIGGERS:
        match = self.TRIGGER_RE.search(text)
        if match:
          query = (text[:match.start()] + text[match.end():]).strip()
          return self.handle_message(event, query)

  def handle_message(self, event, query):
    raise NotImplementedError
