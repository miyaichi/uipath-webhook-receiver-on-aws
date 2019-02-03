# -*- coding: utf-8 -*-
import gettext
import hmac
import json
import os
import uipath
from hashlib import sha256


def verify_signature(secret, msg, signature):
    mac = hmac.new(secret, msg=msg, digestmod=sha256)
    return hmac.compare_digest(str(mac.digest()), str(signature))


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

    if os.environ["secret"] or "X-UIPATH-Signature" in event["headers"]:
        secret = os.environ["secret"]
        signature = event["headers"]["X-UIPATH-Signature"].decode('base64')
        msg = event["body"].encode('utf-8')
        if not verify_signature(secret, msg, signature):
            response = {
                "statusCode": 403,
                "body": json.dumps({
                    "error": _("Secret and Signature mismatch")
                })
            }
            return response

    payload = json.loads(event["body"])
    type = payload["Type"]
    event_id = payload["EventId"]
    timestamp = payload["Timestamp"]

    response = {"statusCode": 200, "body": json.dumps({"message": message})}
    return response
