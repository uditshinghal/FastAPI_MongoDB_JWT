FROM python

WORKDIR /app

COPY requirement.txt requirement.txt

RUN pip install -r requirement.txt

COPY . .

CMD ["python","run.py"]