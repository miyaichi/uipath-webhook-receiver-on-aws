# uipath-webhook-receiver-on-aws

ユーザーとのインタラクションからUiPathのジョブを起動する仕組みを提供します。

## Use case

### Ticket Service Integration
ユーザーがチケットサービスで課題を追加・更新した際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動します。Scheduled Jobで定期的にリクエストをポーリングする方法に比べ、Webhookを活用することで、ユーザーが情報を更新した際に、タイムリーにジョブを起動できます。

起動されたジョブでは、追加・更新されたチケットの内容を取得し処理すべき内容であれば処理を行った後チケットを更新し、チケットの内容に不備があれば差し戻します。

![Use Case #1](https://user-images.githubusercontent.com/129797/51825579-6a43c100-2328-11e9-821f-18784398d09b.png)

### Chat Service Integration
ユーザーがチャットサービスでジョブの起動を依頼し、それをボットで検知してOrchestratorからジョブを起動します。起動したいプロセスをユーザーが自身で指定することで、タイムリーなサービス提供が可能となります。

![Use Case #2](https://user-images.githubusercontent.com/129797/51886557-a6802b80-23d3-11e9-9e9d-fc89ebc4d6e1.png)

### IoT Enterprise Button Integration
ユーザーに渡したAWS IoT Enterprise Buttonを押すことで、Orchestratorからジョブを起動します。ボタンを押すだけなので、操作が簡単であり、また、物理的なデバイスとジョブの起動権限を紐づけているので、権限管理がやりやすいです。

![Use Case #3](https://user-images.githubusercontent.com/129797/51886565-ab44df80-23d3-11e9-8523-55e7e41ee6b4.png)

### HTML Form Integration
HTMLフォームをGET/POSTすることで、Orchestratorからジョブを起動します。起動できるプロセス、起動する権限をWebページのアクセス権限と連動して管理することができます。

![Use Case #4](https://user-images.githubusercontent.com/129797/51886570-ac760c80-23d3-11e9-9708-c313aaee4c94.png)

## Path to deploy

* install serverless framework
```console
$ npm install -g serverless
```

* cron this repository and install serverless-python-requirements
```console
$ git clone <this repository>
$ cd <this clone directory>
$ npm install --save serverless-python-requirements
```

* modify config.json
```console
$ vim congig.json
```

* deploy it
```console
$ serverless deploy [--stage production]
```

## Configuration

設定はconfig.jsonに記載します。また、AWS Lambdaの環境変数設定で値を変更することができます。IoT Enterprise Buttonは、デバイスのプレイスメントの属性でプロセス名（属性の名前 process_name）を指定します。

```
$ cat config.json
{
    "orchestrator": {
        "url": "",
        "tenancy_name": "",
        "username": "",
        "password": "",
        "api_key": "",
        "queue_name": ""
    },

    "backlog": {
        "process_name": ""
    },

    "hangout": {
        "verification_token": "",
        "available_processes": ""
    },

    "http": {
        "available_processes": ""
    },

    "slack": {
        "verification_token": "",
        "available_processes": ""
    }
}
```

### orchestrator

```
"orchestrator": {
    "url": "",
    "tenancy_name": "",
    "username": "",
    "password": "",
    "api_key": "",
    "queue_name": ""
}
```

| Name         | Description |
| ------------ | ----------- |
| url          | URL         |
| tenancy_name | テナント名  |
| username     | ユーザー名  |
| password     | パスワード  |
| api_key      | API Key     |

### backlog

```
"backlog": {
    "process_name": ""
}
```

| Name         | Description                                |
| ------------ | ------------------------------------------ |
| process_name | BacklogのWebhookを受信後、起動するプロセス |

### Google Hangouts Chat

```
"hangout": {
    "verification_token": "",
    "available_processes": ""
}
```

| Name                | Description                              |
| ------------------- | ---------------------------------------- |
| verification_token  | 確認トークン                             |
| available_processes | 有効なプロセス名リスト（カンマ区切り）   |

### http

```
"http": {
    "available_processes": ""
}
```

| Name                | Description                            |
| ------------------- | -------------------------------------- |
| available_processes | 有効なプロセス名リスト（カンマ区切り） |

### Slack

```
"slack": {
    "verification_token": "",
    "available_processes": ""
}
```

| Name                | Description                            |
| ------------------- | -------------------------------------- |
| verification_token  | slack app の verification token        |
| available_processes | 有効なプロセス名リスト（カンマ区切り） |

## To Do

* Chatwork integration
* ServiceNow integration
* Wrike integration
* Orchestrator Queue integration
