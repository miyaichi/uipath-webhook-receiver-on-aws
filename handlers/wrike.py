# -*- coding: utf-8 -*-
import json
import os
import uipath

# To enable event, uncomment the dictionary items below
valid_events = {
    "TaskCreated":
    "Fired when a user creates a new task",
    "TaskDeleted":
    "Fired whena task is deleted",
    "TaskTitleChanged":
    "Fired when a task title changes",
    "TaskImportanceChanged":
    "Fired when a task importance changes",
    "TaskStatusChanged":
    "Fired when a task status changes",
    "TaskDatesChanged":
    "Fired when start, finish dates, duration, or the “Work on weekends” flag is changes",
    "TaskParentsAdded":
    "Fired when a task is added to a folder",
    "TaskParentsRemoved":
    "Fired when a task is removed from a folder",
    "TaskResponsiblesAdded":
    "Fired when any new assignee is added to a task, including all Wrike users (and collaborators) and users with pending invitations",
    "TaskResponsiblesRemoved":
    "Fired when someone is unassigned from a task",
    "TaskSharedsAdded":
    "Fired when a task is shared",
    "TaskSharedsRemoved":
    "Fired when a task is unshared",
    "TaskDescriptionChanged":
    "Fired when a task’s description is changed. Note: Notifications related to description field changes are fired with approximately a 5-minute delay.",
    "TaskCustomFieldChanged":
    "Fired when a custom field value on a custom field is changed",
    "AttachmentAdded":
    "Fired when a new attachment is added to a task",
    "AttachmentDeleted":
    "Fired when an attachment was deleted from task or a comment with attachment was deleted",
    "CommentAdded":
    "Fired when a new comment is added. Not fired for comments without text (that is, comments with attachments only).",
    "CommentDeleted":
    "Fired when a comment is deleted",
    "TimelogChanged":
    "Fired when a timelog record is added, updated, or removed",
    "FolderCreated":
    "Fired when a folder or project is created",
    "FolderDeleted":
    "Fired when a folder or project is deleted",
    "FolderTitleChanged":
    "Fired when a user changes the title of a folder or project",
    "FolderParentsAdded":
    "Fired when a folder or project is added to another folder",
    "FolderParentsRemoved":
    "Fired when a folder or project is removed from another folder",
    "FolderSharedsAdded":
    "Fired when a folder or project is shared",
    "FolderSharedsRemoved":
    "Fired when a folder or project is unshared",
    "FolderDescriptionChanged":
    "Fired when a user changes the description of a folder or project",
    "FolderCommentAdded":
    "Fired when a comment is added to a folder or project",
    "FolderCommentDeleted":
    "Fired when a comment is removed from a folder or project",
    "FolderAttachmentAdded":
    "Fired when an attachment is added to a folder or project",
    "FolderAttachmentDeleted":
    "Fired when an attachment is removed from a folder or project",
    "FolderCustomFieldChanged":
    "Fired when a custom field value is changed for folder or project",
    "ProjectDatesChanged":
    "Fired when the start or end dates of a project are changed",
    "ProjectOwnersAdded":
    "Fired when any new owner is assigned to a project, including all Wrike users (and Collaborators) and users with pending invitations",
    "ProjectOwnersRemoved":
    "Fired when an owner is unassigned from a project"
}


def handler(event, context):
    process_name = os.environ["process_name"]
    if (not process_name):
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "process name not found"
            })
        }
        return response

    events = json.loads(event["body"])
    if isinstance(events, dict):
        events = [events]
