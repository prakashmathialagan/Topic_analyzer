
import requests 
from bs4 import BeautifulSoup 
import os, time
import re
import pandas as pd
import click

@click.command()
@click.argument('filename')
def get_data(filename):
    #print(filename)
    #url_lis=pd.read_csv(filename)
    url_lis=pd.read_excel(filename)
    #url_lis=pd.read_excel("urlss.xlsx", sheet_name="Sheet1")
    d_list=[]
    for a in url_lis["URL"][:]:
        time.sleep(5)
        
        d_dict={}
        content=get_frame(a)
        #heads = get_head(a)
        d_dict["URL"]=a.strip()
        d_dict["content"]=content
        #d_dict["head"]=heads
        d_list.append(d_dict)
        print(f"Content Scarpped for {a}")
        time.sleep(2)
    df=pd.DataFrame(d_list)
    df.to_csv("topic_9Jun27.csv", encoding='UTF-8') 
    url_lis.columns 
    title = url_lis['Page Title '].values.tolist()
    file_p = pd.Series(title)

    df_new=pd.concat([df,file_p],axis=1)  
    df_new.to_csv("article_tile_content27.csv",encoding='UTF-8')

def get_links(url):
    '''
    Input: URL for the page
    Function to get article links from the given URL
    Returns: list of links 
    '''
    print("Links Scrapping in progress")
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html.parser') 
    table = soup.findAll('div',attrs={"class":"article-preview__content"})           
    links_a=[] 
    for x in table:
        a_tags =x.findAll('a', href=True)
        for link in a_tags:
            a=link.get('href')
            #print(a)
            links_a.append(a)
    print(f"total links scrapped is {len(links_a)}")
    return links_a
    

def get_content(url, f_path):
    '''
    Input: URL to get the content
    Function to get article content from the given URL
    Returns: create a txt file with content
    '''

    print("Content scrapper in progress")
    fn_name = url.rsplit('/', 2)[-1]
    r = requests.get(url)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify() )
    article_text = ''

    try:
        article = soup.find("div", {"class": "article-content__content"}).findAll('p')
    except Exception as e:
        article = ''
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text=True))
    # write inot a file
    print("Content scrapped-text file creation in progress")
    index_if = [m.start() for m in re.finditer("\[if", article_text)]
    len_index_if = len(index_if)
    for i in range(len_index_if):
        try:
            indexIf = article_text.index("[if")
            print("indexIf", indexIf)
        except:
            indexIf = -1

        try:
            indexIfEnd = article_text.index("{});")
            print("indexIfEnd", indexIfEnd)
        except:
            indexIfEnd = article_text.index("dif]")
            print("indexIfEnd in Exc", indexIfEnd)
        try:
            st = article_text[indexIf:indexIfEnd + 4]
            print("st", st)
        except:
            st = ''
        rep = article_text.replace(st, '')
        article_text = rep


    file_name = f_path + fn_name + '.txt'
    text_file = open(file_name, "w", encoding = "utf-8")
    n = text_file.write(article_text)
    text_file.close()
    print(f"text file :{file_name} created with {n} words")

def get_frame(url):
    '''
    Input: URL to get the content
    Function to get article content from the given URL
    Returns: content
    '''
    
    print("Content scrapper in progress")    
    r = requests.get(url)
    # print(r.content)
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify() )
    article_text = ''

    try:
        article = soup.find("div", {"class": "article-content__content"}).findAll('p')
    except Exception as e:
        print(e)   
        article = ''
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text=True))    
    
    return article_text


    
            
if __name__=='__main__':
    get_data()
    #do pass URL lit
    #to_URL='https://www.thedigitaltransformationpeople.com/channels/'
    url_lis=pd.read_excel(get_data())
    #url_lis=pd.read_excel("urlss.xlsx", sheet_name="Sheet1")   
    #url_lis.columns
    #do get links
    #links=get_links(to_URL)
    #b=[c for c in links if 'https://www.thedigitaltransformationpeople.com/' in c]
    #print(f"Total clenaned URL is {len(b)}")
    #do pass each link to get the content and store in list
    
    #current_path = os.path.dirname(os.path.abspath(__file__))
    #f_path=current_path+"/files/"
#     d_list=[]
#     for a in url_lis["URL"][2:3]:
#         time.sleep(5)
        
#         d_dict={}
#         content=get_frame(a)
#         d_dict["URL"]=a.strip()
#         d_dict["content"]=content
#         d_list.append(d_dict)
#         print(f"Content Scarpped for {a}")
#         time.sleep(2)
#     df=pd.DataFrame(d_list) 

# df.to_csv("topic_9Jun123.csv", encoding='UTF-8') 
# url_lis.columns 
# title = url_lis['Page Title '].values.tolist()
# file_p = pd.Series(title)

# df_new=pd.concat([df,file_p],axis=1)  
# df_new.to_csv("article_tile_content123.csv",encoding='UTF-8')
    