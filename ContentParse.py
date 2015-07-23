from BrowserShadow import BrowserShadow
from bs4 import BeautifulSoup

def get_articles_list():
    """ got the articles list """
    blog_name = input('Please input the name of the blog:')
    content_list_page_url = 'http://blog.csdn.net/%(blog_name)s/article/list/1'%{'blog_name':blog_name}
    
    # the type of the page_content is string
    brw = BrowserShadow()
    res = brw.open_url(content_list_page_url)
    page_content = res.read()
    page_soup = BeautifulSoup(page_content)
    article_info_list = []
    
    #get pages size
    articles_num = page_soup.select('#papelist > span')
    s_temp = str(articles_num[0])
    total_page_size = int(s_temp[s_temp.find('共')+1 : s_temp.find('页')])

    next_page = 1
    while 1:      
        # got the articles information of the current page      
        one_list = page_soup.find_all('div' , 'list_item article_item')

        for one_info in one_list:
            # got abstract information of the article
            s_temp = one_info.select('.article_title h1 a')
            article_title = s_temp[0].get_text().replace('\r\n','').replace('\n[置顶]','').replace('    ','')
            
            article_href = 'http://blog.csdn.net/' + s_temp[0]['href']
            article_time = one_info.select('.article_manage > .link_postdate')[0].get_text()
                      
            page_info = {'article_title':article_title, 'article_href':article_href, 'article_time':article_time}
            article_info_list.append(page_info)
            
        next_page = next_page + 1
        next_page_url = 'http://blog.csdn.net/%(blog_name)s/article/list/%(page_num)d'%{'blog_name':blog_name,'page_num':next_page}
        
        # obtain the soup of the next page
        if next_page > total_page_size:
            break
        else:
            res = brw.open_url(next_page_url)
            page_content = res.read()
            page_soup = BeautifulSoup(page_content)
            
##    for article in article_info_list:
##        print(article)
    return article_info_list
       
""" end get_articles_list""" 


def get_article_content(article_info_list):
    """ get the content of the articles"""
    for page_info in article_info_list:
        page_url = page_info['article_href']
        brw = BrowserShadow()
        res = brw.open_url(page_url)
        page_content = res.read()
        page_soup = BeautifulSoup(page_content)
        article_content = page_soup.select('#article_content')
        print(article_content)
        break;
    
""" end get_articles_list""" 

article_info_list = get_articles_list()
get_article_content(article_info_list)
