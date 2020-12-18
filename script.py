import string
import random
import os.path

def scrape():
    ## function: scrape MP fan website for TV Shows, movies.
    ## returns: list of quotes
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time

    ## making url lists
    urls = ["http://montypython.50webs.com/Holy_Grail_Scripts.htm", "http://montypython.50webs.com/Meaning_of_Life.htm", "http://montypython.50webs.com/Life_of_Brian.htm"]
    urls += ["http://montypython.50webs.com/Monty_Python_Series_" + str(i) + ".htm" for i in range(1,5)]

    ##scrapes text
    text = []
    driver = webdriver.Firefox()
    for link in urls:
        #vists each overview url
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
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

        for s in scenes:
            driver.get(s)
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            pdata = soup.find_all('p')
            for p in pdata:
                if not p.findChildren("i"):
                    text.append(p.getText())

            #removes useless <p/> junk at bottom of page
            text = text[:-4]
            
    driver.quit()
    return text

##removes garbage from scraped text
def cleantext():
    #dirty text in
    text = scrape()

    ##cleans text 
    for x in range(len(text)):
        ##remove ":"
        if ":" in text[x]:
            text[x] = (text[x])[(text[x]).index(":")+2:]
        ##remove "\n"
        text[x] = (text[x].strip()).replace('\n', '')
        ##remove "..."
        text[x] = text[x].replace("...", "")
        ##remove quotations
        text[x] = text[x].replace('"', '')
        text[x] = text[x].replace("-", " ")
        text[x] = text[x].replace(":", "")
    
    return text

#puts counts of words into a matrix
def get_count_matrix(text):

    ##get count of word transitions
    matrix = {}
    for line in text:
        ##reformat line for punctuation then split
        line = line.replace("!", " ! * ").replace("?", " ? * ").replace(".", " . * ")
        words = line.split()
        ##add '', or beginning to word list
        words.insert(0,'*')
        #iterate through words
        for x in range(len(words)-1):
            #if word is actually end of sentence punctuation, skip it
            if words[x] in (string.punctuation).replace("*",""):
                continue
            #if word x is in matrix
            if words[x] in matrix.keys():
                #if transition x -> y is in matrix, increment
                if words[x+1] in matrix[words[x]].keys():
                    matrix[words[x]][words[x+1]] += 1

                #if transition x -> y is not in matrix, make it
                else:
                    matrix[words[x]][words[x+1]] = 1
            else:
                #add x to new nested matrix
                matrix[words[x]] = {}
                matrix[words[x]][words[x+1]] = 1

    return matrix


#reformat matrix to be based on probability, not counts
def prob_format(matrix):

    for k1 in matrix.keys():
        #get sum of row entries
        rowsum = 0
        for k2 in matrix[k1].keys():
            rowsum+= matrix[k1][k2]
        #reformat row entries as probability
        for k2 in matrix[k1].keys():
            matrix[k1][k2] = (matrix[k1][k2]) / rowsum

    return matrix

def builder(matrix, size):

    text = ['']
    ##building loop
    while len(text) <= size or (len(text) >= size and text[-1] not in string.punctuation):
        #if beginning of new sentence, 
        if (text is None) or (str(text[-1]) in (string.punctuation)):
            text.append((random.choices(list(matrix["*"].keys()), weights = [matrix["*"][w] for w in matrix["*"].keys()], k = 1)[0]).capitalize())
        
        #duplicate check
        if len(text) > 1 and text[-1] == text[-2]:
            text.pop(-1)

        #else add to chain
        #if previous word, x transitions to some y
        elif text[-1] in matrix.keys():
                text.append(random.choices(list(matrix[text[-1]].keys()), weights= [matrix[text[-1]][w] for w in matrix[text[-1]]], k = 1)[0])

        #if x does not transition to any y, append random word
        else:
            text.append(random.choice(list(matrix.keys())))
            
    #turn text list into string, fix punctuation spacing
    text = ((' '.join(text)).replace(" !", "!").replace(" ?", "?").replace(" .", ".")).strip()
    return (text)



def main():
    #rescrape/clean text data
    matrix = prob_format(get_count_matrix(cleantext()))

    #user interface loop
    inp = int(input("About how many words would you like? (-1 to quit) :  "))
    while (inp > 0):
        print("----------------------------------- \n")
        print(builder(matrix, inp))
        print("----------------------------------- \n")
        inp = int(input("About how many words would you like? (0 to quit) :  "))
    

if __name__ == "__main__":
    main()
