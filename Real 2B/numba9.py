import pandas as pd # ใช้สำหรับการจัดการข้อมูลในรูปแบบ DataFrame

# ข้อมูลทดสอบ: actual คือค่าจริงจากหมอ, predicted คือค่าที่ได้จาก AI
df = pd.DataFrame({
    'actual':    ['Positive', 'Negative', 'Positive', 'Positive', 'Negative', 'Negative', 'Positive', 'Negative'],
    'predicted': ['Positive', 'Negative', 'Negative', 'Positive', 'Positive', 'Negative', 'Positive', 'Negative']
})

def get_confusion_matrix(df):
    # True Positive: ทำนายว่าเป็น และเป็นจริง
    tp = ((df['actual'] == 'Positive') & (df['predicted'] == 'Positive')).sum()
    # False Positive: ทำนายว่าเป็น แต่จริงๆ ไม่ได้เป็น
    fp = ((df['actual'] == 'Negative') & (df['predicted'] == 'Positive')).sum()
    # True Negative: ทำนายว่าไม่เป็น และจริงๆ ก็ไม่เป็น
    tn = ((df['actual'] == 'Negative') & (df['predicted'] == 'Negative')).sum() #&: ใช้ AND เพื่อเลือกแถวที่ ทั้ง actual และ predicted เป็น ‘Negative’
    # False Negative: ทำนายว่าไม่เป็น แต่จริงๆ เป็น
    fn = ((df['actual'] == 'Positive') & (df['predicted'] == 'Negative')).sum() #.sum(): บวก True ทั้งหมด (เพราะใน Pandas, True = 1, False = 0)
    
    return tp, fp, tn, fn #คืนค่าทั้งหมดออกมาเพื่อไปใช้คำนวณ metrics ต่อ

def calculate_metrics(tp, fp, tn, fn):
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
#ที่ต้องมี else 0 เพื่อป้องกันการเกิดการหารด้วย 0

    return pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Value': [accuracy, precision, recall, f1]
    }) # ใช้ pd.DataFrame เพื่อแสดง metrics อย่างเป็นระเบียบในรูปแบบตาราง

# เรียกใช้ฟังก์ชัน
tp, fp, tn, fn = get_confusion_matrix(df)
metrics_df = calculate_metrics(tp, fp, tn, fn)

# แสดงผล
print("Confusion Matrix:")
print(f"TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn}\n")
print(metrics_df)