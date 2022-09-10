import os
import sys
import glob
import xml.etree.ElementTree as ET
import numpy as np
from data.data_config import get_train_data
from PIL import  Image
output_folder = "txtlabel"
def get_lbel_path():
    return output_folder
#训练数据集放在traindata 中，之后创建一个空的valdata文件夹与traindata 文件夹同级
origin_img_folder = "traindata"
origin_label_folder = "Annotations"

classes =  ["butterfly","panda","squirrel","tiger","elephant","giraffe"]

all_file = glob.glob(get_train_data() + origin_label_folder +"/*.xml") #F://xxxx/Annotations\xxx.xml

#需要检测的所有类别,需要和xml中的标注名称对应
if not os.path.exists(get_train_data() + output_folder):
    os.mkdir(get_train_data() + output_folder)

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = round(x * dw ,2)
    w = round(w * dw,2)
    y = round(y * dh,2)
    h = round(h * dh,2)
    return (x, y, w, h)

def progress(percent,width=100):
    if percent > 1:
        percent=1
    show_str=('[%%-%ds]' %width) %(int(percent*width)*'#')
    print('\r%s %s%%' %(show_str,int(percent*100)),end='',file=sys.stdout,flush=True)

def convert_annotation(ffile,image_id):
    in_file = open(get_train_data() + origin_label_folder + '/%s.xml' % (image_id),encoding="utf-8")
    out_file = open(get_train_data() + output_folder + '/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    file = ffile.replace(origin_label_folder, origin_img_folder).replace(".xml", ".jpg")
    image = Image.open(file)
    w = image.width
    h = image.height

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:  # 检索xml中的缺陷名称
            print(image_id)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
import shutil
if __name__ == "__main__":
    current = 0
    for file in all_file:
        current +=1
        progress(float(current)/len(all_file))
        image_id = file.split("\\")[-1].split(".")[0]
        convert_annotation(file,image_id)

    all_file = glob.glob(get_train_data() + output_folder +"/*.txt")
    np.random.shuffle(all_file)
    k = 0
    for file in all_file:
        imgfile = file.replace(output_folder, origin_img_folder).replace(".txt", ".jpg")

        if k < len(all_file)*0.2:
            shutil.move(imgfile, imgfile.replace("traindata", "valdata"))
            shutil.move(file, file.replace("txtlabel", "valdata"))
        elif len(all_file)*0.2 < k < len(all_file)*0.4:
            shutil.move(imgfile, imgfile.replace("traindata", "testdata"))
            shutil.move(file, file.replace("txtlabel", "testdata"))
        else:
            shutil.move(file, file.replace("txtlabel", "traindata"))
        k += 1