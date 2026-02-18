# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import WAIT_TIME, HEADLESS_MODE, MAX_RESULTS  # أضف MAX_RESULTS هنا
import logging
from config import WAIT_TIME, HEADLESS_MODE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GoogleMapsScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        if HEADLESS_MODE:
            options.add_argument('--headless')
        # حل مشكلة التعارض في النسخ الحديثة
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)

    def search(self, keyword, location):
        query = f"{keyword} {location}"
        logging.info(f" جاري فتح الخريطة الأساسية والبحث عن: {query}")

        # الرابط الذي يعمل عندك يقيناً
        base_url = "https://www.google.com/maps/@35.0569866,35.8934105,11z"

        try:
            self.driver.get(base_url)
            # انتظار طويل لأن الخرائط في سوريا تأخذ وقتاً للتحميل
            time.sleep(15)

            # محاولة إيجاد مربع البحث بأكثر من طريقة (Selector) لضمان النجاح
            try:
                search_box = self.wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
            except:
                # إذا فشل الـ ID نجرب الـ Name
                search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))

            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)

            logging.info(" تم كتابة نص البحث وضغط Enter...")
            # انتظار ظهور القائمة الجانبية بعد البحث
            time.sleep(15)

            self.driver.save_screenshot("after_search.png")
            logging.info(" تم حفظ لقطة الشاشة after_search.png")

        except Exception as e:
            logging.error(f" لم نتمكن من الوصول لمربع البحث: {e}")
            self.driver.save_screenshot("error_state.png")

    def scroll_sidebar(self, max_results):
        logging.info(" جاري التمرير داخل القائمة الجانبية...")
        try:
            # البحث عن القائمة الجانبية (التي تحتوي على النتائج)
            sidebar = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))

            items_found = 0
            while items_found < max_results:
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', sidebar)
                time.sleep(3)
                # حساب عدد النتائج التي ظهرت
                current_items = self.driver.find_elements(By.CLASS_NAME, "hfpxzc")
                if len(current_items) == items_found: break  # وصلنا للنهاية
                items_found = len(current_items)
                logging.info(f" تم تحميل {items_found} نتيجة...")
                if items_found >= max_results: break
        except Exception as e:
            logging.error(f" خطأ أثناء التمرير: {e}")

    def extract_data(self):
        logging.info(" جاري سحب البيانات التفصيلية...")
        results_data = []

        # إعادة جلب العناصر للتأكد من وجودها بعد الـ Scroll
        places = self.driver.find_elements(By.CLASS_NAME, "hfpxzc")

        # تحديد العدد النهائي للسحب (الأصغر بين ما وجدناه وبين المطلوب)
        limit = min(len(places), MAX_RESULTS)

        for i in range(limit):
            try:
                # إعادة جلب القائمة في كل مرة لتجنب خطأ العناصر القديمة (Stale Element)
                current_places = self.driver.find_elements(By.CLASS_NAME, "hfpxzc")
                place = current_places[i]

                name = place.get_attribute("aria-label")

                # التمرير للعنصر قبل الضغط عليه
                self.driver.execute_script("arguments[0].scrollIntoView();", place)
                time.sleep(1)
                place.click()
                time.sleep(3)  # وقت لتحميل البيانات على اليمين

                try:
                    address = self.driver.find_element(By.XPATH, '//button[@data-item-id="address"]').text
                except:
                    address = "N/A"

                try:
                    phone = self.driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone")]').text
                except:
                    phone = "N/A"

                results_data.append({
                    "الاسم": name,
                    "العنوان": address,
                    "رقم الهاتف": phone
                })
                logging.info(f"📍 [{i + 1}/{limit}] تم سحب: {name}")

            except Exception as e:
                logging.warning(f"⚠️ تخطي العنصر {i + 1} بسبب خطأ بسيط")
                continue

        return results_data

    def close(self):
        self.driver.quit()


