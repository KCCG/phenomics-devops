#!/bin/bash +x
echo "Installing"
npm install
echo "Installation Done"

echo 'Building hippo app.'
rm -rf build
REACT_APP_BASE_URL=https://phenomics-dev.kccg.garvan.org.au/search-engine  CI=true npm run build > build.txt 2>&1


echo 'Getting ECR credentials for nginx image'
eval $(aws ecr get-login --no-include-email | sed 's|https://||')
echo 'Received credentials, activated for 12 hours'


echo 'Creating docker file.'
printf "FROM 254144944163.dkr.ecr.ap-southeast-2.amazonaws.com/phenomics-dev:nginx-latest\nADD build /usr/share/nginx/html" > Dockerfile

echo 'Creating docker images.'
docker build --force-rm=true --tag=254144944163.dkr.ecr.ap-southeast-2.amazonaws.com/phenomics-dev:hippo-latest .

echo 'Getting ECR credentials'
eval $(aws ecr get-login --no-include-email | sed 's|https://||')
echo 'Received credentials, activated for 12 hours'

echo 'Uploading hippo image to ecr'
docker push 254144944163.dkr.ecr.ap-southeast-2.amazonaws.com/phenomics-dev:hippo-latest
echo 'Image uploaded'
echo 'Hippo is ready to be deployed'

