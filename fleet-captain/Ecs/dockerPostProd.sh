#!/bin/bash

echo 'Tagging docker image'
docker tag fleet-captain_fleet-captain:latest 254144944163.dkr.ecr.ap-southeast-2.amazonaws.com/phenomics-prod:fleet-captain-latest
echo 'Tagging completed for docker image'

echo 'Getting ECR credentials'
eval $(aws ecr get-login --no-include-email | sed 's|https://||')
echo 'Received credentials, activated for 12 hours'

echo 'Uploading pipeline image to ecr'
docker push 254144944163.dkr.ecr.ap-southeast-2.amazonaws.com/phenomics-prod:fleet-captain-latest
echo 'Image uploaded'
echo 'Captain is ready to be deployed'

