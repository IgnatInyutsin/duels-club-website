FROM python:3.6
COPY ./flask/requirements.txt /requirements.txt
WORKDIR /usr/src/app/
EXPOSE 5000
RUN pip install -r /requirements.txt
CMD ["python", "app.py"]