import sys
import requests
from bs4 import BeautifulSoup
from itertools import combinations
import heapq

def showoutput(output):
    for i in range(len(output)):
        print("Ticket", i+1, end=": " )
        for j in range(len(output[i])):
                    if j != len(output[i])-1:
                        print(output[i][j],"-", end=" ")
                    else:
                        print(output[i][j])
        
num_input = sys.argv[1:]
num = list()
for i in num_input:
    num.append(int(i))
    
def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        print("Error!")
    else:
        return resp.text
    
url = "https://en.lottolyzer.com/number-frequencies/taiwan/lotto-649"
page = get_web_page(url)

soup = BeautifulSoup(page, 'html.parser')
div = soup.find_all("tr")
div = div[2:]

total_num = 0
frequence_list = list()

for block in div:
    num1 = block.find("td")
    num2 = block.find("td", "freq-p1")
    total_num += (int)(num2.text)
    temp = [num1.text, num2.text]
    frequence_list.append(temp)
    
percentage_list = list()

for i in frequence_list:
    percent = (int)(i[1]) / total_num
    temp = [i[0], round(percent,6)]
    percentage_list.append(temp)

usr_choice = list(combinations(num, 6))
percentage_per_choice = list()
for i in usr_choice:
    score = 1
    for j in i:
        score *= percentage_list[j-1][1]
    percentage_per_choice.append(score)
    
max_num_index_list = map(percentage_per_choice.index, heapq.nlargest(6, percentage_per_choice))
output = list()
for i in max_num_index_list:
    output.append(usr_choice[i])

showoutput(output)


