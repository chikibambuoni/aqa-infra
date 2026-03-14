build:
	docker buildx build -t aqa-infra .

rebuild:
	docker buildx build -t aqa-infra . && devpod delete aqa-infra --force && devpod up . --id aqa-infra --ide none

test:
	docker run -v $PWD:/app aqa-infra pytest tests/ -v

ssh:
	devpod ssh aqa-infra

lint:
	docker run -v $PWD:/app aqa-infra ruff check .
