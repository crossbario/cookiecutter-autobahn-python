FROM {{ cookiecutter.image }}

RUN mkdir /service
WORKDIR /service

COPY requirements.txt /service
RUN pip install --no-cache -r /service/requirements.txt

{% if cookiecutter.framework == 'twisted' %}
COPY client_tx.py /service/client.py
{% else %}
COPY client_aio.py /service/client.py
{% endif %}

CMD ["python", \
        "-u", \
        "/service/client.py", \
            "--url", "{{ cookiecutter.url }}", \
            "--realm", "{{ cookiecutter.realm }}", \
            "--service_name", "{{ cookiecutter.service_name }}" \
]
