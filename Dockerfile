FROM python:3.8-buster
COPY . /app
RUN pip install -r /app/requirements.txt
CMD python /app/manage.py migrate && \
    python /app/manage.py collectstatic --noinput && \
    python /app/manage.py runserver 0.0.0.0:8000
