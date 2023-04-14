fmt:
	black .
	isort -rc .
	autoflake --in-place -r api

