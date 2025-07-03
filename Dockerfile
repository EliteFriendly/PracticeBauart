FROM python:3.12
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# RUN pip install -r /app/requirements.txt 
    
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python

COPY . /app/
