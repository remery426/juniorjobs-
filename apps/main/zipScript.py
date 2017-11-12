import math
import requests
from bs4 import BeautifulSoup as BS4
from .models import Search

def extract(str1):
    new = ""
    numerical = "1234567890"
    for i in range(0,len(str1)):
        if str1[i] =="+":
          break
        if str1[i] in numerical:
            new+= str1[i]
    return int(new)
def extractText(str1):
    new = ""
    was_plus = False
    for i in range(0,len(str1)):
        if str1[i] == "+":
            was_plus = True
        else:
            if was_plus == True:
                new+= str1[i]
    return new[1:]
def parseZip(id, currentUser=None):
    response = {}

    if (id[len(id)-7:len(id)-1]) == "&page=":
        id = id[:len(id)-7]
        print(id)
    response['error_message'] = None
    if len(id) == 0:
        response['error_message'] = "Invalid URL"
        return response
    if "ziprecruiter" not in id:
        response['error_message'] = "URL does not match the specified site"
        return response
    try:
        r = requests.get(id)
    except:
        response['error_message'] = "Invalid URL"
        return response

    c = r.content
    soup = BS4(c,"html.parser")
    iter1 =soup.find("div", {"id":"job_results_headline"}).text
    searchtext = extractText(iter1)
    if(currentUser):
        Search.objects.addSearch(id, searchtext, currentUser)
    iter1 = extract(iter1)
    iterations = math.floor(iter1/20)+1
    print(iterations)
    junior_dict = {}
    bad_words = ["mentor", "mentoring", "Mentor","Mentoring","Guiding more junior peers","couch junior","guide junior","help junior", "teach junior", "assist junior", "senior", "Senior", "Sr.", "sr.", "SR"]
    bad_title = ["Principal", "principal", "sr", "lead", "Lead", "LEAD", "Head", "head"]
    count = 0
    add_count = 0
    page_var = ""
    count = 0
    while add_count <= iterations:
        print(add_count)
        if add_count>0:
            num_holder = add_count +1
            page_var = "&page=" + str(num_holder)
        print(str(id)+page_var)
        r = requests.get(str(id)+page_var)
        c = r.content
        soup = BS4(c ,"html.parser")
        for x, y, z in zip(soup.find_all("p",{"class":"job_snippet"}),soup.find_all("span",{"class":"just_job_title"}), soup.find_all("p",{"class":"job_org"})):
            found_bad = False
            for i in bad_words:
                if i in x.text or i in y.text:
                    found_bad = True
                    break
            if found_bad == False:
                for i in bad_title:
                    if i in y.text:
                        found_bad =True
                        break
            if found_bad == False:
                junior_dict[y.text] = [x.find("a")['href'], z.text]
        add_count+=1
    response['results'] = junior_dict
    response['original'] = iter1
    response['newLen'] = len(junior_dict)
    return response
