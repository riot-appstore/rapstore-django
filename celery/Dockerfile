FROM riot/riotbuild

RUN apt-get update
RUN apt-get install -y python3-pip
ENV APP_USER user
ENV APP_ROOT /code

#ENV C_FORCE_ROOT true # intentionally kept it commented

RUN mkdir /home/${APP_USER}
RUN mkdir /raw
RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir /home/${APP_USER} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

RUN chown -R ${APP_USER} /home/${APP_USER}
RUN chown -R ${APP_USER} /raw


COPY requirements.txt /code/
WORKDIR ${APP_ROOT}

RUN pip3 install -r requirements.txt

USER ${APP_USER}
RUN touch /home/${APP_USER}/.gitconfig
RUN git config --global user.name "RIOT"
RUN git config --global user.email "riot@riot-os.org"
