FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /apps
COPY . /code/
RUN git clone https://github.com/RIOT-OS/RIOT.git
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD ["bash", "docker-entry.sh"]
