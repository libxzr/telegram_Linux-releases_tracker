FROM python:latest
COPY src /src
RUN pip install -r /src/requirements.txt
CMD ["python", "/src/kernel_org.py"]
