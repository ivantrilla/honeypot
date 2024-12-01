FROM python:3.12.5
EXPOSE 8000
WORKDIR /app 
COPY . /app 
ENV PYTHONPATH=/app
RUN pip3 install -r requirements.txt --no-cache-dir; yes yes | python3 manage.py collectstatic
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "honeypot.wsgi:application"] 
