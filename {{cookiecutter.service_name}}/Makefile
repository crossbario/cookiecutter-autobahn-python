default:
	@echo ""
	@echo "Targets for service '{{ cookiecutter.service_name }}':"
	@echo ""
	@echo "  version          Print Autobahn Python Docker image version ({{ cookiecutter.image }})"
	@echo "  start            Start Autobahn Python Docker image ({{ cookiecutter.image }})"
	@echo ""

build:
	docker build \
		-t "img_{{ cookiecutter.service_name }}:latest" \
		-f Dockerfile .

version: build
	docker run -it --rm \
		{{ cookiecutter.service_name }} \
		python -c "from autobahn import version; print(version)"

start:
	docker run -it --rm \
		--name {{ cookiecutter.service_name }} \
		--user {{ cookiecutter.uid }} \
		"img_{{ cookiecutter.service_name }}:latest"
