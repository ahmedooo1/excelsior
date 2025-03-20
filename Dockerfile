FROM python:3.11
WORKDIR /app
ENV PYTHONPATH="/app:/app/order_service:/app/user_service"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]