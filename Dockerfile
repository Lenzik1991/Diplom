FROM python:3.10-slim

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY todolist/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


#WORKDIR /opt/todolist
#
#ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
#    PIP_NO_CASH_DIR=off \
#    PYTHON_PATH=/opt/todolist
#
#RUN groupadd --system service && useradd --system -g service api
#
#RUN pip install "poetry==1.2.2"
#
#COPY poetry.lock pyproject.toml ./
#RUN poetry config virtualenvs.create false \
#    && poetry install --no-dev --no-ansi --no-root
#
#COPY src/ ./d
#USER api
#
#ENTRYPOINT ["bash", "entrypoint.sh"]
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#EXPOSE 8000