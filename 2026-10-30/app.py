import json
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, render_template, request, session
from google import genai

# 讀取與 app.py 同一個資料夾的 .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
# 產生一組隨機密鑰，用來保護 Flask 的 Session 資料
app.secret_key = secrets.token_hex(16)

TOPICS = ["輸入輸出", "條件判斷", "迴圈", "串列"]


def generate_question(topic):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=(
            f"請根據「{topic}」產生一道 Python 初學者的四選一選擇題。"
            "只能有一個正確答案。"
            "請回傳 JSON 格式，包含 question、A、B、C、D、answer、explanation 七個欄位。"
            "answer 只能填入 A、B、C 或 D。"
            "explanation 請用繁體中文解釋正確答案，50字以內。"
        ),
        config={"response_mime_type": "application/json"},
    )
    # 將 Gemini 回傳的 JSON 文字轉成 Python 字典
    return json.loads(response.text)


@app.route("/", methods=["GET", "POST"])
def home():
    topic = ""
    feedback = ""
    explanation = ""
    student_answer = ""
    question_data = session.get("question_data")

    if request.method == "POST":
        topic = request.form.get("topic", "")
        action = request.form.get("action", "")
        print("我選擇的主題:", topic)

        # 按下「幫我出題」：呼叫 Gemini 產生新題目
        if action == "generate":
            if not topic:
                feedback = "請先選擇學習主題！"
            else:
                try:
                    question_data = generate_question(topic)
                    session["question_data"] = question_data
                except Exception as e:
                    print("Gemini API 錯誤:", e)
                    question_data = None
                    session.pop("question_data", None)
                    feedback = f"AI 出題失敗：{e}"

        # 按下「提交答案」：比對 AI 提供的正確答案
        if action == "check" and question_data:
            student_answer = request.form.get("student_answer", "")
            if student_answer == "":
                feedback = "請先選擇一個答案！"
            elif student_answer == question_data["answer"]:
                feedback = "答對了！"
                explanation = question_data["explanation"]
            else:
                feedback = f"答錯了！正確答案是 {question_data['answer']}。"
                explanation = question_data["explanation"]
    else:
        # 重新開啟網頁時清掉舊題目
        session.pop("question_data", None)
        question_data = None

    return render_template(
        "index.html",
        topics=TOPICS,
        topic=topic,
        question_data=question_data,
        student_answer=student_answer,
        feedback=feedback,
        explanation=explanation,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
