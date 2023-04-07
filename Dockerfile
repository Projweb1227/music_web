# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code 
WORKDIR /code

# Install pip requirements
COPY music_web/requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY ./music_web/ /code/

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#todo cahge /app to this
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "music_eng.wsgi"]
# CMD ["python", "music_eng/manage.py", "runserver", "0.0.0.0:8000", "--settings=music_eng.settings.production"]
CMD [ "sh" ,"entrypoint.sh" ]
# CMD ["gunicorn", "--env", "DJANGO_SETTINGS_MODULE=music_eng.settings.production", "--bind", "0.0.0.0:8000", "music_eng.wsgi:application"]
