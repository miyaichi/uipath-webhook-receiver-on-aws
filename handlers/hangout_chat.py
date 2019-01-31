# -*- coding: utf-8 -*-
import json
import os
import requests
import uipath


def handler(event, context):
    url = os.environ["webhook_url"]

    process_name = event["body"]
    if (not process_name):
        message = "process name not found"
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        response = requests.post(
            url, json.dumps({
                "text": message
            }), headers=headers)
        response = {"statusCode": 200, "body": message}
        return response

    message = uipath.start_jobs(process_name)
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = requests.post(
        url, json.dumps({
            "text": message
        }), headers=headers)
    response = {"statusCode": 200, "body": message}
    return response
