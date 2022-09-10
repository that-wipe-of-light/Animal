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
for file_img in glob.glob(os.path.join(get_train_data(),"traindata/*.jpg")):
    file = file_img.replace(".jpg",".txt")
    img = Image.open(file_img)
    w,h  = img.width,img.height

    infos = []
    with open(file,"r") as f: #遍历图片标签
        for line in f.readlines():
            label,xc,yc,ww,hh = line.split(" ")
            label,xmin,ymin,xmax,ymax = int(label.strip()), \
                                        int((float(xc.strip())-float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) - float(hh.strip()) / 2) * h),\
                                        int((float(xc.strip()) + float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) + float(hh.strip())/2)*h)
            infos.append([label,xmin,ymin,xmax,ymax])
            if ymax - ymin <15:
                continue
            if xmin < 0 or ymin <  0 or xmax >  w or ymax >  h:
                print("xxxxx")
                continue
            target = img.crop([xmin, ymin, xmax, ymax])
            try:
                targetp =os.path.join(get_train_data(),"train_aug")
                if not os.path.exists(targetp):
                    os.mkdir(targetp)
                target.save(os.path.join(targetp, f"{str(k)}_{str(label)}.jpg"))
            except:
                print(file_img)
            k+=1

