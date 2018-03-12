FROM ubuntu
RUN apt-get update
RUN apt-get -y install build-essential unzip wget git python-pip
RUN apt-get -y install software-properties-common
RUN add-apt-repository -uy ppa:team-gcc-arm-embedded/ppa
RUN apt-get -y install gcc-arm-embedded
RUN apt-get -y install gcc-msp430
RUN git clone https://github.com/RIOT-OS/RIOT.git

RUN mkdir /code
COPY . /code/
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
#RUN python manage.py collectstatic --noinput
#CMD ["bash", "docker-entry.sh"]
#INSTALL MIPS GCC
#INSTALL AVR


