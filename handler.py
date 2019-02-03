# -*- coding: utf-8 -*-
import gettext
import json
import logging
import os

languages = [os.environ["language"]]
trans = gettext.translation(
    'messages', localedir='locale', languages=languages, fallback=True)
trans.install()

def monitoring(func):
    def decorate(event, context):
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        log.debug("Received event {}".format(json.dumps(event)))
        response = func(event, context)
        log.debug("Response {}".format(json.dumps(response)))
        return response

    return decorate


@monitoring
def backlog_handler(event, context):
    import handlers.backlog
    response = handlers.backlog.handler(event, context)
    return response


@monitoring
def github_handler(event, context):
    import handlers.github
    response = handlers.github.handler(event, context)
    return response


@monitoring
def hagout_chat_handler(event, context):
    import handlers.hangout_chat
    response = handlers.hangout_chat.handler(event, context)
    return response


@monitoring
def http_handler(event, context):
    import handlers.http
    response = handlers.http.handler(event, context)
    return response


@monitoring
def iot_button_handler(event, context):
    import handlers.iot_button
    response = handlers.iot_button.handler(event, context)
    return response


@monitoring
def slash_command_handler(event, context):
    import handlers.slash_command
    response = handlers.slash_command.handler(event, context)
    return response
