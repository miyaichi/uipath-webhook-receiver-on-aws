# -*- coding: utf-8 -*-
import json
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def logging(func):
    def decorate(*args, **kwds):
        log.debug("Received event {}".format(json.dumps(args[0])))
        response = func(*args, **kwds)
        log.debug("Response {}".format(json.dumps(response)))
        return response

    return decorate


@logging
def backlog_handler(event, context):
    import handlers.backlog
    response = handlers.backlog.handler(event, context)
    return response


@logging
def http_handler(event, context):
    import handlers.http
    response = handlers.http.handler(event, context)
    return response


@logging
def iot_button_handler(event, context):
    import handlers.iot_button
    response = handlers.iot_button.handler(event, context)
    return response


@logging
def slash_command_handler(event, context):
    import handlers.slash_command
    response = handlers.slash_command.handler(event, context)
    return response
