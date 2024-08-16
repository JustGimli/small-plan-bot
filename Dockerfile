FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  


RUN pip install --upgrade pip


COPY ./src . 
# COPY .env .
COPY req.txt .
# RUN chmod +x schedule_task.py
RUN pip install -r req.txt


ARG CACHEBUST=1

CMD python main.py