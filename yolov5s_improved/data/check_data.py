import six
from PIL import Image
import numpy as np
from PIL import Image,ImageFont, ImageDraw
import glob
import os
from data_config import get_train_data

classes = ["butterfly","panda","squirrel","tiger","elephant","giraffe"]
all_N_label = {}
k = 0
for file in glob.glob(os.path.join(get_train_data(),"traindata_aug","*.txt")):
    file_img = file.replace(".txt",".jpg")
    img = Image.open(file_img)
    w,h  = img.width,img.height

    infos = []
    with open(file,"r") as f:
        for line in f.readlines():
            label,xc,yc,ww,hh = line.split(" ")
            label,xmin,ymin,xmax,ymax = int(label.strip()), \
                                        int((float(xc.strip())-float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) - float(hh.strip()) / 2) * h),\
                                        int((float(xc.strip()) + float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) + float(hh.strip())/2)*h)
            infos.append([label,xmin,ymin,xmax,ymax])

    font = ImageFont.truetype(font='simhei.ttf', size=np.floor(3e-2 * np.shape(img)[1] + 0.5).astype('int32'))
    draw = ImageDraw.Draw(img)
    for info in infos:
        cls_index,xmin, ymin, xmax, ymax  = info
        int_clas_index = int(cls_index)
        label = classes[int_clas_index]

        label_size = draw.textsize(label, font)
        if int(ymin) - label_size[1] >= 0:
            text_origin = np.array([int(xmin), int(ymin) - label_size[1]])
        else:
            text_origin = np.array([int(xmin), int(ymin) + 1])
        for i in range(1):
            draw.rectangle(
                [int(xmin)+i,int(ymin)+i,int(xmax)-i,int(ymax)-i],
                outline =(0,0,255))
        draw.rectangle(
            [tuple(text_origin), tuple(text_origin + label_size)],
            fill=(255,0,255))
        draw.text(text_origin, str(label), fill=(0, 0, 0), font=font)
    img.show()

