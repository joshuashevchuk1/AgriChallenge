FROM python:3.9-slim

WORKDIR /agri

COPY . .

ENV PYTHONPATH=/agri/src:$PYTHONPATH

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9020

CMD [ "bash", "-c", "bash"]

#CMD ["python", "/agri/src/run.py"]
