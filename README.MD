# Codigo para rinha de backend 2024 Q1
## Requisitos
requer:
- python 3.11
- poetry 1.7.x

### build da imagem
docker build -t rinha-backend .

### rodar o container
docker run -p 8080:8080 rinha-backend