# -*- coding: utf-8 -*-
import json


def backlog_handler(event, context):
    import backlog
    response = backlog.handler(event, context)
    return response

def iot_button_handler(event,context):
    import iot_button
    response = iot_button.handler(event, context)
    return response 