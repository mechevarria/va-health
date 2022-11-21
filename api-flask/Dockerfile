FROM python:3.7.13
EXPOSE 5000
WORKDIR /app
COPY ayasdi-sdk-3.0.0.7.tar.gz .
RUN pip install ayasdi-sdk-3.0.0.7.tar.gz python-dotenv Flask Flask-RESTful
COPY *.sh .
# copying Python files last to prevent unnecessary layers in docker
COPY *.py .
CMD ["flask", "run", "--host", "0.0.0.0"]