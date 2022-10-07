import requests
from bs4 import BeautifulSoup
import re
import urllib3
import pandas as pd


file = open("medicine_list.csv", 'a', encoding='UTF-8')

# https://www.1mg.com/drugs-all-medicines?page=911

main_header = {"authority": "www.1mg.com",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
               }

header = {"authority": "www.1mg.com:authority: www.1mg.com",
          "referer": "https://www.1mg.com/drugs-all-medicinesreferer: https://www.1mg.com/drugs-all-medicines",
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"
          }

sess = requests.session()


def all_links(url):
    res = sess.get(url, headers=main_header)
    soup = BeautifulSoup(res.content, "html.parser")
    # print(soup)
    links = soup.find(class_='style__inner-container___3BZU9 style__product-grid___3noQW style__padding-top-bottom-12px___1-DPF')
    for link in links:
        link = re.search('(?:href=")(.*)" target', str(link))
        # link = urllib.parse.urljoin(url, link.group(1))
        print(link)
        medicine_data(link)


def medicine_data(url):
        # print(res.url)
        try:
            res = sess.get(url, headers=header)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                if "otc" in res.url:
                    otc_med_data(soup)
                else:
                    non_otc_med_data(soup)
        except requests.exceptions.ConnectionError:
            pass


def non_otc_med_data(soup):
    cols = ['title', 'manufacturers', 'salt_composition', 'salt_SYNONYMS', 'drug_prescription','storage', 'side_effect', 'price', 'strip',
            'treatment', 'url', 'Manufacturer_Marketer_address', 'description', 'country', 'Category']
    rows = []
    if soup.find(class_='DrugHeader__header-content___f6GbC') is not None:
        title = soup.find(class_='DrugHeader__header-content___f6GbC').text
        print(title)
        manufacturers = soup.find(class_='DrugHeader__meta-value___vqYM0').text
        salt_composition = soup.find(class_='saltInfo').text
        if len(soup.findAll(class_='saltInfo DrugHeader__meta-value___vqYM0')) == 2:
            storage = soup.findAll(class_='saltInfo DrugHeader__meta-value___vqYM0')[1].text
        else:
            storage = "Not Mention"
        side_effect = soup.find(class_='DrugOverview__list-container___2eAr6 DrugOverview__content___22ZBX')
        if soup.find(class_='PriceBoxPlanOption__margin-right-4___2aqFt PriceBoxPlanOption__stike___pDQVN') is not None:
            price = soup.find(class_='PriceBoxPlanOption__margin-right-4___2aqFt PriceBoxPlanOption__stike___pDQVN').text
            # print(price)
        elif soup.find(class_='style__strike-price___3Ag3J') is not None:
            price = soup.find(class_='style__strike-price___3Ag3J').text
            # print(price)
        elif soup.find(class_='DrugPriceBox__slashed-price___2UGqd') is not None:
            price = soup.find(class_='DrugPriceBox__slashed-price___2UGqd').text
        elif soup.find(class_='DrugPriceBox__price___dj2lv') is not None:
            price = soup.find(class_='DrugPriceBox__price___dj2lv').text
        elif soup.find(class_='PriceBoxPlanOption__offer-price___3v9x8 PriceBoxPlanOption__offer-price-cp___2QPU_') is not None:
            price = soup.find(class_='PriceBoxPlanOption__offer-price___3v9x8 PriceBoxPlanOption__offer-price-cp___2QPU_').text
            # print(price)
        else:
            price = 'NOT Mention'
            # print(price)
        if soup.find(class_="DrugPriceBox__quantity___2LGBX") is not None:
            strip = soup.find(class_="DrugPriceBox__quantity___2LGBX").text
            # print(strip)
        else:
            strip = 'NOT Mention'
            # print(strip)
        if soup.find(class_='DrugOverview__list___1HjxR DrugOverview__uses___1jmC3') is not None:
            treatment = soup.find(class_='DrugOverview__list___1HjxR DrugOverview__uses___1jmC3').text
        else:
            treatment = 'NOT Mention'
        if soup.find(class_='saltInfo DrugHeader__underline___f4HNk DrugHeader__meta-value___vqYM0') is not None:
            salt_SYNONYMS = soup.find(class_='saltInfo DrugHeader__underline___f4HNk DrugHeader__meta-value___vqYM0').text
            # print(salt_SYNONYMS)
        else:
            salt_SYNONYMS = 'NOT Mention'
        if soup.find(class_='DrugPage__manufacturer-address___2ACya') is not None:
            Manufacturer_Marketer_address = soup.find(class_='DrugPage__manufacturer-address___2ACya').text
        else:
            Manufacturer_Marketer_address = 'Not Mention'
        if soup.find(class_="DrugHeader__prescription-req___34WVy") is not None:
            drug_prescription = soup.find(class_="DrugHeader__prescription-req___34WVy").text
        else:
            drug_prescription = "NOT Aviable"
        if soup.find(class_="DrugPage__vendors___R1Bnk") is not None:
            origin_country = soup.find(class_="DrugPage__vendors___R1Bnk").text
            if 'Expires' in origin_country:
                country = re.search("Country of origin:(.*)Expires", origin_country)
                country = country.group(1)
            else:
                country = re.search("Country of origin:(.*)", origin_country)
                country = country.group(1)
            # print(len(origin_country))
        elif soup.find(class_='VendorInfo__container___-iV1S') is not None:
            origin_country = soup.find(class_="VendorInfo__container___-iV1S").text
            if 'Expires' in origin_country:
                country = re.search("Country of origin:(.*)Expires", origin_country)
                country = country.group(1)
            else:
                country = re.search("Country of origin:(.*)", origin_country)
                country = country.group(1)
        else:
            country = "NOT Mention"
        # print(drug_prescription)
        rows.append({
            cols[0]: title,
            cols[1]: manufacturers,
            cols[2]: salt_composition,
            cols[3]: salt_SYNONYMS,
            cols[4]: drug_prescription,
            cols[5]: str(storage),
            cols[6]: side_effect,
            cols[7]: str(price),
            cols[8]: strip,
            cols[9]: str(treatment),
            cols[10]: url,
            cols[11]: Manufacturer_Marketer_address,
            cols[13]: country,

            cols[14]:'NON OTC'
        })
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    data_save(df)


