# uipath-webhook-receiver-on-aws

ユーザーとのインタラクションからUiPathのジョブを起動する仕組みを提供します。

## Use case

### Ticket Service Integration
ユーザーがチケットサービスで課題を追加・更新した際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動します。Scheduled Jobで定期的にリクエストをポーリングする方法に比べ、Webhookを活用することで、ユーザーが情報を更新した際に、タイムリーにジョブを起動できます。

起動されたジョブでは、追加・更新されたチケットの内容を取得し処理すべき内容であれば処理を行った後チケットを更新し、チケットの内容に不備があれば差し戻します。

![Use Case #1](https://user-images.githubusercontent.com/129797/52317889-5291ca00-2a05-11e9-8ccf-6e531d37cec9.png)

### Chat Service Integration
ユーザーがチャットサービスでジョブの起動を依頼し、それをボットで検知してOrchestratorからジョブを起動します。起動したいプロセスをユーザーが自身で指定することで、タイムリーなサービス提供が可能となります。

![Use Case #2](https://user-images.githubusercontent.com/129797/52317622-1c077f80-2a04-11e9-980a-55c1410540b7.png)

### IoT Enterprise Button Integration
ユーザーに渡したAWS IoT Enterprise Buttonを押すことで、Orchestratorからジョブを起動します。ボタンを押すだけなので、操作が簡単であり、また、物理的なデバイスとジョブの起動権限を紐づけているので、権限管理がやりやすいです。

![Use Case #3](https://user-images.githubusercontent.com/129797/52317642-2c1f5f00-2a04-11e9-8bc4-2d6a18220126.png)

### HTML Form Integration
HTMLフォームをGET/POSTすることで、Orchestratorからジョブを起動します。起動できるプロセス、起動する権限をWebページのアクセス権限と連動して管理することができます。

![Use Case #4](https://user-images.githubusercontent.com/129797/52317655-3a6d7b00-2a04-11e9-8868-b4708a2942a0.png)

### Version Control System Integration
ユーザーがバージョンコントロールシステムでアクションした際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動します。gitのpull requestを受信してレビュー準備をすることや、pushを受信してリリースの準備をすることができます。

![Use Case #5](https://user-images.githubusercontent.com/129797/52317664-48230080-2a04-11e9-913c-136bbfd0a30f.png)

### Orchestrator
少しわかりにくいですが、OrchestratorのWebhookを受信して、それをトリガーとしてOrchestratorからジョブを起動します。Orchestratorの設定情報やQueue、Jobの状態を受けて処理を行うことができます。

![Use Case #6](https://user-images.githubusercontent.com/129797/52317679-58d37680-2a04-11e9-9a37-eddaa776913c.png)

## Deploy

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

### Backlog

### Github

* Githubで対象とするリポジトリの Setting / Webhooks / Add Webhook を選択します。
* 以下を設定してWebhookを登録します。
    * Payload URL: 作成したGithub用のEndpointを設定します。
    * Secret: Webhookメッセージのダイジェストを作成するためのSecret。config.[stage].jsonにも同じ値を設定します。
    * Which events would you like to trigger this webhook?: Webhookを送信するトリガーを設定します。

参考：[Webhooks](https://developer.github.com/webhooks/)

### Google Hangouts

* Google Cloud ConsoleでHangouts Chat APIを有効にします。
* Hangouts Chat APIの設定で以下を設定します。
    * Bot Name: Orchestrator-Webhook-Receiver
    * Avator URL: https://www.uipath.com/hubfs/Valentin/Brand%20Kit/logos/UiPath-icon.png
    * Description: Run the job with unattended robot
    * Bot URL: 作成したGoogle Hangouts用のEndpointを設定します。
    * Verification Token: Webhookの発信元を確認するためのToken。config.[stage].jsonにも同じ値を設定します。

参考：[Chatbot Concepts](https://developers.google.com/hangouts/chat/concepts/bots)

### HTML Form

* templates/request.tpl.html, templates/response.tpl.htmlを編集します。テンプレートエンジンはjinjaを利用しています。
* LocaleはアクセスしたブラウザのRequest Headerで判断しますので、Localeを追加する場合は、localeフォルダにロケール情報を用意してください。

参考：[jinja](http://jinja.pocoo.org/)

### IoT Buttion

### Orchestrator

* Orchestratorで User / Webhook を選択します。
* 以下を設定してWebhookを登録します。
    * URL: 作成したOrchestrator用のEndpointを設定します。
    * Secret: Webhookメッセージのダイジェストを作成するためのSecret。config.[stage].jsonにも同じ値を設定します。
    * Event Type: Webhookを送信するトリガーを設定します。

参考：[About Webhooks](https://orchestrator.uipath.com/lang-en/docs/about-webhooks)

### Wrike

## Configuration

設定はconfig.[stage].jsonに記載します。また、AWS Lambdaの環境変数設定で値を変更することができます。IoT Enterprise Buttonは、デバイスのプレイスメントの属性でプロセス名（属性の名前 process_name）を指定します。

```
{
    "language": "ja",

    "orchestrator": {
        "url": "",
        "tenancy_name": "",
        "username": "",
        "password": "",
        "api_key": "",
        "ntlm_authentication": "False"
    },

    "handler": {
        "backlog": {
            "process_name": ""
        },
        "github": {
            "secret": "",
            "process_name": ""
        },
        "google_hangouts": {
            "verification_token": "",
            "available_processes": ""
        },
        "html_form": {
            "available_processes": ""
        },
        "orchestrator": {
            "secret": "",
            "process_name": ""
        },
        "slack": {
            "verification_token": "",
            "available_processes": ""
        }
        "wrike": {
            "secret": "",
            "available_processes": ""
        }
    }
}
```

### language

```
"language": "ja"
```

| Name     | Description          |
| -------- | -------------------- |
| language | メッセージの表示言語 |

### orchestrator

```
"orchestrator": {
    "url": "",
    "tenancy_name": "",
    "username": "",
    "password": "",
    "api_key": "",
    "ntlm_authentication": "False"
}
```

| Name                | Description                                     |
| ------------------- | ----------------------------------------------- |
| url                 | URL                                             |
| tenancy_name        | テナント名                                      |
| username            | ユーザー名                                      |
| password            | パスワード                                      |
| api_key             | API Key                                         |
| ntlm_authentication | Windows 認証を有効にしていればTrue (True/False) |

## backlog

```
"handler": {
    "backlog": {
        "process_name": ""
    }
}
```

| Name         | Description                                |
| ------------ | ------------------------------------------ |
| process_name | BacklogのWebhookを受信後、起動するプロセス |

### Github

```
"handler": {
    "github": {
        "secret": "",
        "process_name": ""
    }
}
```

| Name         | Description                               |
| ------------ | ----------------------------------------- |
| secret       | Webhook登録時に設定したsecret             |
| process_name | GithubのWebhookを受信後、起動するプロセス |

### Google Hangouts Chat

```
"handler": {
    "google_hangouts": {
        "verification_token": "",
        "available_processes": ""
    }
}
```

| Name                | Description                              |
| ------------------- | ---------------------------------------- |
| verification_token  | 確認トークン                             |
| available_processes | 有効なプロセス名リスト（カンマ区切り）   |

### HTML form

```
"handler": {
    "html_form": {
        "available_processes": ""
    }
}
```

| Name                | Description                            |
| ------------------- | -------------------------------------- |
| available_processes | 有効なプロセス名リスト（カンマ区切り） |

### Orchestrator

```
"handler": {
    "orchestrator": {
        "secret": "",
        "process_name": ""
    }
}
```

| Name         | Description                                     |
| ------------ | ----------------------------------------------- |
| secret       | Webhook登録時に設定したsecret                   |
| process_name | OrchestratorのWebhookを受信後、起動するプロセス |

### Slack

```
"handler": {
    "slack": {
        "verification_token": "",
        "available_processes": ""
    }
}
```

| Name                | Description                            |
| ------------------- | -------------------------------------- |
| verification_token  | slack app の verification token        |
| available_processes | 有効なプロセス名リスト（カンマ区切り） |

### Wrike

```
"handler": {
    "wrike": {
        "secret": "",
        "process_name": ""
    }
}
```

| Name         | Description                               |
| ------------ | ----------------------------------------- |
| secret       | Webhook登録時に設定したsecret             |
| process_name | WrikeのWebhookを受信後、起動するプロセス |

## To Do

* Wrike integration test
* ServiceNow integration
* Orchestrator Queue integration
