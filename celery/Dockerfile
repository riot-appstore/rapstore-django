FROM python:latest
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true # intentionally kept it commented

ENV APP_USER user
ENV APP_ROOT /src

RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_ROOT}

RUN mkdir /config
RUN pip install celery

USER ${APP_USER}
ADD . ${APP_ROOT}
