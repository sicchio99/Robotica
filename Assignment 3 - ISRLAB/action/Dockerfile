FROM python:3.10-slim
LABEL authors="giodegas"

COPY *.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8090
CMD ["python", "action.py"]
