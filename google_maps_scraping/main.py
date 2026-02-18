# main.py
from scraper import GoogleMapsScraper
from storage import DataStorage
from config import SEARCH_KEYWORD, LOCATION, MAX_RESULTS
import logging


def run_project():
    # 1. تهيئة السكرابر
    bot = GoogleMapsScraper()

    try:
        # 2. البحث عن الكلمة والموقع
        bot.search(SEARCH_KEYWORD, LOCATION)

        # 3. التمرير لجلب العدد المطلوب من النتائج
        bot.scroll_sidebar(MAX_RESULTS)

        # 4. استخراج البيانات التفصيلية (الأسماء، الهواتف، العناوين)
        leads_data = bot.extract_data()

        # 5. التخزين والمعالجة
        DataStorage.save_to_excel(leads_data)

    except Exception as e:
        logging.error(f" حدث خطأ غير متوقع في البرنامج: {e}")

    finally:
        # 6. إغلاق المتصفح
        bot.close()
        logging.info(" انتهت المهمة.")


if __name__ == "__main__":
    run_project()
