FROM public.ecr.aws/lambda/python:3.9

RUN pip install Pillow

COPY image_processor.py ${LAMBDA_TASK_ROOT}

CMD ["image_processor.lambda_handler"]

