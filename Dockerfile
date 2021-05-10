FROM python:3.7 as builder

MAINTAINER Yannik Behr <y.behr@gns.cri.nz>

COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

# update PATH environment variable just to stop the warnings
ENV PATH=/root/.local/bin:$PATH

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --user numpy 
RUN pip install --user -r requirements.txt

FROM python:3.7-slim

# Setup new user
ARG NB_USER="lhs_user"
ARG NB_UID="1000"
ENV NB_USER=$NB_USER NB_UID=$NB_UID HOME=/home/$NB_USER
ENV PATH="$HOME/.local/bin:${PATH}"
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER 

USER $NB_USER
WORKDIR $HOME

# copy only the dependencies installation from the 1st stage image
COPY --from=builder --chown=$NB_USER:users /root/.local /home/$NB_USER/.local

RUN mkdir -p $HOME/lh_sampling
WORKDIR $HOME/lh_sampling

COPY --chown=$NB_USER:users . .
RUN python setup.py develop --user 

