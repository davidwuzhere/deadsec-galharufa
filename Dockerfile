FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD python manage.py waitdb && python manage.py makemigrations && python3 manage.py migrate && python manage.py makemigrations galharufa && python3 manage.py migrate galharufa && python manage.py runserver 0.0.0.0:8000