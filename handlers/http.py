# -*- coding: utf-8 -*-
import json
import os
import uipath
from jinja2 import Environment, FileSystemLoader
from urlparse import parse_qs


def handler(event, context):
    params = parse_qs(event["body"])

    process_name = os.environ["process_name"]
    if "process_name" in params:
        process_name = params["process_name"][0]

    env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))
    tpl = env.get_template('response.tpl.html')

    if (not process_name):
        message = "process_name not found"
        response = {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html;charset=UTF-8'
            },
            "body": tpl.render({
                "message": message
            })
        }
        return response

    message = uipath.start_jobs(process_name)
    response = {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'text/html;charset=UTF-8'
        },
        "body": tpl.render({
            "message": message
        })
    }
    return response
