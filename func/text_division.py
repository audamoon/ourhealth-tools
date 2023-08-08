import pypandoc
from bs4 import BeautifulSoup
import json
# Convert DOCX to HTML
output = pypandoc.convert_file('test.docx', 'html')

soup = BeautifulSoup(output, 'html.parser')

for tag in soup.find_all(True):
    tag.attrs = {} 


modified_html = str(soup).replace("<li><p>","<li>").replace("</p></li>","</li>").replace("<h1></h1>","")

soup = BeautifulSoup(modified_html, 'html.parser')

all_h1 = soup.find_all('h1')

def get_tags_between_elements(start_element, end_element):
    json_arr = [{"h1":str(start_element).replace("\r\n"," ")}]
    current_element = start_element.find_next_sibling()
    while current_element and current_element != end_element:
        element = str(current_element).replace("\r\n"," ").replace("\n"," ")
        if "title" in str(current_element):
            json_format = {"title":element}
        elif "description" in str(current_element):
            json_format = {"description":element}
        else:
            json_format = {current_element.name:element}
        json_arr.append(json_format)
        current_element = current_element.find_next_sibling()
    return json_arr

def get_last_tags(start_element):
    json_arr = [{"h1":str(start_element).replace("\r\n"," ")}]
    current_element = start_element.find_next_sibling()
    while current_element:
        element = str(current_element).replace("\r\n"," ").replace("\n"," ")
        if "title" in str(current_element):
            json_format = {"title":element}
        elif "description" in str(current_element):
            json_format = {"description":element}
        else:
            json_format = {current_element.name:element}
        json_arr.append(json_format)
        current_element = current_element.find_next_sibling()
    return json_arr

json_arr = []
for i in range (len(all_h1)-1):
    json_arr.append(get_tags_between_elements(all_h1[i], all_h1[i+1]))
json_arr.append(get_last_tags(all_h1[len(all_h1)-1]))    
with open("text_test.json","w",encoding="UTF-8") as f:
        json.dump(json_arr,f,ensure_ascii=False)