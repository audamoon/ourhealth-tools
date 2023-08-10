import requests
from bs4 import BeautifulSoup
from func.google_sheet_mgr import SheetManager

gs = SheetManager("1WsAf_t2PuLD4qowmv5zYyp7YMNpyuSsN0Ir35u5aWQk")
a = gs.get_values("A")
array = []
for els in a:
    print(els)
    for url in els:
        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all elements with the class "open-modal city"
                elements = soup.find_all(class_="contacts-page__wrapper content-body")

                # Print the text content of each element
                array.append(elements[0].findChildren("p")[3].text.strip().split(',')[0].replace("Адрес: ",""))
            else:
                print(f"Failed to connect. Status code: {response.status_code}")
                array.append("Не нашёл")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to the website: {e}")
            array.append("Не нашёл")
print(array)
gs.write_column_from_array("B1:B20",array)
