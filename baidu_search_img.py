#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
from skimage import io
import requests
import urllib
from PIL import Image
import numpy as np
import time, os

VISIT_RESULT = 5

# 打开浏览器
driver = webdriver.Chrome()

# 打开百度首页
driver.get('https://www.baidu.com')
 
# 通过class name定位图片搜索按钮
image_search_button = driver.find_element(By.CLASS_NAME, 'soutu-btn')
 
# 点击图片搜索按钮
image_search_button.click()

# 定位到图片上传输入框
input_element = driver.find_element(By.ID, 'soutu-url-kw')
 
# 图片的URL
image_url = 'http://gips1.baidu.com/it/u=3874647369,3220417986&fm=3028&app=3028&f=JPEG&fmt=auto?w=720&h=1280'

#将原图保存备用
urllib.request.urlretrieve(image_url, "./original.jpg")

# 将图片的URL设置到输入框
driver.execute_script("arguments[0].value = arguments[1];", input_element, image_url)
time.sleep(3)
 
# 触发搜索
search_button = driver.find_element(By.CLASS_NAME, 'soutu-url-btn-new')
search_button.click()

# 等待图片加载完成
images = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'general-imgcol-item'))
)

#保存屏幕截图
driver.get_screenshot_as_file('screenshot.png')
print("The screen shot of last visited page is saved!")

#获取所有图片
imgs = driver.find_elements(By.TAG_NAME, 'img')

# 获取VISIT_RESULT指定的图片的src属性
visited_img_src = imgs[VISIT_RESULT].get_attribute('src')

print('--------------visited_img_src------------')
print(visited_img_src)

#保存下载的图片
visited_img = "./img_" + str(VISIT_RESULT) + ".jpg"
urllib.request.urlretrieve(visited_img_src, visited_img)

#定义比较图片的函数
def compare_2_imgs(image1_path, image2_path):
    # 读取图片
    imageA = io.imread(image1_path)
    imageB = io.imread(image2_path)
 
    # 确保图片大小相同
    new_shape = (200, 200)
    
    # 调整图片大小
    resized_image1 = resize(imageA, new_shape, mode='constant', anti_aliasing=True)
    resized_image2 = resize(imageB, new_shape, mode='constant', anti_aliasing=True)

    # 计算两图片的SSIM
    similarity_index = ssim(resized_image1, resized_image2, channel_axis=-1, data_range=255)
    print(f'SSIM: {similarity_index}')
 
    #判断两张图片是否相似
    similarity_threshold = 0.9
    if similarity_index > similarity_threshold:
        print("************Pictures are similar.************")
    else:
        print("************Pictures are not similar.************")
compare_2_imgs('./original.jpg' , visited_img)

# # 等待展示
time.sleep(10)
 
# 关闭浏览器
driver.quit()
