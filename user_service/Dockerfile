FROM python:3.11
WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app:/app/application"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]