# -*- coding: utf-8 -*-
import json
import os
import uipath
from urlparse import parse_qs


def handler(event, context):
    params = parse_qs(event["body"])

    token = params["token"][0]
    if token != os.environ["slack_verification_token"]:
        message = "request token does not match"
        response = {"statusCode": 200, "body": message}
        return response

    process_name = None
    if "text" in params:
        process_name = params["text"][0]

    available_processes = [
        s.strip() for s in os.environ["slack_available_processes"].split(',')
    ]
    if (not process_name or process_name not in available_processes):
        message = "available process name: " + ", ".join(available_processes)
        response = {"statusCode": 200, "body": message}
        return response

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": message}
    return response
