from flask import Flask, render_template, request

app = Flask(__name__)

# 每個學習主題的固定題目：題目文字、選項、正確答案
QUESTIONS = {
    "輸入輸出": {
        "text": "Python 使用哪個函式顯示文字？",
        "options": {"A": "input()", "B": "print()", "C": "len()", "D": "range()"},
        "answer": "B",
    },
    "條件判斷": {
        "text": "Python 中，條件不成立時要執行的區塊使用哪個關鍵字？",
        "options": {"A": "if", "B": "for", "C": "else", "D": "def"},
        "answer": "C",
    },
    "迴圈": {
        "text": "range(3) 會產生哪些數字？",
        "options": {"A": "1, 2, 3", "B": "0, 1, 2", "C": "0, 1, 2, 3", "D": "3"},
        "answer": "B",
    },
    "串列": {
        "text": "nums = [10, 20, 30]，nums[1] 的值是多少？",
        "options": {"A": "10", "B": "20", "C": "30", "D": "1"},
        "answer": "B",
    },
}


@app.route("/", methods=["GET", "POST"])
def home():
    topic = ""
    question = None
    student_answer = ""
    feedback = ""

    if request.method == "POST":
        # 取得學生選擇的學習主題
        topic = request.form.get("topic", "")
        print("目前選擇的主題：", topic)

        # 根據主題決定要顯示的題目
        if topic in QUESTIONS:
            question = QUESTIONS[topic]

        # 判斷學生是否按下「提交答案」
        if request.form.get("action") == "check" and question:
            student_answer = request.form.get("student_answer", "")
            if student_answer == "":
                feedback = "請先選擇一個答案！"
            elif student_answer == question["answer"]:
                feedback = "答對了！"
            else:
                feedback = "答錯了！"

    return render_template(
        "index.html",
        topics=QUESTIONS.keys(),
        topic=topic,
        question=question,
        student_answer=student_answer,
        feedback=feedback,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
