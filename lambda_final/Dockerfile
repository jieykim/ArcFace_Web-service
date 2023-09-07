# aws에서 제공하는 lambda base python image 사용
FROM amazon/aws-lambda-python:3.8

# optional : pip update
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

WORKDIR /app
COPY . .

# install packages
RUN pip install boto3 numpy opencv-python-headless deepface tensorflow mtcnn




# 실행 시 lambda_function.py의 lambda_handler 함수를 실행시킴을 정의
CMD ["python", "app/lambda_function.lambdahandler"]
