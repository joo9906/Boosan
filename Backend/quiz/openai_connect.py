# # quiz/openai_utils.py
# from dotenv import load_dotenv
# import openai, os
# from pathlib import Path

# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")

# quiz/openai_utils.py

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_quiz(quiz_type='number'):
    prompt_dict = {
        "number": """
고령자를 위한 숫자 기억 퀴즈를 만들어줘.  
예시:  
문제: 다음 숫자를 거꾸로 말하세요. 2, 5, 9  
정답: 9, 5, 2
""",
        "word": """
고령자를 위한 단어 기억 퀴즈를 만들어줘.  
예시:  
문제: 다음 단어를 외운 뒤, 가나다순으로 정렬하세요. 바나나, 사과, 토마토  
정답: 바나나, 사과, 토마토
""",
        "time": """
고령자를 위한 시간 감각 퀴즈를 만들어줘.  
예시:  
문제: 지금이 오후 3시라면, 2시간 30분 뒤는 몇 시인가요?  
정답: 오후 5시 30분
""",
        "memory": """
고령자를 위한 일상 기억력 퀴즈를 만들어줘.  
예시:  
문제: 아침에 한 일을 기억하고 3가지 말해보세요.  
정답: (개인에 따라 다름 — 예시: 양치, 아침 식사, 산책)
"""
    }

    prompt = prompt_dict.get(quiz_type, prompt_dict["number"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content
