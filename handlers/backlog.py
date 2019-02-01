# -*- coding: utf-8 -*-
import gettext
import json
import os
import uipath

# To enable activities, uncomment the dictionary items below
valid_activities = {
    1: "課題の追加",
    2: "課題の更新",
    3: "課題にコメント",
    #    4: "課題の削除",
    #    5: "Wikiを追加",
    #    6: "Wikiを更新",
    #    7: "Wikiを削除",
    #    8: "共有ファイルを追加",
    #    9: "共有ファイルを更新",
    #    10: "共有ファイルを削除",
    #    11: "Subversionコミット",
    #    12: "GITプッシュ",
    #    13: "GITリポジトリ作成",
    #    14: "課題をまとめて更新",
    #    15: "プロジェクトに参加",
    #    16: "プロジェクトから脱退",
    #    17: "コメントにお知らせを追加",
    #    18: "プルリクエストの追加",
    #    19: "プルリクエストの更新",
    #    20: "プルリクエストにコメント",
    #    21: "プルリクエストの削除",
    #    22: "マイルストーンの追加",
    #    23: "マイルストーンの更新",
    #    24: "マイルストーンの削除",
    #    25: "グループがプロジェクトに参加",
    #    26: "グループがプロジェクトから脱退"
}


def _(message):
    return message


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
        if activity["type"] in valid_activities:
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
