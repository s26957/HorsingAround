from datetime import datetime, date
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

breeds = """
 Koń czystej krwi arabskiej
 Koń pełnej krwi angielskiej
 Koń luzytański
 Cob Irlandzki
 Koń holsztyński
 Mustang
 Koń achał-tekiński
 Walijski kuc górski
 Osioł
 Nokota
 Criollo
 Tennessee Walker
 Kuc szetlandzki
 Pinto
 Quarter Horse
 Kłusak francuski
 Koń andaluzyjski
 Angloarab Shagya
 Knabstrup
 Koń fryzyjski
 Hunter Irlandzki
 Koń hanowerski
 Koń fiordzki
 Bashkir Curly
 Marwari
 Kuc nowofunlandzki
 Appaloosa
 Kerry Bog
 Holenderski koń gorącokrwisty
 Kuc Connemara
 Koń islandzki
 Selle français
 Koń Drum
 Haflinger
 Koń lipicański
 Koń trakeński
 Perszeron
 Shire
 Koń doński
 Kucyk Highland
 Koń berberyjski
 Camargue
 Mangalarga Marchador
 Koń fiński
 Kuc belgijski
 Konik polski
 Koń ban´ei
"""

number_of_loops = 20 #one loop takes ~20 seconds
breeds_data = {}
prev_horses = []
save_file_name = "dane.txt" #file for emergency saves of all transactions
save_file = open(save_file_name, 'a')

for breed in breeds.split('\n'):
    breeds_data[breed[1::]] = []

login = "TotallyHuman"
password = "!@34QWer"

driver = webdriver.Chrome()
driver.get("https://www.howrse.pl/marche/vente/")

# logging:
search_LOG = driver.find_element(By.NAME, value="login")
search_LOG.send_keys(login)
search_PAS = driver.find_element(By.NAME, value="password")
search_PAS.send_keys(password)
search_PAS.send_keys(Keys.RETURN)

# go to auction page after logging
time.sleep(5)
driver.get("https://www.howrse.pl/marche/vente/")


def horse_compare(horse1, horse2):
    if len(horse1) != len(horse2):
        return False
    for index in range(len(horse1) - 3):
        if horse1[index] != horse2[index]:
            return False
    return True


try:
    for i in range(number_of_loops):
        # get list of auctions:
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "vente-chevaux"))
        )
        sales = main.text.split('\n')
        sales = sales[3::]
        i = 0
        j = 0
        horses = []
        print("CURRENT AUCTIONS:")
        while i < 4: #get first 4 horses
            horse = []
            not_found = True
            while (not_found):
                line = sales[j]
                horse.append(line)
                if line[(len(line) - 6)::] == "aukcji" \
                        or line[(len(line) - 6)::] == "aukcje" \
                        or line[(len(line) - 6)::] == "aukcja":
                    not_found = False
                j += 1
            horses.append(horse)
            print(horse)
            i = i + 1

        print()
        # analysing data - if horse was sold adding to breeds_data dir
        j = 0  # cofniecie indeksu
        for i in range(len(prev_horses)):
            if not horse_compare(prev_horses[i], horses[i - j]):
                # checking if horse was sold or audction ended without any bids
                print("horse auction dissappeard:", '\n', prev_horses[i])
                h = prev_horses[i]
                if h[len(h) - 1][0] > '0':
                    print("sold:")
                    # getting info about breed:
                    # for horses without nickname:
                    if h[2][0] >= 'A' and h[2][0] <= 'Z':
                        breeds_data[h[2]].append([h[len(h) - 2],
                                                  datetime.now().strftime("%m_%d_%H_%M")]) #appending breed and price and date
                        line = h[2] + "," + h[len(h) - 2] + ";"
                        print(line)
                        save_file.write(line)
                    # with nickname:
                    else:
                        breeds_data[h[3]].append([h[len(h) - 2],
                                                  datetime.now().strftime("%m_%d_%H_%M")])
                        line = h[3] + "," + h[len(h) - 2] + ";"
                        print(line)
                        save_file.write(line)
                j += 1
        prev_horses = horses
        print()
        time.sleep(20)
        driver.refresh()

    #saving results to file
    now = datetime.now()
    save_file_name = "data" + now.strftime("%m_%d_%H_%M") + ".txt"
    data_file = open(save_file_name, 'w')
    for b in breeds_data.keys():
        if len(breeds_data[b]) > 0:
            line = b + ":"
            print(b, ": ", breeds_data[b])
            for sale in breeds_data[b]:
                line = line + sale[0] + "," + sale[1] + ";"
            data_file.write(line + "\n")
    data_file.close()
except:
    print("oops something went wrong!")
    driver.quit()
    save_file.close()
