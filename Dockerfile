FROM python:3.9
WORKDIR /FLASK_REST_API
COPY . .
ENV FLASK_APP=main.py
# UPGRADE pip3
RUN pip3 install --upgrade pip
RUN pip install gunicorn

RUN apt-get update && \
    apt-get install -y gnupg2 curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:15400", "main:app"]
