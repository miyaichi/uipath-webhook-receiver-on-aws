# -*- coding: utf-8 -*-
import json
import os
import uipath


def handler(event, context):
    process_name = os.environ["process_name"]
    if "process_name" in event["placementInfo"]["attributes"]:
        process_name = event["placementInfo"]["attributes"]["process_name"]
    
    if (process_name):
        body = {"message": "process_name not found"}
        response = {"statusCode": 200, "body": json.dumps(body)}
        return response
    
    process_name = event["placementInfo"]["attributes"]["process_name"]
    message = uipath.start_jobs(process_name)
    body = {"message": message}
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response
