# 
FROM python:3.9

# 
WORKDIR /code/bot

# 
RUN mkdir -p /code/scriptJson && chmod -R 777 /code/scriptJson
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code

# 
CMD ["python", "app.py"]