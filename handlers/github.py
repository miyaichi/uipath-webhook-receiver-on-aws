# -*- coding: utf-8 -*-
import gettext
import hmac
import json
import os
import uipath
from hashlib import sha1, sha256


def verify_signature(secret, msg, signature, digest):
    mac = hmac.new(secret.encode(), msg=msg.encode(), digestmod=eval(digest))
    return hmac.compare_digest(str(mac.hexdigest()), str(signature))


def handler(event, context):
    process_name = os.environ["process_name"]
    if (not process_name):
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": _("process_name not found")
            })
        }
        return response

    if os.environ["secret"] or "X-Hub-Signature" in event["headers"]:
        secret = os.environ["secret"]
        digest, signature = event["headers"]["X-Hub-Signature"].split("=")
        if not verify_signature(secret, str(event["body"]), signature, digest):
            response = {
                "statusCode": 403,
                "body": json.dumps({
                    "error": _("Secret and Signature mismatch")
                })
            }
        return response

    event_type = event['headers']['X-GitHub-Event']
    payload = json.loads(event["body"])

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": json.dumps({"message": message})}
    return response
