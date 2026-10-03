def valid_name(name):
    if len(name) < 3:
        return False

    for c in name:
        if not (('A' <= c <= 'Z') or ('a' <= c <= 'z')):
            return False

    return True


def calculate_score(score1, score2, score3, time):
    # หาผลรวมเอง ไม่ใช้ sum()
    final_score = score1 + score2 + score3

    # คะแนนทุกด่าน >= 80
    if score1 >= 80 and score2 >= 80 and score3 >= 80:
        final_score += 26

    # ได้ 100 คะแนน เพิ่มด่านละ 5
    if score1 == 100:
        final_score += 5

    if score2 == 100:
        final_score += 5

    if score3 == 100:
        final_score += 5

    # คะแนนทั้ง 3 ด่านเท่ากัน
    if score1 == score2 and score2 == score3:
        final_score += 10

    # ใช้เวลาน้อยกว่า 45 นาที
    if time < 45:
        final_score += 15

    # คะแนนสูงสุดไม่เกิน 300
    if final_score > 300:
        final_score = 300

    return final_score


def should_swap(a, b):
    # ถ้า a ควรอยู่หลัง b ให้ return True

    # 1. คะแนนมากกว่าอยู่ก่อน
    if a[4] < b[4]:
        return True

    if a[4] > b[4]:
        return False

    # 2. คะแนนเท่ากัน เวลาน้อยกว่าอยู่ก่อน
    if a[5] > b[5]:
        return True

    if a[5] < b[5]:
        return False

    # 3. คะแนนและเวลาเท่ากัน score3 มากกว่าอยู่ก่อน
    if a[3] < b[3]:
        return True

    if a[3] > b[3]:
        return False

    # 4. ทุกอย่างเท่ากัน เรียงชื่อตาม A-Z
    if a[0] > b[0]:
        return True

    return False


# =========================
# Main Program
# =========================

n = int(input())

adventurers = []
invalid_count = 0

for i in range(n):

    name = input()
    age = int(input())
    score1 = int(input())
    score2 = int(input())
    score3 = int(input())
    time = float(input())

    # ตรวจสอบข้อมูล
    valid = True

    if not valid_name(name):
        valid = False

    if age < 12 or age > 60:
        valid = False

    if score1 < 6 or score1 > 100:
        valid = False

    if score2 < 6 or score2 > 100:
        valid = False

    if score3 < 6 or score3 > 100:
        valid = False

    if time <= 0:
        valid = False

    # ถ้าข้อมูลผิด
    if not valid:
        invalid_count += 1
        continue

    # คำนวณคะแนน
    final_score = calculate_score(
        score1,
        score2,
        score3,
        time
    )

    # index
    # 0 = name
    # 1 = score1
    # 2 = score2
    # 3 = score3
    # 4 = final_score
    # 5 = time

    adventurers.append([
        name,
        score1,
        score2,
        score3,
        final_score,
        time
    ])


# =========================
# ไม่มีผู้สมัครที่ valid
# =========================

if len(adventurers) == 0:
    print("No valid adventurers")
    print("Invalid:", invalid_count)

else:

    # =========================
    # Bubble Sort
    # =========================

    size = len(adventurers)

    for i in range(size - 1):

        for j in range(size - 1 - i):

            if should_swap(adventurers[j], adventurers[j + 1]):

                temp = adventurers[j]
                adventurers[j] = adventurers[j + 1]
                adventurers[j + 1] = temp

    # =========================
    # แสดงอันดับ
    # =========================

    total_score = 0

    for i in range(len(adventurers)):

        name = adventurers[i][0]
        final_score = adventurers[i][4]
        time = adventurers[i][5]

        total_score += final_score

        print(
            i + 1,
            name,
            final_score,
            time
        )

    # =========================
    # ผู้ชนะ
    # =========================

    winner = adventurers[0][0]

    print("Winner:", winner)

    # =========================
    # ค่าเฉลี่ย
    # =========================

    average = total_score / len(adventurers)

    print("Average: %.2f" % average)

    # =========================
    # จำนวนข้อมูลผิด
    # =========================

    print("Invalid:", invalid_count)