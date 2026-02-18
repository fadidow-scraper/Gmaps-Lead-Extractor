# storage.py
import pandas as pd
import os
from config import OUTPUT_FILE


class DataStorage:
    @staticmethod
    def save_to_excel(data):
        if not data:
            print(" لا توجد بيانات لحفظها.")
            return

        # تحويل القائمة إلى DataFrame
        df = pd.DataFrame(data)

        # حذف المكررات بناءً على الاسم ورقم الهاتف
        df.drop_duplicates(subset=['الاسم', 'رقم الهاتف'], inplace=True)

        # الحفظ بصيغة Excel
        try:
            df.to_excel(OUTPUT_FILE, index=False, engine='openpyxl')
            print(f" تم حفظ {len(df)} نتيجة في ملف: {OUTPUT_FILE}")

            # فتح المجلد تلقائياً لمشاهدة النتيجة
            os.startfile(os.getcwd())
        except Exception as e:
            print(f" حدث خطأ أثناء الحفظ: {e}")
