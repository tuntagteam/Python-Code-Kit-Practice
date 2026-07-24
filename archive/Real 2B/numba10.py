import pandas as pd  # ใช้สำหรับการจัดการข้อมูลตาราง เช่น groupby, merge, pivot

# ข้อมูลการให้คะแนนหนังสือของผู้ใช้แต่ละคน
df = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3],
    'book_id': ['B01', 'B02', 'B01', 'B03', 'B01', 'B02'],
    'rating': [5, 4, 3, 5, 4, 2]
})
# DataFrame นี้จำลองว่า user 1 ให้คะแนน B01 = 5, B02 = 4 เป็นต้น
# เราจะใช้วิเคราะห์ว่าเล่มไหนโดนใจที่สุด, ใครขัดแย้งกับคนอื่น และสร้าง pivot

# คำนวณค่าเฉลี่ยของคะแนนแต่ละเล่ม
book_avg = df.groupby('book_id')['rating'].mean()
# groupby(): จับกลุ่มตาม book_id
# ['rating'].mean(): หาค่าเฉลี่ยของคอลัมน์ rating ในแต่ละกลุ่ม

# หาหนังสือที่คะแนนเฉลี่ยสูงสุด
top_book_id = book_avg.idxmax()   # คืน book_id ที่ค่าเฉลี่ยสูงสุด
top_book_score = book_avg.max()   # คะแนนเฉลี่ยสูงสุด

print(f"หนังสือที่ได้คะแนนเฉลี่ยสูงสุดคือ: {top_book_id} ({top_book_score:.1f} คะแนน)")

# รวมคะแนนเฉลี่ยของหนังสือไปกับข้อมูลเดิม (ด้วย merge)
df_with_avg = df.merge(book_avg.rename('avg_rating'), on='book_id')
# book_avg เป็น Series ต้อง rename() ให้กลายเป็นคอลัมน์ 'avg_rating'
# merge(): รวมข้อมูล rating ของผู้ใช้ และค่าเฉลี่ยของหนังสือที่เค้าให้ไว้

# สร้างคอลัมน์ deviation เพื่อดูว่าแต่ละคนเบี่ยงเบนจากค่าเฉลี่ยเท่าไร
df_with_avg['deviation'] = abs(df_with_avg['rating'] - df_with_avg['avg_rating'])
# abs(): เอาค่าที่ไม่ติดลบ → deviation = ความต่างแน่นอน

# รวมค่า deviation ต่อ user เพื่อดูว่าใครขัดแย้งกับค่าเฉลี่ยรวมมากสุด
user_deviation = df_with_avg.groupby('user_id')['deviation'].sum()

most_conflicted_user = user_deviation.idxmax()
most_conflicted_score = user_deviation.max()

print(f"ผู้ใช้ที่ให้คะแนนขัดแย้งกับค่าเฉลี่ยมากที่สุดคือ: user_id {most_conflicted_user} (รวมเบี่ยงเบน {most_conflicted_score:.2f})")

# Pivot Table แสดงผู้ใช้แต่ละคนให้คะแนนแต่ละเล่มเท่าไหร่
pivot = df.pivot_table(index='user_id', columns='book_id', values='rating')
# index = user_id: แถวคือผู้ใช้
# columns = book_id: คอลัมน์คือหนังสือ
# values = rating: ค่าในตารางคือคะแนน

print("Pivot Table:")
print(pivot.fillna("-"))  # ใช้ .fillna("-") เพื่อดูว่าใครไม่ได้ให้คะแนนเล่มไหน