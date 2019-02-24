from selenium import webdriver
import json
import string
driver =  webdriver.Chrome("C:\\chromedriver.exe")
articles=[]

def saveLinksToJson():
    year=2010
    root="https://timesofindia.indiatimes.com/archive/year-"
    for i in range(9):
        articlePages = []
        yearPage=root+str(year)
        for month in range(12):
            print("year ",year,"month ",month+1)
            monthPage=yearPage+",month-"+str(month+1)+".cms"
            driver.get(monthPage)
            calender=driver.find_element_by_id("calenderdiv")
            links=calender.find_elements_by_tag_name("td")
            for link in links:
                try:
                    a={}
                    a['link']=link.find_element_by_tag_name("a").get_attribute("href")
                    a['year']=year
                    a['month']=month+1
                    articlePages.append(a)
                except:
                    pass
        print("saving data for year ",year)
        fileName="data_"+str(year)+".json"
        with open(fileName, 'w') as outfile:
            json.dump(articlePages, outfile)
        year = year + 1


def findArticles(tags,url,year,month,csvName):
    print("year ",year,"month ",month)
    driver.get(url)
    links=driver.find_elements_by_tag_name('a')
    for link in links:
        try:
            # print("testing ",link.text)

            title=link.text
            for p in string.punctuation:
                title = title.replace(p, "")
            title=title.split(' ')
            n=len(title)
            for i in range(n):
                title[i]=title[i].lower()
            # print(" title ",title)
            for tag in tags:
                if tag in title:
                    print("tag found ")
                    article = {}
                    article["link"]=link.get_attribute('href')
                    article['title']=link.text
                    article['year']=year
                    article['month']=month
                    with open(csvName,'a') as f:
                        f.write('\n"'+str(link.text).replace('"','')+'","'+str(link.get_attribute('href'))+'",'+str(year)+','+str(month))
                    break
        except:
            pass



def getUrlFromJson(fileName,tags,csvName):
    visitedLink=[]
    with open(fileName,'r') as f:
        array=json.load(f)
    for link in array:
        if link['year']!=2015 or int(link['month'])>9:
            if link['link'] not in visitedLink:
                visitedLink.append(link['link'])
                findArticles(tags,link['link'],link['year'],link['month'],csvName)

#saveLinksToJson()
year=2015
while year<2019:
    getUrlFromJson("data_"+str(year)+".json",["hiv","aids"],"articles_"+str(year)+".csv")
    year=year+1


#findArticles(["hiv","aids"],"https://timesofindia.indiatimes.com/2010/1/11/archivelist/year-2010,month-1,starttime-40189.cms",2018,10)
#
# findArticles(["stop"],"https://timesofindia.indiatimes.com/2019/1/17/archivelist/year-2019,month-1,starttime-43482.cms")
#
#
#
# print(articles)
driver.close()