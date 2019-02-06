# -*- coding: utf-8 -*-
import gettext
import json
import os
import requests


def start_jobs(process_name):
    o = orchestrator()
    if o.account_authenticate() and o.find_release_key(
            process_name) and o.start_jobs():
        message = _("{} started. Job ID is {}").format(process_name, o.job_id)
    else:
        message = _("{} can not started. message is {}").format(
            process_name, o.message)
    return message


def find_process_name(release_key):
    o = orchestrator()
    if o.account_authenticate() and o.find_process_name(release_key):
        process_name = o.process_name
    else:
        process_name = None
    return process_name


class orchestrator:
    def __init__(self):
        self.url = os.environ["orchestrator_url"]
        self.tenancy_name = os.environ["orchestrator_tenancy_name"]
        self.username = os.environ["orchestrator_username"]
        self.password = os.environ["orchestrator_password"]
        self.api_key = os.environ["orchestrator_api_key"]
        self.queue_name = os.environ["orchestrator_queue_name"]
        self.token = None
        self.process_name = None
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
            self.message = _("{} failed").format("/api/Account/Authenticate")
        return self.token

    def find_release_key(self, process_name):
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
                self.process_name = process_name
                self.release_key = response.json()["value"][0]["Key"]
            else:
                self.message = _("Relasse not found")
        else:
            self.message = _("{} failed").format("/odata/Releases")
        return self.release_key

    def find_process_name(self, release_key):
        if self.token is None:
            return None

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token
        }
        params = {
            "$filter": "Key eq '" + release_key + "'",
            "api_key": self.api_key
        }
        response = requests.get(
            self.url + "/odata/Releases", headers=headers, params=params)
        if response.status_code == 200:
            if response.json()["@odata.count"] > 0:
                self.process_name = response.json()["value"][0]["Name"]
            else:
                self.message = _("Process not found")
        else:
            self.message = _("{} failed").format("/odata/Releases")
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
            self.message = _("{} failed").format(
                "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs")
        return None
