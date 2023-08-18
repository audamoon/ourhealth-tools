import pypandoc
from bs4 import BeautifulSoup
import json


class TextParser:
    def __init__(self,docfile_path) -> None:
        self.docfile_path = docfile_path
        self.json_array = {}

    def __convert_to_HTML(self):
        return pypandoc.convert_file(self.docfile_path, 'html')

    def __clear_HTML(self):
        html = self.__convert_to_HTML()
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(True):
            tag.attrs = {}

        self.document_text = str(soup).strip().replace("<li><p>","<li>").replace("</p></li>","</li>").replace("<h1></h1>","").replace("<br/>","")
    
    def get_clear_HTML(self):
        self.__clear_HTML()
        return self.document_text


class Text:
    def __init__(self,text) -> None:
        self.text = "".join(text)

    def garmonia(self):
        json_main = {}
        soup = BeautifulSoup(self.text, "html.parser")
        h1 = str(soup.h1).replace("\r","").replace("\n"," ")
        next_el = soup.h1.find_next_sibling()
        other_tags_str = ""
        while next_el != soup.h2:
            other_tags_str = other_tags_str + (str(next_el))
            next_el = next_el.find_next_sibling()

        json_main["h1_block"] = {h1:other_tags_str.replace("\r","").replace("\n"," ")}

        h2_json = {}
        all_h2 = soup.find_all("h2")
        for j in range(len(all_h2)):
            h2_current = str(all_h2[j]).replace("\r","").replace("\n"," ")
            next_tag = all_h2[j].find_next("h2")
            next_el = all_h2[j].find_next_sibling()
            other_tags_str = ""
            while next_el != next_tag:
                other_tags_str = other_tags_str + (str(next_el))
                next_el = next_el.find_next_sibling()
            h2_json.update({h2_current:other_tags_str.replace("\r","").replace("\n"," ")})
        json_main["h2_blocks"] = h2_json
        return json_main


class TextController:
    def __init__(self,texts) -> None:
        self.texts = texts
    
    def get_right_json(self):
        json_fin = {}
        for i in range(len(self.texts)):
            text_object = Text(self.texts[i][0])
            json_fin[f"text-{i}"] = text_object.garmonia()

        with open("result.json", "w",encoding="UTF-8") as f:
            json.dump(json_fin,f, ensure_ascii=False)


class TextDivider:
    def __init__(self,docfile_path) -> None:
        self.parser = TextParser(docfile_path)

    def __get_h1_before_h2(self,html):
        soup = BeautifulSoup(html, "html.parser")
        h1_str = "".join(str(soup.h1))

        next_el = soup.h1.find_next_sibling()
        while next_el != soup.h2:
            h1_str = h1_str + "".join(str(next_el))
            next_el = next_el.find_next_sibling()
        return [h1_str]

    def __divide_by_tag(self,html,tag_name):
        soup = BeautifulSoup(html, "html.parser")
        all_tags = soup.find_all(tag_name)
        divided_text = []

        for i in range(len(all_tags)):
            current_tag = all_tags[i]
            next_tag = current_tag.find_next(tag_name)
            next_el = current_tag.find_next_sibling()
            separator = ""
            text = separator.join(str(current_tag))
            while next_tag != next_el:
                text = text + separator.join(str(next_el))
                next_el = next_el.find_next_sibling()
            divided_text.append(text)
        return divided_text

    def complete_divide(self):
        h1_divided = self.__divide_by_tag(divider.parser.get_clear_HTML(),"h1")
        texts = []
        text_solid = ""
        html = "".join(text_solid)
        for i in range(len(h1_divided)):
            text_solid = h1_divided[i]
            html = "".join(text_solid)
            h1_list = self.__get_h1_before_h2(html)
            h2_list = self.__divide_by_tag(html,"h2")
            together = [h1_list + h2_list]
            texts.append(together)
        return texts

divider = TextDivider("garmoni.docx")
controller = TextController(divider.complete_divide())
controller.get_right_json()

