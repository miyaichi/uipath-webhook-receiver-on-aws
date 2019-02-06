# -*- coding: utf-8 -*-
import gettext
import json
import os
import uipath


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

    activities = json.loads(event["body"])
    if isinstance(activities, dict):
        activities = [activities]

    issues = []
    for activity in activities:
        issues.append({
            "project_id": activity["project"]["id"],
            "issue_id": activity["id"],
            "type_id": activity["type"]
        })

    if len(issues) == 0:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": _("This webhook was ignored")
            })
        }
        return response

    message = uipath.start_jobs(process_name)
    response = {"statusCode": 200, "body": json.dumps({"message": message})}
    return response
