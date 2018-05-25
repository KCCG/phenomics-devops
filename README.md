```
______________                              _____                  ________            _______
___  __ \__  /__________________________ ______(_)_____________    ___  __ \_______   ___  __ \_______________
__  /_/ /_  __ \  _ \_  __ \  __ \_  __ `__ \_  /_  ___/_  ___/    __  / / /  _ \_ | / /  / / /__  __ \_  ___/
_  ____/_  / / /  __/  / / / /_/ /  / / / / /  / / /__ _(__  )     _  /_/ //  __/_ |/ // /_/ /__  /_/ /(__  )
/_/     /_/ /_/\___//_/ /_/\____//_/ /_/ /_//_/  \___/ /____/      /_____/ \___/_____/ \____/ _  .___//____/
                                                                                              /_/
```

Introduction
============
Phenmomic devops is a collection of scripts to streamline CI-CD processes. There are individual folders covering one core functionality. Most of the stuff is in `python` and `shell` scripts.

Following are key components for this service:

**docker_deploy_script**
* A generic script to deploy docker images from ECR to ECS cluster. This is used by Jenkins server for CD.
* Runtime Pyhton 2.7.10

**fleet-captain**
* A dockerized service which is used for monitoring historical data execution. It performs:
  * Checking the idle service using dynamodb table `worker-config`
  * Kill idle/sluggish `ECS tasks` with provided threshold.
  * Generates report and sends it using `phenomics-notification` service.
  * A worker to call pipeline for historical index building.
* Runtime Pyhton 3.5.1

Setup
=====
1. The best way of dealing with python environment is to use `direnv`.
2. Install `pyenv` for python `2.7.10` and `3.5.1` run times.
3. Update `.envrc` file in each service folder.

Deployment
==========
1. Services/scripts having docker as requirement has Ddocker/Compose configured.
2. DevOps contains script to tag image and publish it to ECR. ( Should be handled by Jenkins)
2. DevOps requires AWS CLI and credentials in environment variables.


