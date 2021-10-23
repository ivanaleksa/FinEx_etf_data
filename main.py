import requests
from bs4 import BeautifulSoup
import json
import csv


def get_data():
    # url = 'https://finex-etf.ru/products'
    headers = {
        'user - agent': 'Mozilla / 5.0(Windows NT 6.3;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                        '93.0.4577.82YaBrowser / 21.9.1.684 Yowser / 2.5 Safari / 537.36',
        'accept': '* / *'
    }
    """ забираем главную страницу сайта """
    # req = requests.get(url, headers=headers)
    # with open("data/index.html", "w", encoding="utf-8") as f:
    #     f.write(req.text)
    with open("data/index.html", "r", encoding="utf-8") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    list_link_soup = soup.find("div", class_="jss130").find_all("div", class_="jss134")
    list_link = ["https://finex-etf.ru" + item.find("a").get("href") for item in list_link_soup] # получаем ссылки на
    # страницы фондов
    data_bit = []
    data_bonds = []
    count = 1
    log = open("logs/logs.txt", "a", encoding="utf-8")
    for link in list_link:  # проходимся по страницам фондов и забираем данные
        """ забираем код страницы и записываем его в файл, чтобы не беспокоить лишний раз сайт """
        # req = requests.get(link, headers=headers)
        # with open(f"data/{link[-4:]}.html", "w", encoding="utf-8") as f:
        #     f.write(req.text)

        with open(f"data/{link[-4:]}.html", "r", encoding="utf-8") as f:
            src = f.read()
        soup = BeautifulSoup(src, "lxml")

        try:
            first_table = soup.find("div", class_="eknlvg65").find_all("div", class_="e1hxtrkz5")
            second_table = soup.find("div", class_="e5mda474").find_all("div", class_="e1be2p460")
            first_table_dict = {}
            second_table_dict = {}
            if second_table[0].text == "Акции":
                first_table_dict["Название фонда"] = f"{link[-4:]}"
                first_table_dict["Комиссия фонда"] = first_table[1].text
                first_table_dict["Стоймость 1 акций"] = first_table[2].text
                first_table_dict["Годовая доходность в рублях"] = first_table[3].text
                first_table_dict["Годовая доходность в долларах"] = first_table[4].text
                first_table_dict["Инструмент фонда"] = second_table[0].text
                first_table_dict["Дата создания фонда"] = second_table[4].text
                first_table_dict["Валюта фонда"] = second_table[6].text
                first_table_dict["Волатильность"] = second_table[12].text
                data_bit.append(first_table_dict)
            else:
                second_table_dict["Название фонда"] = f"{link[-4:]}"
                second_table_dict["Комиссия фонда"] = first_table[1].text
                second_table_dict["Стоймость 1 акций"] = first_table[2].text
                second_table_dict["Годовая доходность в рублях"] = first_table[3].text
                second_table_dict["Годовая доходность в долларах"] = first_table[4].text
                second_table_dict["Инструмент фонда"] = second_table[0].text
                second_table_dict["Дата создания фонда"] = second_table[4].text
                second_table_dict["Валюта фонда"] = second_table[6].text
                second_table_dict["Волатильность"] = second_table[12].text
                data_bonds.append(second_table_dict)
            log.write(f"Complete {count} step ({link[-4:]}.html)\n")
            count += 1
        except AttributeError:
            log.write(f"Error in file {link[-4:]}.html. Don't found class\n")
    with open("data_etf_bits.json", "w", encoding="utf-8") as f:
        json.dump(data_bit, f, indent=4, ensure_ascii=False)
    with open("data_etf_bonds.json", "w", encoding="utf-8") as f:
        json.dump(data_bonds, f, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == "__main__":
    main()
