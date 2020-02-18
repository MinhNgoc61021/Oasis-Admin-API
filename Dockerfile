FROM python:3.7.4
WORKDIR ./oasis-admin-api
COPY  requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

