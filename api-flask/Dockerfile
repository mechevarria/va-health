FROM python:3.7
EXPOSE 5000
WORKDIR /app
COPY ayasdi-sdk-3.0.0.7.tar.gz .
COPY requirements.txt .
RUN pip install -r /app/requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
