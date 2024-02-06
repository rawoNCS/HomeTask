FROM python:3.11.7-slim-bullseye

COPY ./app /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
#CMD ["flask", "--app", "app", "run"]


#ADD an_api.py /src

# Expose 5001 as unused ports for testing purposes
#EXPOSE 5000 5001
#CMD ["python", "/src/an_api.py"]


#WORKDIR /hello-devspace

#COPY ./requirements.txt /hello-devspace/requirements.txt

#RUN pip install --no-cache-dir --upgrade -r requirements.txt

#COPY ./app /app

#ENTRYPOINT ["uvicorn", "app.main:app"]
#CMD ["--host", "0.0.0.0", "--port", "80"]