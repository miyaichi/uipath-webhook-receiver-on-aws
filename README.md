# uipath-webhook-receiver-on-aws

ユーザーとのインタラクションからUiPathのジョブを起動する仕組みを提供します。

## Use case

### Ticket Service Integration
ユーザーがチケットサービスで課題を追加・更新した際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動します。Scheduled Jobで定期的にリクエストをポーリングする方法に比べ、Webhookを活用することで、ユーザーが情報を更新した際に、タイムリーにジョブを起動できます。

起動されたジョブでは、追加・更新されたチケットの内容を取得し処理すべき内容であれば処理を行った後チケットを更新し、チケットの内容に不備があれば差し戻します。

![Use Case #1](https://user-images.githubusercontent.com/129797/51825579-6a43c100-2328-11e9-821f-18784398d09b.png)

### Chat Service Integration
ユーザーがチャットサービスでジョブの起動を依頼し、それをボットで検知してOrchestratorからジョブを起動します。起動したいプロセスをユーザーが自身で指定することで、タイムリーなサービス提供が可能となります。

現在の実装では、指定されたプロセスを実行するだけですが、ユーザーとのインタラクションを取るBotに修正することも可能です。

![Use Case #2](https://user-images.githubusercontent.com/129797/51886557-a6802b80-23d3-11e9-9e9d-fc89ebc4d6e1.png)

### IoT Enterprise Button Integration
ユーザーに渡したAWS IoT Enterprise Buttonを押すことで、Orchestratorからジョブを起動します。ボタンを押すだけなので、操作が簡単であり、また、物理的なデバイスとジョブの起動権限を紐づけているので、権限管理がやりやすいです。

![Use Case #3](https://user-images.githubusercontent.com/129797/51886565-ab44df80-23d3-11e9-8523-55e7e41ee6b4.png)

### HTML Form Integration
HTMLフォームをPOSTすることで、Orchestratorからジョブを起動します。どの起動できるプロセスの管理、起動する権限の管理をWebページのアクセス権限と連動して管理することができます。

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

設定は、config.jsonに記載します。また、AWS Lambdaの環境変数設定で変更することが可能です。

```
$ cat config.json
{
    "orchestrator_url": "orchestrator url",
    "orchestrator_tenancy_name": "orchestrator tenancy name",
    "orchestrator_username": "orchestrator user name",
    "orchestrator_password": "orchestrator password",
    "orchestrator_api_key": "orchestrator api_key",
    "orchestrator_queue_name": "orchestrator queue name",

    "backlog_process_name": "process name for backlog",

    "hangout_webhook_url": "google hangouts chat webhook url",

    "slack_token": "slack token"
}
```

### orchestrator

| Name                      | Description |
| ------------------------- | ----------- |
| orchestrator_url          | URL         |
| orchestrator_tenancy_name | テナント名  |
| orchestrator_username     | ユーザー名  |
| orchestrator_password     | パスワード  |
| orchestrator_api_key      | API Key     |

### backlog

| Name                 | Description                                |
| -------------------- | ------------------------------------------ |
| backlog_process_name | BacklogのWebhookを受信後、起動するプロセス |

### Google Hangouts Chat

| Name                 | Description                                |
| -------------------- | ------------------------------------------ |
| hangout_webhook_url | Google Hangouts Chatに登録したWebhookURL |

### Slack

| Name                      | Description                                |
| ------------------------- | ------------------------------------------ |
| slack_verification_token  | slack app の verification token |
| slack_available_processes | 有効なプロセス名リスト（カンマ区切り） |

## To Do

* ServiceNow integration
* Wrike integration
* Orchestrator Queue integration
