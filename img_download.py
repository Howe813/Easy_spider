import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
import time

# 目标网页URL
url = 'https://example.com'  # 替换为你要爬取的实际网页URL

# 设置保存图片的文件夹
root = "images/"
if not os.path.exists(root):
    os.mkdir(root)

# 初始化WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
driver = webdriver.Chrome(options=options)

# 打开网页
driver.get(url)

# 等待页面加载完全
time.sleep(5)  # 等待时间可根据实际情况调整

# 获取网页源代码
html = driver.page_source

# 关闭浏览器
driver.quit()

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html, 'html.parser')

# 查找所有的<img>标签
img_tags = soup.find_all('img')

# 打印调试信息
print(f"找到 {len(img_tags)} 张图片")

# 创建一个集合来存储已下载的图片URL，避免重复
downloaded_urls = set()

# 初始化文件名计数器
image_counter = 1

# 提取所有图片的URL并下载
for img in img_tags:
    # 优先检查 'data-src' 属性，如果没有则使用 'src'
    img_url = img.get('data-src') or img.get('src')
    
    # 如果img_url为空或无效，跳过
    if not img_url:
        print("找到一个无效的img_url，跳过")
        continue
    
    # 如果img_url是相对路径，将其转换为绝对路径
    img_url = urljoin(url, img_url)
    
    # 检查URL是否已经下载过
    if img_url in downloaded_urls:
        print(f"重复的图片URL，跳过: {img_url}")
        continue

    # 添加到已下载的URL集合中
    downloaded_urls.add(img_url)
    
    # 生成顺序文件名
    img_name = f"{image_counter}.jpg"
    
    # 创建完整的文件路径
    img_path = os.path.join(root, img_name)
    
    # 下载图片并保存
    try:
        img_data = requests.get(img_url).content
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
            print(f"图片已保存: {img_path}")
        
        # 增加计数器
        image_counter += 1
        
    except requests.exceptions.RequestException as e:
        print(f"下载图片失败 {img_url}: {e}")

print("所有图片已下载完成")
