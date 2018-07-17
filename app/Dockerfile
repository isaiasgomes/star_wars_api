FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY star_wars_api.py /app
CMD python star_wars_api.py