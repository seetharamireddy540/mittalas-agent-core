ARG TARGETARCH=arm64
FROM public.ecr.aws/lambda/python:3.11-${TARGETARCH}

COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

CMD ["app.lambda_handler"]
