# uipath-webhook-receiver-on-aws

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

## Use case

* ticket service
* html form
* aws iot button
* slack command

## To Do

* ServiceNow integration
* Wrike integration
* Slack integration