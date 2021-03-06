FROM python:3.7

# RUN pip install fastapi uvicorn

EXPOSE 80

COPY . .
COPY ./requirement.txt /
RUN pip install -r requirement.txt

CMD ["uvicorn", "order:app", "--host", "0.0.0.0", "--port", "8001"]