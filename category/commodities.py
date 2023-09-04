
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.common.alert import Alert
import requests

file_path = os.path.join("/home/ben/Documents/freelancer/web-scrap/tests/production2/scraping-financial-juice/category/noted-headline", "commodities.txt")

def scroll_to_element(driver, element):
    # Scroll to the element using JavaScript
    script = "arguments[0].scrollIntoView();"
    driver.execute_script(script, element)

def scrape_articles_commodities(url, driver):
    try:
        # Membuka halaman web menggunakan WebDriver yang sudah login
        driver.get(url)

        # Tunggu sebentar agar konten AJAX dimuat sepenuhnya
        # time.sleep(10)

        response = requests.get(url)
        print(f"Response halaman page commodities setelah login: {response.status_code}")

        try:
            # Coba dapatkan teks dari pop-up prompt
            alert = Alert(driver)
            alert_text = alert.text  # Dapatkan teks pop-up prompt
            print("Pop-up prompt: ", alert_text)
            alert.dismiss()
        except Exception as e:
                # Tangani kasus jika pop-up prompt tidak ada
            print("Tidak ada pop-up prompt yang ditemukan")

        try:
            alert = driver.switch_to.alert
            # Jika alert muncul, dapatkan teks pada alert dan cetak ke konsol
            alert_text = alert.text
            print('Teks pada alert:', alert_text)
            alert.accept()
            # Klik tombol "Cancel" dengan menggunakan ID tombolnya
            # dismiss_button_id = "onesignal-slidedown-cancel-button"  # Ganti dengan ID tombol "Cancel" yang sesuai
            # driver.execute_script(f"document.getElementById('{dismiss_button_id}').click()")

            # Tunggu beberapa saat untuk melihat efek setelah menutup alert (opsional)
            driver.implicitly_wait(2)

        except Exception as e:
            # Jika alert tidak muncul, lanjutkan eksekusi kode Anda
            print('Tidak ada alert yang muncul.')

        wait = WebDriverWait(driver, 10)
  
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="aspnetForm"]/div[3]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/ul/li[4]/a')))
        click_element = driver.find_element(by=By.XPATH,value='//*[@id="aspnetForm"]/div[3]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/ul/li[4]/a')
        driver.execute_script('arguments[0].click()',   click_element)

        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"headline-title"))) #sangat berguna, jadi ketika class ini sudah muncul,maka baru di page source
        with open(file_path, "r") as file:
            headline_id = file.read()

        results = []
        last_headline_id = headline_id
        print(last_headline_id)
        

 
        while True:
        # Scroll to the last headline_id found in the previous iteration
            if last_headline_id:
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainFeed"]/div[1]')))

                    i = True
                    while i:
                        try:
                            alert = driver.switch_to.alert
                            alert_text = alert.text
                            print('Teks pada alert:', alert_text)
                            alert.accept()
                            driver.implicitly_wait(2)

                        except Exception as e:
                            print('Tidak ada alert yang muncul.')
                        
                        html = driver.find_element(By.TAG_NAME, 'html')
                        html.send_keys(Keys.PAGE_DOWN)
                        # Add some waiting time to allow content to load
                        driver.implicitly_wait(20)  # Set the implicit wait time as needed

                        ###
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        articles = soup.find_all('div', attrs={'data-headlineid': True})
                        for article in articles:
                            headline_id = article['data-headlineid']
                            if headline_id == last_headline_id:
                                print("Selesai scroll commodities")
                                i = False
                                time.sleep(5) # break sebelum di tutup, bukan ketika di scrool
                                break

                except  Exception as e: 
                    print("Error ketika page source di:", e)
                    break
            


            # Wait for new content to load
            driver.implicitly_wait(10)  # Set the implicit wait time as needed

            # Get the updated page source
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            articles = soup.find_all('div', attrs={'data-headlineid': True})

            # Check if there's any new data loaded
            if not articles:
                break

            # Find new data based on data-headlineid
            for article in articles:
                headline_id = article['data-headlineid']
                if headline_id != '0' and (last_headline_id is None or int(headline_id) > int(last_headline_id)):
                    parent_title = article.find('p', class_='headline-title')
                    if parent_title is not None:
                        anchor_element = parent_title.find('a') or parent_title.find('span')
                        if anchor_element is not None:
                            text_inside_a_tag = anchor_element.text.strip()
                            # latest_id_to_save = headline_id
                            results.append({'idData': headline_id, 'title': text_inside_a_tag})
            if articles:
                last_headline_id = articles[-1]['data-headlineid']      
                if last_headline_id == headline_id:  # Check if the last data is the same as the current one
                    print("selesai scrapping commodities")
                    break

        if results:
           with open(file_path, "w") as file:
                file.write(results[0]['idData'])

        return results


    except Exception as e:
        print("Error ketika scrapping:", e)
        raise e