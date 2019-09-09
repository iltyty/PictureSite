# code to test model inferencing(using pre-trained models) using pytorch.

from tkinter import messagebox
from torchvision import transforms
from torchvision import models
import torch
from PIL import Image
import cv2

# 参数是图片的路径
def classify(image):
    alexnet = models.alexnet(pretrained=True)

    transform = transforms.Compose(
        [  # [1]
            transforms.Resize(256),  # [2]
            transforms.CenterCrop(224),  # [3]
            transforms.ToTensor(),  # [4]
            transforms.Normalize(  # [5]
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]  # [6]  # [7]
            ),
        ]
    )
    # 读取图片
    img = Image.open(image)

    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)

    alexnet.eval()

    with open("./process/classes.txt") as f:
        classes = [line.strip() for line in f.readlines()]

    resnet = models.resnet101(pretrained=True)

    resnet.eval()

    out = resnet(batch_t)

    _, indices = torch.sort(out, descending=True)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    # 以下输出的是图片分类信息
    result_classes = []
    result_percentages = []
    for idx in indices[0][:5]:
        result_classes.append(classes[idx])
        result_percentages.append(percentage[idx].item())
    return {"classes": result_classes, "percentages": result_percentages}
