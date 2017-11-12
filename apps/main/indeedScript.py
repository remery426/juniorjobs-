import requests
from bs4 import BeautifulSoup as BS4
from .models import Search
def get_totalPages(str1):
    sub = ""
    num1 = 0
    of_found = False
    for i in range(0,len(str1)):
        if str1[i] == " ":
            if of_found == True:
               break
            else:
                if sub == "of":
                    of_found = True
                sub = ""
        else:
            sub+=str1[i]
    new_sub = ""
    for i in sub:
        if i !=",":
            new_sub+=i
    return int(new_sub)


def parseIndeed(id, currentUser=None):
    if (id[len(id)-9:len(id)-2])== "&start=":
        id = id[:len(id)-9]
    response = {}
    response['error_message'] = None
    if len(id) == 0:
        response['error_message'] = "Invalid URL"
        return response
    if "indeed" not in id:
        response['error_message'] = "URL does not match the specified site"
        return response
    try:
        r = requests.get(id)
    except:
        response['error_message'] = "Invalid URL"
        return response
    if r:
        c = r.content
        soup = BS4(c,"html.parser")
        find_total = soup.find('div',{"id":"searchCount"}).text
        foundText = soup.find('div',{"id":"refineresults"})
        searchtext = (foundText.find('h1').text)
        if(currentUser):
            Search.objects.addSearch(id, searchtext, currentUser)
        iterations = get_totalPages(find_total)
        bad_words = ["mentor", "mentoring", "Mentor","Mentoring","Guiding more junior peers","couch junior","guide junior","help junior", "teach junior", "assist junior"]
        junior_dict ={}
        add_count = 0
        page_var = ""
        count = 0

        while add_count * 15 <= iterations:
            if add_count>0:
                num_holder = 10 * add_count
                page_var = "&start=" + str(num_holder)
            r = requests.get(str(id)+page_var)
            c = r.content

            soup = BS4(c ,"html.parser")
            a_list = []
            b_list = []
            for i, j in zip(soup.find_all("a",{"data-tn-element":"jobTitle"}),soup.find_all("span",{'class':'company'})):
                if i != None and "senior" not in i.text.lower() and "sr." not in i.text.lower() and "lead" not in i.text.lower() and "principal" not in i.text.lower() and "Sr" not in i.text:
                    count+=1
                    a_list.append(i)
                    b_list.append(j.text)
            for x, y, z in zip(soup.find_all("span",{"class":"summary"}),a_list,b_list):
                was_bad = False
                for b in bad_words:
                    if b in x.text:
                        was_bad = True
                if was_bad == False:
                    junior_dict[y.text]= [y["href"], z]

            add_count+=1
            response['results'] = junior_dict
            response['original'] = iterations
            response['newLen'] = len(junior_dict)
        return response
