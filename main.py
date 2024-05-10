import json
import csv
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def Writer(data_dict, data_name):
    with open(f"data/{data_name}.json", "a", encoding="utf-8") as file:
        json.dump(data_dict, file, indent=4, ensure_ascii=False)

    csv_file = open(f'data/{data_name}.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)

    for ex in data_dict:
        writer.writerow(ex.values())

    csv_file.close()

def Scraper(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        counter = 1
        result = []
        #with open(f"data/{url.split("/")[-2]}.html", "w") as file:
        #    file.write(response.text)

        with open(f"data/{url.split("/")[-2]}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        watches_blocks = soup.find_all("div", class_="row mb-40")

        for watches_block in watches_blocks:
            watch_list = watches_block.find_all("div", class_="small-6 medium-4 large-3 column end mt-40 overview-watch-one-item")

            for watch in watch_list:
                try:
                    watch_name = watch.find("a").find("span").find("b").text
                except Exception:
                    print(f"g-shock {counter} haven't name")
                watch_link = "https:" + watch.find("a").get("href")
                response_exemplar = requests.get(watch_link, headers=headers)
                if response_exemplar.status_code == 200:
                    soup_exemplar = BeautifulSoup(response_exemplar.text, "lxml")
                    try:
                        img_link = soup_exemplar.find("img", class_="colldetail-zoom-main").get("src")
                    except Exception:
                        print(f"g-shock {counter} haven't photo")
                    properties_blocks = soup_exemplar.find_all("div", class_="small-12 medium-6 large-6 column")

                    properties = []
                    try:
                        for properties_block in properties_blocks:
                            for div in properties_block.find_all("div"):
                                if div.find("a"):
                                    propert = {div.find("a").text.strip(): div.find("a").next_sibling.next_sibling.text.strip()}
                                    properties.append(propert)
                    except Exception:
                        print(f"g-shock {counter} haven't properties")

                    result.append(
                        {
                            "g-shock name": watch_name,
                            "g-shock photo link": img_link,
                            "properties of g-shock": properties
                        }
                    )
                print(f"g-shock {counter} scraping was successful")
                counter += 1
        Writer(result, url.split("/")[-2])

    else:
        print("Request Error")
    print("scraping was successful")
                    
def main():
    Scraper("https://www.g-shock.eu/euro/watches/")
    print(f"\n{"#" *20}\n")
    Scraper("https://www.g-shock.eu/euro/watches-women/")

if __name__ == "__main__":
     main()