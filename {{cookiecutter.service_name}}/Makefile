default:
	@echo ""
	@echo "Targets for service '{{ cookiecutter.service_name }}':"
	@echo ""
	@echo "  version          Print Autobahn Python Docker image version ({{ cookiecutter.image }})"
	@echo "  version_host     Print Autobahn Python on host version"
	@echo "  start            Start Autobahn Python Docker image ({{ cookiecutter.image }})"
	@echo "  start_host       Start Autobahn Python on host"
	@echo ""

version:
	docker run -it --rm \
		{{ cookiecutter.image }} \
		python -c "from autobahn import version; print(version)"

start:
	docker run -it --rm \
		--name {{ cookiecutter.service_name }} \
		--user {{ cookiecutter.uid }} \
		--link {{ cookiecutter.router_service_name }}
		{{ cookiecutter.image }}

version_host:
	python -c "from autobahn import version; print(version)"

start_host:
	crossbar start --personality community --cbdir ./.crossbar/
