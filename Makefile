compose:
	docker compose up --build

test:
	python -m pip install -r services/svc-api/requirements.txt && pip install pytest
	pytest -q
