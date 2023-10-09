from wand.image import Image
from bs4 import BeautifulSoup
import requests


def url_to_square(url):
    src = find_src(url = url)
    src =  requests.get(src, stream= True).raw
    img = Image(file = src)
    if(img.height<500):
        squared = square(image= img)
    else:
         squared = img
    squared.save(filename='request.png')

def square(image):
        w = int(image.width / 2)
        h = image.height

        clone_1 = image.clone()
        clone_2 = image.clone()

        x,y = upper_left(check=image, x= 0, y=30)

        clone_1.crop(x,y, width = w, height = h)

        x = w

        x,y = upper_left(check=image, x= x, y=30)

        clone_2.crop(x,y, width = w, height = h)
        
        w1 = clone_1.width
        w2 = clone_2.width

        w_res = min(w1,w2)
        h_res = clone_1.height + clone_2.height

        cntrl_point = h
        
        res = Image(width=w_res +5, height= h_res, background="white")
        res.composite(image= clone_2, left=5, top= cntrl_point)
        res.composite(image=clone_1, left=5,top=0)

        return res

def upper_left(check, x,y):

    img_inverted = check.clone() #in this section load image and change chanels white and black  
    img_inverted.level(0.6, 0.5, gamma=1)

    while(img_inverted[x,y].string<'srgb(250,250,250)'):
            x+=1
    
    y=0

    return x,y 

def find_src(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    src = soup.find(id='mainImage').get('src')
    src = 'https://acomics.ru' + src
    return src



