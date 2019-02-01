# -*- coding: utf-8 -*-
import gettext
import jinja2
import json
import os
import uipath
from urlparse import parse_qs

def handler(event, context):
    languages = [os.environ["language"]]
    if "Accept-Language" in event["headers"]:
        languages = [
            s.split(";")[0]
            for s in event["headers"]["Accept-Language"].split(',')
        ]
    trans = gettext.translation(
        'messages', localedir='locale', languages=languages, fallback=True)
    trans.install()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('./templates', encoding='utf8'),
        extensions=['jinja2.ext.i18n'])
    env.install_gettext_translations(trans)

    process_name = None
    if event["body"] is not None:
        params = parse_qs(event["body"])
        if "process_name" in params:
            process_name = params["process_name"][0]

    available_processes = [
        s.strip() for s in os.environ["available_processes"].split(',')
    ]
    if (not process_name or process_name not in available_processes):
        tpl = env.get_template('request.tpl.html')
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
    tpl = env.get_template('response.tpl.html')
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
