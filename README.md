# uipath-webhook-receiver-on-aws

ユーザーとのインタラクションからUiPathのジョブを起動する仕組みを提供します。

## Use case

### Ticket Service Integration
ユーザーがチケットサービスで課題を追加・更新した際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動する。Scheduled Jobで定期的にリクエストをポーリングする方法に比べ、Webhookを活用することで、ユーザーが情報を更新した際に、タイムリーにジョブを起動できる。

起動されたジョブでは、追加・更新されたチケットの内容を取得、処理すべき内容であれば、処理を行いチケットを更新し、チケットの内容に不備があれば差し戻す。

![Use Case #1](https://user-images.githubusercontent.com/129797/51825579-6a43c100-2328-11e9-821f-18784398d09b.png)

### Chat Service Integration
ユーザーがチャットサービスでジョブの起動を依頼し、それをボットで検知してOrchestratorからジョブを起動する。起動したいプロセスをユーザーが自身で指定することで、タイムリーなサービス提供が可能となる。

現在の実装は、指定されたプロセスを実行するだけだが、ユーザーとのインタラクションを取るBotに修正することも可能。

![Use Case #2](https://user-images.githubusercontent.com/129797/51886557-a6802b80-23d3-11e9-9e9d-fc89ebc4d6e1.png)

### IoT Enterprise Button Integration
ユーザーに渡したAWS IoT Enterprise Buttonを押すことで、Orchestratorからジョブを起動する。ボタンを押すだけなので、操作が簡単であり、また、物理的なデバイスとジョブの起動権限を紐づけているので、権限管理がやりやすい。

![Use Case #3](https://user-images.githubusercontent.com/129797/51886565-ab44df80-23d3-11e9-8523-55e7e41ee6b4.png)

### HTML Form Integration
HTMLフォームをPOSTすることで、Orchestratorからジョブを起動する。どの起動できるプロセスの管理、起動する権限の管理をWebページのアクセス権限と連動して管理することがかの無。

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

## To Do

* ServiceNow integration
* Wrike integration
* Orchestrator Queue integration
