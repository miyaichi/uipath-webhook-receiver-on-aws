# -*- coding: utf-8 -*-
import datetime
import gettext
import json
import os
import requests
from distutils.util import strtobool
from requests_ntlm import HttpNtlmAuth


def start_jobs(process_name):
    o = orchestrator()
    if o.account_authenticate():
        filter = "Name eq '{}'".format(process_name)
        odata = o.get_odata("/odata/Releases", filter)
        if odata:
            release_key = odata["value"][0]["Key"]
            job_id = o.start_jobs(release_key)
            if job_id:
                message = _("{} started. Job ID is {}").format(
                    process_name, o.job_id)
                return message

    message = _("{} can not started. message is {}").format(
        process_name, o.message)
    return message


def alerts(filter):
    o = orchestrator()
    if o.account_authenticate():
        odata = o.get_odata("/odata/Alerts", filter)
        if odata:
            return odata["value"], None
    return None, o.message


def jobs(filter):
    o = orchestrator()
    if o.account_authenticate():
        odata = o.get_odata("/odata/Jobs", filter)
        if odata:
            return odata["value"], None
    return None, o.message


class orchestrator:
    def __init__(self):
        self.url = os.environ["orchestrator_url"]
        self.tenancy_name = os.environ["orchestrator_tenancy_name"]
        self.username = os.environ["orchestrator_username"]
        self.password = os.environ["orchestrator_password"]
        self.api_key = os.environ["orchestrator_api_key"]
        self.ntlm_authentication = strtobool(
            os.environ["orchestrator_ntlm_authentication"])

        self.message = None

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def account_authenticate(self):
        if self.ntlm_authentication:
            self.session.auth = HttpNtlmAuth(self.username, self.password)
            return True

        params = {"api_key": self.api_key}
        response = self.session.post(
            self.url + "/api/Account/Authenticate",
            json.dumps({
                "tenancyName": self.tenancy_name,
                "usernameOrEmailAddress": self.username,
                "password": self.password
            }),
            params=params)
        if response.status_code == 200:
            self.session.headers["Authorization"] = "Bearer {}".format(
                response.json()["result"])
            return True

        self.message = _("{} failed").format("/api/Account/Authenticate")
        return False

    def get_odata(self, path, filter=None):
        params = {}
        if self.api_key:
            params["api_key"] = self.api_key
        if filter:
            params["$filter"] = filter
        response = self.session.get(self.url + path, params=params)
        if response.status_code == 200:
            odata = response.json()
            if len(odata["value"]):
                return odata

            self.message = _("{} not found").format(path)
        else:
            self.message = _("{} failed").format(path)
        return None

    def start_jobs(self, release_key):
        params = {}
        if self.api_key:
            params["api_key"] = self.api_key
        response = self.session.post(
            self.url +
            "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs",
            json.dumps({
                "startInfo": {
                    "ReleaseKey": release_key
                }
            }),
            params=params)
        if response.status_code == 201:
            if "value" in response.json():
                self.job_id = str(response.json()["value"][0]["Id"])
                return True

        if "message" in response.json():
            self.message = response.json()["message"]
        else:
            self.message = _("{} failed").format(
                "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs")
        return False
