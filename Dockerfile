FROM python:3.8

ENV  PROTOBUF_VERSION=3.19.4

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LANGUAGE=C.UTF-8

ARG uid
ARG username
ARG  useremail

# cd whylogs
# docker build -t whylogs --build-arg uid=$UID --build-arg username="Jane Smith" --build-arg useremail=jsmith@isp.com -f Dockerfile .
# docker run --rm -it -p 8080:8888 -v /working/directory:/workspace whylogs

RUN mkdir /workspace
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install apt-utils -y -q
RUN apt-get update && \
    apt-get install git -y && \
    apt-get install awscli -y && \
    apt-get install sudo -y && \
    adduser --quiet --disabled-password --gecos "" --uid ${uid} --gid ${uid} whyuser && \
    adduser whyuser sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN curl -sLJO https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip && \
    unzip protoc-*-linux-x86_64.zip -d /usr && \
    chmod -R a+rx /usr/bin/ /usr/include/google
RUN apt-get update && \
    apt-get install -y cmake openjdk-17-jre-headless graphviz && \
    pip install --root-user-action ignore --upgrade pip && \
    pip install --root-user-action ignore pytest && \
    pip install --root-user-action ignore pytest-cov && \
    pip install --root-user-action ignore jupyterlab && \
    pip install --root-user-action ignore numpy && \
    pip install --root-user-action ignore pandas && \
    pip install --root-user-action ignore sphinx
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install nodejs npm -y
RUN npm install --global yarn
RUN curl -sLJO "https://gitlab-runner-downloads.s3.amazonaws.com/latest/deb/gitlab-runner_amd64.deb" && \
    dpkg -i gitlab-runner_amd64.deb

RUN apt-get update && apt-get install -y less emacs vim

RUN pip install --root-user-action ignore ruff

USER whyuser

RUN git config --global user.name "${username}" && \
    git config --global user.email ${useremail}

WORKDIR /home/whyuser
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1 && \
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> .bashrc

WORKDIR /workspace
CMD [ "bash" ]
