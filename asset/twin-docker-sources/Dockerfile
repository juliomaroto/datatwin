FROM python:3

WORKDIR /usr/src/twin

RUN git clone https://github.com/juliomaroto/datatwin.git .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./twin.py" ]
