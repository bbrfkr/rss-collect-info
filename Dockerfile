FROM python:3.7-alpine

RUN pip install redis
COPY collect-info.py /
CMD ["python", "/collect-info.py"]
