docker run --name nifi -p 8443:8443 -v /s/repo_volumes/hse/etl/nifi-files:/tmp/nifi-files -d -e SINGLE_USER_CREDENTIALS_USERNAME=admin -e SINGLE_USER_CREDENTIALS_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB apache/nifi:latest


# https://localhost:8443

# pets-data.json