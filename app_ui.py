import streamlit as st
import requests

# عنوان الصفحة
st.title("💊 نظام التنبؤ بالدواء المناسب")
st.write("أدخل بيانات المريض للحصول على التوقع من الذكاء الاصطناعي")

# 1. إدخال البيانات من المستخدم (واجهة سهلة)
age = st.number_input("العمر", min_value=1, max_value=100, value=30)
sex = st.selectbox("الجنس", ["M", "F"])
bp = st.selectbox("مستوى ضغط الدم (BP)", ["HIGH", "LOW", "NORMAL"])
cholesterol = st.selectbox("مستوى الكوليسترول", ["HIGH", "NORMAL"])
na_to_k = st.number_input("نسبة الصوديوم إلى البوتاسيوم (Na_to_K)", value=15.0)

# 2. زر التوقع
if st.button("توقع الدواء"):
    # تجهيز البيانات لإرسالها للرابط الخاص بك
    # (لاحظ: استبدل الرابط أدناه برابط موقعك الحقيقي على Render)
    api_url = "https://my-api-pxoj.onrender.com/predict"
    
    input_data = {
        "Age": age,
        "Sex": sex,
        "BP": bp,
        "Cholesterol": cholesterol,
        "Na_to_K": na_to_k
    }

    try:
        # الاتصال بالـ API
        response = requests.post(api_url, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            drug_name = result["prediction"]
            st.success(f"الدواء المقترح هو: {drug_name}")
        else:
            st.error("حدث خطأ في الاتصال بالسيرفر!")
            st.write(response.text)
            
    except Exception as e:
        st.error(f"حدث خطأ: {e}")