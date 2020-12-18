

def scrape():
    ## function: scrape MP fan website for TV Shows, movies.
    ## returns: list of quotes
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time

    ## making url lists
    urls = ["http://montypython.50webs.com/Holy_Grail_Scripts.htm"]
    # urls = ["http://montypython.50webs.com/Holy_Grail_Scripts.htm", "http://montypython.50webs.com/Meaning_of_Life.htm", "http://montypython.50webs.com/Life_of_Brian.htm"]
    # urls += ["http://montypython.50webs.com/Monty_Python_Series_" + str(i) + ".htm" for i in range(1,5)]

    ##scrapes text
    text = []
    driver = webdriver.Firefox()
    for link in urls:
        #vists each overview url
        driver.get(link)
        soup = BeautifulSoup(driver.page_source)
        pobj = soup.findAll('p')
        urls = []
        for p in pobj:
            if p.find('a'):
                #if single p/a link
                if len(p.findAll('a')) == 1:
                    urls.append(p.find('a')["href"])
                else:
                #if multiple p/a links
                    for a in p.findAll('a'):
                        urls.append(a["href"])
        #filter useless urls
        scenes = []
        for u in urls:
            if u and "scripts" in u:
                scenes.append("http://montypython.50webs.com/" + u)
        print(scenes)
        for s in scenes:
            driver.get(s)
            soup = BeautifulSoup(driver.page_source)
            pdata = soup.find_all('p')
            for p in pdata:
                if not p.findChildren("i"):
                    text.append(p.getText())

            #removes useless <p/> junk at bottom of page
            text = text[:-4]
        print(scenes)
            
    driver.quit()
    return text

##removes garbage from scraped text
def cleantext():
    #dirty text in
    text = scrape()

    ##cleans text 
    for x in range(0,len(text)):
        ##remove ":"
        if ":" in text[x]:
            text[x] = (text[x])[(text[x]).index(":")+2:]
        ##remove "\n"
        text[x] = (text[x].strip()).replace('\n', '')
        ##remove "..."
        text[x] = text[x].replace("...", "")
        text[x] = text[x].split(".")
    
    print(text)


##this should be main method {} lol

cleantext()