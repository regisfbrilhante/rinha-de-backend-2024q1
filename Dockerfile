FROM python:3.11-alpine

RUN apk add python3-tkinter
# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./src /app/src

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--limit-concurrency", "20000"]