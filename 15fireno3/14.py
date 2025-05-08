import random

# 1. รับจำนวนครั้งทอย
N = int(input("Enter number of tosses N: ").strip())

# 2. จำลองทอยเหรียญ
results = []
for i in range(N):
    # สุ่ม 0 หรือ 1 แล้วแทน H/T
    if random.random() < 0.5:
        results.append('หัว')
    else:
        results.append('ก้อย')

# 3. แสดงตารางครั้งที่–ผลทอย
print(f"{'Trial':<6}{'Result'}")
for i, r in enumerate(results, start=1):
    print(f"{i:<6}{r}")

# 4. นับสถิติ
total_heads = results.count('หัว')
total_tails = results.count('ก้อย')

# หาช่วงหัวต่อเนื่องยาวที่สุด
max_consec = 0
current = 0
for r in results:
    if r == 'หัว':
        current += 1
        if current > max_consec:
            max_consec = current
    else:
        current = 0  # เจอก้อย → เซ็ตนับใหม่


# แสดงผลสรุป
print(f"\n หัว: {total_heads}")
print(f"ก้อย: {total_tails}")
print(f"หัวที่ต่อเนื่องยาวที่สุด : {max_consec}")