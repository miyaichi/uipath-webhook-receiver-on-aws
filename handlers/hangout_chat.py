# -*- coding: utf-8 -*-
import gettext
import json
import os
import requests
import uipath


def handler(event, context):
    body = json.loads(event["body"])

    token = body["token"]
    if token != os.environ["verification_token"]:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "text": _("Request token does not match")
            })
        }
        return response

    process_name = body["message"]["argumentText"].strip()
    available_processes = [
        s.strip() for s in os.environ["available_processes"].split(',')
    ]
    if (not process_name or process_name not in available_processes):
        response = {
            "statusCode":
            200,
            "body":
            json.dumps({
                "text":
                _("Available process name are {}").format(
                    ", ".join(available_processes))
            })
        }
        return response

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": json.dumps({"text": message})}
    return response
