FROM python:3.9-slim
RUN apt update -yq
RUN pip install --upgrade pip
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install uvicorn
ENV TZ="Asia/Kolkata"
COPY ./src/ /home/app/
WORKDIR /home/app/
CMD ["uvicorn", "skin_disease_pred_api.main:app", "--host", "0.0.0.0", "--port", "8000"]