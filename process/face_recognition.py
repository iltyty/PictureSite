# coding=utf-8
# @File  : face_recognition.py
# @Author: 邱圆辉
# @Date  : 2019/9/9
# @Desc  : { face recognition }

from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw
import os
import torch
import time


def init_mtcnn():
    device = torch.device("cpu")

    return MTCNN(keep_all=True, device=device)


def recognize(input_path):
    input_image = Image.open(input_path)
    output_image = input_image.copy()
    mtcnn = init_mtcnn()

    boxes, _ = mtcnn.detect(input_image)
    draw = ImageDraw.Draw(output_image)

    if boxes is not None:
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)

        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        path = "./media/processed_images/" + now + r".jpg"
        path = os.path.abspath(path)
        output_image.save(path)

        path = "\\" + os.path.relpath(path)
        return path.replace("\\", "/")

    else:
        return ""


def main():
    mtcnn = init_mtcnn()

    input_image = Image.open("input.jpg")
    boxes, _ = mtcnn.detect(input_image)
    draw = ImageDraw.Draw(input_image)

    for box in boxes:
        draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)

    input_image.save("output.jpg")


if __name__ == "__main__":
    main()
