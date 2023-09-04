import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import http.client
import json
import threading
import time


#IMPORT BY CATEGORY
from category.my_news import scrape_articles_my_news
from category.bonds import scrape_articles_bonds
from category.commodities import scrape_articles_commodities
from category.crypto import scrape_articles_crypto
from category.equities import scrape_articles_equities
from category.forex import scrape_articles_forex
from category.indexes import scrape_articles_indexes
from category.macro import scrape_articles_macro
from category.risk import scrape_articles_risk

def login_to_website(email, password):
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    try:
        # Membuka halaman login
        login_url = 'https://www.financialjuice.com/home'  
        driver.get(login_url)

        # Tunggu sebentar agar halaman login dimuat
        
        response = requests.get(login_url)
        print(f"Response halaman: {response.status_code}")
        time.sleep(5)


        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(), 'Sign In')]"))) 
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='ctl00_SignInSignUp_loginForm1_inputEmail']"))) 
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='ctl00_SignInSignUp_loginForm1_inputPassword']")))
        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='ctl00_SignInSignUp_loginForm1_btnLogin']"))) 

        sign_in_button = driver.find_element(by=By.XPATH, value="//a[contains(text(), 'Sign In')]")
        if not sign_in_button:
            print("terkena batasan limit cloudfla")
        sign_in_button.click()

        time.sleep(3)

        email_input = driver.find_element(by=By.XPATH,value="//input[@id='ctl00_SignInSignUp_loginForm1_inputEmail']")
        password_input = driver.find_element(by=By.XPATH,value="//input[@id='ctl00_SignInSignUp_loginForm1_inputPassword']")

        email_input.send_keys(email)
        password_input.send_keys(password)

        # Klik tombol login
        login_button = driver.find_element(by=By.XPATH, value="//*[@id='ctl00_SignInSignUp_loginForm1_btnLogin']")
        login_button.click()

        

    except Exception as e:
        print("Error during login:", e)
        raise e

    return driver

def scraping_task():
    max_execution_time_ms = 300000  # 300000 milidetik (300 detik)

    try:
        start_time = time.time()  # Waktu mulai scraping
        #MY_NEWS
        scraped_articles_my_news = scrape_articles_my_news(url, driver)
        while True:
            if (time.time() - start_time) * 1000 > max_execution_time_ms:
                print("Scraping berhenti karena waktu telah habis.")
                break
            if scraped_articles_my_news:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_my_news)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                

                
            else:
                print("Artikel My News kosong")

            # # time.sleep(10)

            scraped_articles_bonds = scrape_articles_bonds(url, driver)
            if scraped_articles_bonds:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_bonds)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response bonds:", conn.getresponse().status)
            else:
                print("Artikel Bonds kosong")


        # # time.sleep(10)

            scraped_articles_commodities = scrape_articles_commodities(url, driver)
            if scraped_articles_commodities:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_commodities)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                # print("Response commodities:", conn.getresponse().status)
            else:
                print("Artikel commodities kosong")

            # # time.sleep(10)

            scraped_articles_crypto = scrape_articles_crypto(url, driver)
            if scraped_articles_crypto:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_crypto)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response crypto:", conn.getresponse().status)
            else:
                print("Artikel crypto kosong")

            # # time.sleep(10)

            scraped_articles_equities = scrape_articles_equities(url, driver)
            if scraped_articles_equities:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_equities)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                # print("Response equities:", conn.getresponse().status)
            else:
                print("Artikel equities kosong")

            
            # time.sleep(10)

            scraped_articles_forex = scrape_articles_forex(url, driver)
            if scraped_articles_forex:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_forex)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response forex:", conn.getresponse().status)
            else:
                print("Artikel forex kosong")
            
            # # time.sleep(10)

            scraped_articles_indexes = scrape_articles_indexes(url, driver)
            if scraped_articles_indexes:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_indexes)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response indexes:", conn.getresponse().status)
            else:
                print("Artikel indexes kosong")
            
            # time.sleep(10)


            scraped_articles_macro = scrape_articles_macro(url, driver)
            if scraped_articles_macro:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_macro)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response macro:", conn.getresponse().status)
            else:
                print("Artikel macro kosong")
            
            # time.sleep(10)

            scraped_articles_risk = scrape_articles_risk(url, driver)
            if scraped_articles_risk:
                # SEND TO SERVER
                # Mengonversi data menjadi format JSON
                json_data = json.dumps(scraped_articles_risk)

                # Mengirim data JSON ke server menggunakan POST request
                conn = http.client.HTTPConnection("localhost", 3001)
                headers = {'Content-type': 'application/json'}
                conn.request("POST", "/", json_data, headers)
                print("Response risk:", conn.getresponse().status)
            else:
                print("Artikel risk kosong")
    
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
    
    finally:
        # Tutup browser dan bebas sumber daya lainnya
        driver.quit()



if __name__ == "__main__":
    email = 'pemudaaja789@gmail.com'
    password = 'Admin'

    driver = login_to_website(email, password)
    time.sleep(5)
    url = 'https://www.financialjuice.com/home' 

    scraping_task()


    # Buat thread untuk menjalankan scraping
    # scraping_thread = threading.Thread(target=scraping_task)

    # # Mulai thread scraping
    # scraping_thread.start()

    # # Tunggu maksimum waktu eksekusi
    # max_execution_time = 20  # 5 menit
    # scraping_thread.join(1)
    # stop_thread = True
    
    # if scraping_thread.is_alive():
    #     print("Scraping berhenti karena waktu telah habis.")
    #     # Hentikan thread secara manual jika perlu
    #     scraping_thread._stop()
    # else:
    #     print("Scraping selesai dalam waktu yang ditentukan.")


    # Tutup WebDriver setelah selesai
    # driver.quit()
