# uipath-webhook-receiver-on-aws

## Use case

### Ticket Service Integration
ユーザーがチケットサービスで課題を追加・更新した際にWebhookを発生させ、それをトリガーとしてOrchestratorからジョブを起動する。Scheduled Jobで定期的にリクエストをポーリングする方法に比べ、Webhookを活用することで、ユーザーが情報を更新した際に、タイムリーにジョブを起動できる。

起動されたジョブでは、追加・更新されたチケットの内容を取得、処理すべき内容であれば、処理を行いチケットを更新し、チケットの内容に不備があれば差し戻す。

![Use Case #1](https://user-images.githubusercontent.com/129797/51825579-6a43c100-2328-11e9-821f-18784398d09b.png)

### Chat Service Integration
ユーザーがチャットサービスでジョブの起動を依頼し、それをボットで検知してOrchestratorからジョブを起動する。

![Use Case #2](https://user-images.githubusercontent.com/129797/51825724-b858c480-2328-11e9-93bc-bd87aeaad2a9.png)

### IoT Enterprise Button Integration
![Use Case #3](https://user-images.githubusercontent.com/129797/51825742-c1e22c80-2328-11e9-8b3b-4d9a214a0ee9.png)

### HTML Form Integration
![Use Case #4](https://user-images.githubusercontent.com/129797/51825755-cc9cc180-2328-11e9-812f-f4f5df68cd7a.png)



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
