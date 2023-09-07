# aws에서 제공하는 lambda base python image 사용
FROM amazon/aws-lambda-python:3.8

# optional : pip update
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

WORKDIR /app

# install packages
RUN pip install -r lambda-container-example/requirements.txt

# /var/task/ 경로로 실행파일 복사
RUN cp lambda-container-example/lambda_function2.py /var/task/
RUN cp lambda-container-example/ArcFace.py /var/task/

# 실행 시 lambda_function.py의 lambda_handler 함수를 실행시킴을 정의
CMD ["lambda_function2.lambda_handler"]

