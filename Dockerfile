FROM python:3.11-alpine

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./src /app/src

# 
RUN apk add python3-tkinter
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]