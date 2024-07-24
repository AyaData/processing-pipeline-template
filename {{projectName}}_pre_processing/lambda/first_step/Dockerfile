FROM amazon/aws-lambda-python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY handler.py .

CMD [ "handler.handler" ]