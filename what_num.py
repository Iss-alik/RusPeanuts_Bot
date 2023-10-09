import datetime
from bs4 import BeautifulSoup
import requests


# file to list
my_file = open("exceptions.txt", "r") 
data = my_file.read() 
hasnt = data.split("\n") 
my_file.close() 

initial_date = datetime.datetime(1950,10,2)
final_exception = datetime.datetime(1951, 12, 30)

def num_of_date(cur_date):
    exception = num_of_exceptions(cur_date)
    num = cur_date - initial_date - exception
    num = str(num).split(' ')
    num = int(num[0])
    return num

def num_of_exceptions(cur_date):
    if(cur_date > final_exception):
        num_of_exceptions = 65
    else:
        x = int(cur_date.strftime('%w'))
        if x != 0:
            delta = datetime.timedelta(days = x)
            cur_date -= delta
            num_of_exceptions = bin_search(find=cur_date.strftime("%Y-%m-%d")) + 1
    
    return datetime.timedelta(days = num_of_exceptions)

def bin_search(list = hasnt, find = 0):
    l = 0
    h = len(list)
    m = (l+h)//2
    while(l<=h and list[m] != find):

        if(list[m] < find):
            l = m+1
            m = (l+h)//2
        else:
            h = m-1
            m = (l+h)//2
    return m

def num_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    issueNumber= soup.find(class_='issueNumber').string
    num = issueNumber.split('/')
    return int(num[0])
