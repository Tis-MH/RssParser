FROM python:3.10

WORKDIR /code

ADD RssParser /code/RssParser
ADD server /code/server
ADD test /code/test
ADD run.py /code/run.py
ADD requirements.txt /code/requirements.txt
ADD config /code/config

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH="/code/"
ENTRYPOINT [ "python3", "run.py" ]

# docker rm test && docker run --name test -v ./sqlite3.sql:/code/sqlite3.sql test:test