FROM joyzoursky/python-chromedriver

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN pytest weather_app/
RUN pytest functional_tests/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]