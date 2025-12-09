from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# 1. إعداد التطبيق
app = FastAPI(title="Drug Prediction API")

# 2. تحميل "ذاكرة" النموذج
# يتم تحميل الملف مرة واحدة عند بدء تشغيل السيرفر
assets = joblib.load("drug_model_assets.pkl")

model = assets["model"]
scaler = assets["scaler"]
encoders = assets["encoders"]
target_encoder = assets["target_encoder"]
feature_columns = assets["feature_columns"]

# 3. تحديد شكل المدخلات (الواجهة)
class DrugInput(BaseModel):
    Age: int
    Sex: str        # مثال: "F" أو "M"
    BP: str         # مثال: "HIGH", "LOW", "NORMAL"
    Cholesterol: str # مثال: "HIGH", "NORMAL"
    Na_to_K: float

@app.get("/")
def home():
    return {"message": "API تعمل بنجاح. اذهب إلى /docs لرؤية الواجهة."}

@app.post("/predict")
def predict_drug(data: DrugInput):
    try:
        # تحويل البيانات القادمة إلى DataFrame
        input_data = pd.DataFrame([data.dict()])
        
        # معالجة البيانات بنفس طريقة التدريب تماماً
        
        # أ. تحويل النصوص إلى أرقام (Encoding)
        for col, le in encoders.items():
            # التحقق من أن القيمة المدخلة صحيحة
            val = input_data[col].iloc[0]
            if val not in le.classes_:
                return {"error": f"قيمة غير صحيحة للحقل {col}. القيم المسموحة: {list(le.classes_)}"}
            input_data[col] = le.transform(input_data[col])

        # ب. التأكد من ترتيب الأعمدة
        input_data = input_data[feature_columns]

        # ج. توحيد المقاييس (Scaling)
        input_scaled = scaler.transform(input_data)

        # د. التوقع
        prediction_index = model.predict(input_scaled)
        
        # هـ. تحويل الرقم المتوقع إلى اسم الدواء (مثلاً 0 يصبح drugY)
        prediction_name = target_encoder.inverse_transform(prediction_index)

        return {
            "prediction": prediction_name[0],
            "input_received": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # Update code