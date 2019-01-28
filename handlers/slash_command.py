# -*- coding: utf-8 -*-
import json
import os
import uipath
from urlparse import parse_qs


def handler(event, context):
    params = parse_qs(event["body"])

    token = params["token"][0]
    if token != os.environ["slack_token"]:
        message = "request token does not match"
        response = {"statusCode": 200, "body": message}
        return response

#   user_name = params["user_name"][0]
#   command = params["command"][0]
#   channel_name = params["channel_name"][0]
#   text = params["text"][0]

    process_name = params["text"][0]

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": message}
    return response
