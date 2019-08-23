import cv2
import os
import datetime
import numpy as np
#裁掉黑边
def change_size(source_path):
    print(os.path.join(source_path,'raw.png'))
    image= cv2.imread(os.path.join(source_path,'raw.png'),1) #读取图片 image_name应该是变量
    mask = cv2.imread(os.path.join(source_path,'instrument_instances.png'))
    #mask = np.zeros_like(image)
    img = cv2.medianBlur(image,5) #中值滤波，去除黑色边际中可能含有的噪声干扰
    b=cv2.threshold(img,15,255,cv2.THRESH_BINARY)          #调整裁剪效果
    binary_image=b[1]               #二值图--具有三通道
    binary_image=cv2.cvtColor(binary_image,cv2.COLOR_BGR2GRAY)
    print(binary_image.shape)       #改为单通道
 
    x=binary_image.shape[0]
    print("高度x=",x)
    y=binary_image.shape[1]
    print("宽度y=",y)
    edges_x=[]
    edges_y=[]
    for i in range(x):
        for j in range(y):
            if binary_image[i][j]==255:
               edges_x.append(i)
               edges_y.append(j)
 
    left=min(edges_x)               #左边界
    right=max(edges_x)              #右边界
    width=right-left                #宽度
    bottom=min(edges_y)             #底部
    top=max(edges_y)                #顶部
    height=top-bottom               #高度
 
    pre1_picture=image[left:left+width,bottom:bottom+height]        #图片截取
    pre1_mask = mask[left:left+width,bottom:bottom+height]  
    return pre1_picture,pre1_mask                                             #返回图片数据
 
source_path='/data/video_img'                                  #图片来源路径
save_path='/data/video_img/additional_generate_no'                               #图片修改后的保存路径
 
if not os.path.exists(save_path):
    os.mkdir(save_path)
 
with open('/data3/Robotic/total.txt','r') as f:
    file_names=f.readlines()
 
starttime=datetime.datetime.now()
for i in range(len(file_names)):
    source_path = file_names[i].strip('\n')
    x,y=change_size(source_path)        #得到文件名
    cv2.imwrite(source_path+'/raw1'+'.png',x)
    cv2.imwrite(source_path+'/anna1'+'.png',y)
    print("裁剪：",file_names[i])
    print("裁剪数量:",i)
print("裁剪完毕")
endtime = datetime.datetime.now()#记录结束时间
endtime = (endtime-starttime).seconds