def otc_med_data(soup):
    cols = ['title', 'manufacturers', 'salt_composition', 'salt_SYNONYMS', 'drug_prescription', 'storage', 'side_effect', 'price', 'strip',
            'treatment', 'url', 'Manufacturer_Marketer_address', 'description', 'country', 'Category']
    rows = []
    if soup.find(class_='ProductTitle__product-title___3QMYH') is not None:
        title = soup.find(class_='ProductTitle__product-title___3QMYH').text
        print(title, 'otc')
        manufacturers = soup.find(class_='ProductTitle__manufacturer___sTfon').text
        salt_composition = "Not Mention"
        storage = "Not Mention"  # soup.findAll(class_='saltInfo DrugHeader__meta-value___vqYM0')[1].text
        side_effect = soup.find(class_='DrugOverview__list-container___2eAr6 DrugOverview__content___22ZBX')
        if soup.find(class_='PriceBoxPlanOption__margin-right-4___2aqFt PriceBoxPlanOption__stike___pDQVN') is not None:
            price = soup.find(class_='PriceBoxPlanOption__margin-right-4___2aqFt PriceBoxPlanOption__stike___pDQVN').text
            # print(price)
        elif soup.find(class_='style__strike-price___3Ag3J') is not None:
            price = soup.find(class_='style__strike-price___3Ag3J').text
            # print(price)
        elif soup.find(class_='DrugPriceBox__slashed-price___2UGqd') is not None:
            price = soup.find(class_='DrugPriceBox__slashed-price___2UGqd').text
            # print(price)
        elif soup.find(class_='DrugPriceBox__price___dj2lv') is not None:
            price = soup.find(class_='DrugPriceBox__price___dj2lv').text
        elif soup.find(class_='PriceBoxPlanOption__offer-price___3v9x8 PriceBoxPlanOption__offer-price-cp___2QPU_') is not None:
            price = soup.find(class_='PriceBoxPlanOption__offer-price___3v9x8 PriceBoxPlanOption__offer-price-cp___2QPU_').text
        else:
            price = 'NOT Mention'
            # print(price)
        if soup.find(class_="OtcPriceBox__add-box___3rvCP") is not None:
            strip = soup.find(class_="OtcPriceBox__add-box___3rvCP").text
            # print(strip)
        elif soup.find(class_="style__pack-size___3nfIS") is not None:
            strip = soup.find(class_="style__pack-size___3nfIS").text
            # print(strip)
        else:
            strip = 'NOT Mention'
            # print(strip)
        if soup.find(class_='DrugOverview__list___1HjxR DrugOverview__uses___1jmC3') is not None:
            treatment = soup.find(class_='DrugOverview__list___1HjxR DrugOverview__uses___1jmC3').text
        else:
            treatment = 'NOT Mention'
        if soup.find(class_='saltInfo DrugHeader__underline___f4HNk DrugHeader__meta-value___vqYM0') is not None:
            salt_SYNONYMS = soup.find(
                class_='saltInfo DrugHeader__underline___f4HNk DrugHeader__meta-value___vqYM0').text
        else:
            salt_SYNONYMS = 'NOT Mention'
        if soup.find(class_='OtcPage__manufacturer-address___3ugdE') is not None:
            Manufacturer_Marketer_address = soup.find(class_='OtcPage__manufacturer-address___3ugdE').text
        else:
            Manufacturer_Marketer_address = 'Not Mention'

        description = soup.findAll(class_='ProductDescription__description-content___A_qCZ')

        if soup.find(class_="DrugHeader__prescription-req___34WVy") is not None:
            drug_prescription = soup.find(class_="DrugHeader__prescription-req___34WVy").text
            # print(drug_prescription)
        else:
            drug_prescription = "NOT Mention"
        if soup.find(class_="DrugPage__vendors___R1Bnk") is not None:
            origin_country = soup.find(class_="DrugPage__vendors___R1Bnk").text
            if 'Expires' in origin_country:
                country = re.search("Country of origin:(.*)Expires", origin_country)
                country = country.group(1)
            else:
                country = re.search("Country of origin:(.*)", origin_country)
                country = country.group(1)
            # print(len(origin_country))
        elif soup.find(class_='VendorInfo__container___-iV1S') is not None:
            origin_country = soup.find(class_="VendorInfo__container___-iV1S").text
            if 'Expires' in origin_country:
                country = re.search("Country of origin:(.*)Expires", origin_country)
                country = country.group(1)
            else:
                country = re.search("Country of origin:(.*)", origin_country)
                country = country.group(1)
        else:
            country = "NOT Mention"

        rows.append({
            cols[0]: title,
            cols[1]: manufacturers,
            cols[2]: salt_composition,
            cols[3]: salt_SYNONYMS,
            cols[4]: drug_prescription,
            cols[5]: str(storage),
            cols[6]: side_effect,
            cols[7]: str(price),
            cols[8]: strip,
            cols[9]: str(treatment),
            cols[10]: url,
            cols[11]: Manufacturer_Marketer_address,
            cols[12]: description,
            cols[13]: country,
            cols[14]:'OTC'
            })
    df = pd.DataFrame(rows, columns=cols)
    print(df)
    data_save(df)


def data_save(df):
    print(df)
    df.to_csv(file, index=False, line_terminator='\n', header=False)

# url = 'https://www.1mg.com/drugs/tfct-nib-tablet-639098'
#
# medicine_data(url)


for i in range(138000, 138660):
    url = "https://www.1mg.com/drugs/" + str(i)
    print(url)
    medicine_data(url)
    # all_links(url)
