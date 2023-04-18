FROM python:3.7.12
WORKDIR /app
COPY /utils /app/utils
COPY /images /app/images
COPY CellCountApp.py imageCell.py yolov5s_cells.onnx requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torchvision
RUN pip install tensorflow
RUN apt-get update && apt-get install -y libgl1-mesa-glx
EXPOSE 8000
CMD ["python", "CellCountApp.py"]

