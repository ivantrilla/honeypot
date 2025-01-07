FROM python:3.12.5
EXPOSE 8000
WORKDIR /app 
COPY . /app 
ENV PYTHONPATH=/app
ENV ENV_DATABASE=temp
ENV ENV_USER=temp
ENV ENV_PASSWORD=temp
ENV ENV_DJANGO_PASSWORD=temp

RUN pip3 install -r requirements.txt --no-cache-dir; yes yes | python3 manage.py collectstatic
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "honeypot.wsgi:application"] 
