# -*- coding: utf-8 -*-
import gettext
import json
import os
import uipath


def handler(event, context):
    process_name = None
    if "process_name" in event["placementInfo"]["attributes"]:
        process_name = event["placementInfo"]["attributes"]["process_name"]

    if (not process_name):
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": _("process_name not found")
            })
        }
        return response

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": json.dumps({"message": message})}
    return response
