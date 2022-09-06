FROM python:latest

COPY ./main.py /home/vathooks/

RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore requests

ENTRYPOINT [ "python", "/home/vathooks/main.py" ]
