#!/bin/bash
docker buildx build -t aqa-infra . && \
devpod delete aqa-infra --force && \
devpod up . --id aqa-infra --ide none
