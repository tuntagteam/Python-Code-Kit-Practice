import subprocess
import json
import sys
from pathlib import Path


def normalize(text):
    """
    ปรับ output ให้เทียบง่ายขึ้น
    - ตัดช่องว่างหัวท้าย
    - แปลง \r\n เป็น \n
    """
    return text.replace("\r\n", "\n").strip()


def run_test(submission_file, test_input, timeout=2):
    """
    รันไฟล์ Python ของเด็กด้วย input ที่กำหนด
    แล้วคืนค่า stdout, stderr, returncode
    """
    result = subprocess.run(
        [sys.executable, submission_file],
        input=test_input,
        text=True,
        capture_output=True,
        timeout=timeout
    )

    return result.stdout, result.stderr, result.returncode


def judge(submission_file, test_file):
    submission_path = Path(submission_file)
    test_path = Path(test_file)

    if not submission_path.exists():
        print(f"ไม่พบไฟล์คำตอบ: {submission_file}")
        return

    if not test_path.exists():
        print(f"ไม่พบไฟล์เทส: {test_file}")
        return

    with open(test_path, "r", encoding="utf-8") as f:
        tests = json.load(f)

    passed = 0

    print(f"ตรวจไฟล์: {submission_file}")
    print(f"จำนวนเทสทั้งหมด: {len(tests)}")
    print("-" * 50)

    for i, test in enumerate(tests, start=1):
        name = test.get("name", f"test {i}")
        test_input = test["input"]
        expected_output = test["output"]

        try:
            stdout, stderr, returncode = run_test(str(submission_path), test_input)

            actual = normalize(stdout)
            expected = normalize(expected_output)

            if returncode != 0:
                print(f"❌ Test {i}: {name}")
                print("Runtime Error")
                print(stderr.strip())
            elif actual == expected:
                print(f"✅ Test {i}: {name}")
                passed += 1
            else:
                print(f"❌ Test {i}: {name}")
                print("Input:")
                print(test_input, end="")
                print("Expected:")
                print(expected_output, end="")
                print("Actual:")
                print(stdout, end="")

        except subprocess.TimeoutExpired:
            print(f"⏰ Test {i}: {name}")
            print("Time Limit Exceeded")

        print("-" * 50)

    print(f"Result: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("🎉 Accepted")
    else:
        print("❌ Wrong Answer")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("วิธีใช้:")
        print("python judge.py submissions/student1_q2.py tests/q2_brackets.json")
    else:
        judge(sys.argv[1], sys.argv[2])