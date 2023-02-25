FROM python:3.9
RUN pip3 install pip-tools pytest mypy black isort

WORKDIR /workspace
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

RUN echo 'alias lint="black . && mypy . && isort ."' >> ~/.bashrc
ENV PYTHONPATH /workspace