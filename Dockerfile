FROM python:2.7
ADD ./ /Interview/
WORKDIR /Interview/
RUN pip install -r requirements.txt
CMD python app.py