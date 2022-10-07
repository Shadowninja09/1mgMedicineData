''' This program will help you to get access to the Medicine data uploaded on 1mg. 
In this program i'll show you how to crawl each data links and save all the medicine name and category in csv format. 
You can explore as many as things which required to you. Read Carefully (: Happy Coding '''

import requests
from bs4 import BeautifulSoup
import re
# import urllib3
import pandas as pd


file = open("medicine_list.csv", 'a', encoding='UTF-8')

main_header = {"authority": "www.1mg.com",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
               }

header = {"authority": "www.1mg.com:authority: www.1mg.com",
          "referer": "https://www.1mg.com/drugs-all-medicinesreferer: https://www.1mg.com/drugs-all-medicines",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
          }

sess = requests.session()


def all_links(url):
    res = sess.get(url, headers=main_header)
    soup = BeautifulSoup(res.content, "html.parser")
    links = soup.find(class_='style__inner-container___3BZU9 style__product-grid___3noQW style__padding-top-bottom-12px___1-DPF')
    for link in links:
        link = re.search('(?:href=")(.*)" target', str(link))
        print(link)
        medicine_data(link)


def medicine_data(url):
        try:
            res = sess.get(url, headers=header)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                if "otc" in res.url:
#                   for OTC Category Medicines
                    otc_med_data(soup)
                else:
#                   for NON_OTC Category Medicines
                    non_otc_med_data(soup)
        except requests.exceptions.ConnectionError:
            pass


def non_otc_med_data(soup):
    cols = ['title', 'Category']
    rows = []
    if soup.find(class_='DrugHeader__header-content___f6GbC') is not None:
        title = soup.find(class_='DrugHeader__header-content___f6GbC').text
    else :
      title = 'Not Mention'
        print(title)
        rows.append({
            cols[0]: title,
            cols[1]:'NON OTC'
        })
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    data_save(df)


def otc_med_data(soup):
    cols = ['title', 'Category']
    rows = []
    if soup.find(class_='ProductTitle__product-title___3QMYH') is not None:
        title = soup.find(class_='ProductTitle__product-title___3QMYH').text
    else :
      title = 'Not Mention'
        rows.append({
            cols[0]: title,
            cols[14]:'OTC'
            })
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    data_save(df)


def data_save(df):
    print(df)
    df.to_csv(file, index=False, line_terminator='\n', header=False)

    
def main():
#   Set range as many as links you want to access
  for i in range(0, 100):
    url = "https://www.1mg.com/drugs/" + str(i)
    print(url)
    medicine_data(url)

        
main()
