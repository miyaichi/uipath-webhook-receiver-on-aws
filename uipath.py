# -*- coding: utf-8 -*-
import json
import os
import requests


def start_jobs(process_name):
    o = orchestrator()
    if o.account_authenticate() and o.find_release(
            process_name) and o.start_jobs():
        message = process_name + " started. job_id is " + o.job_id
    else:
        message = process_name + " can not started. message: " + o.message
    return message


class orchestrator:
    def __init__(self):
        self.url = os.environ["orchestrator_url"]
        self.tenancy_name = os.environ["orchestrator_tenancy_name"]
        self.username = os.environ["orchestrator_username"]
        self.password = os.environ["orchestrator_password"]
        self.api_key = os.environ["orchestrator_api_key"]
        self.queue_name = os.environ["orchestrator_queue_name"]
        self.token = None
        self.release_key = None
        self.job_id = None
        self.message = None

    def account_authenticate(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        params = {"api_key": self.api_key}
        response = requests.post(
            self.url + "/api/Account/Authenticate",
            json.dumps({
                "tenancyName": self.tenancy_name,
                "usernameOrEmailAddress": self.username,
                "password": self.password,
            }),
            headers=headers,
            params=params)
        if response.status_code == 200:
            self.token = response.json()["result"]
        else:
            self.message = "/api/Account/Authenticate failed"
        return self.token

    def find_release(self, process_name):
        if self.token is None:
            return None

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token
        }
        params = {
            "$filter": "Name eq '" + process_name + "'",
            "api_key": self.api_key
        }
        response = requests.get(
            self.url + "/odata/Releases", headers=headers, params=params)
        if response.status_code == 200:
            if response.json()["@odata.count"] > 0:
                self.release_key = response.json()["value"][0]["Key"]
            else:
                self.message = "relasse not found"
        else:
            self.message = "/odata/Releases failed"
        return self.release_key

    def start_jobs(self):
        if self.token is None or self.release_key is None:
            return None

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token
        }
        params = {"api_key": self.api_key}
        response = requests.post(
            self.url +
            "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",
            json.dumps({
                "startInfo": {
                    "ReleaseKey": self.release_key
                }
            }),
            headers=headers,
            params=params)
        if response.status_code == 200 or response.status_code == 201:
            if "value" in response.json():
                self.job_id = str(response.json()["value"][0]["Id"])
                return self.job_id
        if "message" in response.json():
            self.message = response.json()["message"]
        else:
            self.message = "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs failed"
        return None
