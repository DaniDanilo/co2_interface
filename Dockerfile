FROM python:3
ADD requirements.txt /
RUN pip3 install -r requirements.txt --no-cache-dir
ADD main.py /
CMD [ "python", "./main.py" ]