FROM python:3.7

# RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./app /app
COPY ./requirement.txt /
COPY ./login.db /
RUN pip install -r requirement.txt

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8081"]