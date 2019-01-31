# -*- coding: utf-8 -*-
import json
import os
import uipath
from jinja2 import Environment, FileSystemLoader
from urlparse import parse_qs


def handler(event, context):
    templates = Environment(
        loader=FileSystemLoader('./templates', encoding='utf8'))

    process_name = None
    if event["body"] is not None:
        params = parse_qs(event["body"])
        if "process_name" in params:
            process_name = params["process_name"][0]

    available_processes = [
        s.strip() for s in os.environ["available_processes"].split(',')
    ]
    if (not process_name or process_name not in available_processes):
        tpl = templates.get_template('request.tpl.html')
        url = "https://" + event["requestContext"]["domainName"] + event[
            "requestContext"]["path"]
        response = {
            "statusCode":
            200,
            "headers": {
                'Content-Type': 'text/html;charset=UTF-8'
            },
            "body":
            tpl.render({
                "available_processes": available_processes,
                "url": url
            })
        }
        return response

    message = uipath.start_jobs(process_name)
    tpl = templates.get_template('response.tpl.html')
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
