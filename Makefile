generate-docs:
	pdoc3 --html --force app

test:
	pytest .

fmt:
	black .
	isort -rc .
	autoflake --in-place -r app

