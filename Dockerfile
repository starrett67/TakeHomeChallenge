FROM python:2.7
COPY ./ /Interview/
WORKDIR /Interview/
RUN pip install -r requirements.txt
CMD python app.py