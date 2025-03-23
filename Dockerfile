FROM python:3.9 
RUN pip install Flask==2.2.5
RUN pip install mysql-connector-python==8.0.33
RUN pip install boto3==1.33.13
WORKDIR /usr/src/app  
COPY myapp.py .  
CMD [ "python", "./myapp.py" ]
