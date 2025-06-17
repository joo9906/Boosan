# medical/utils.py
import os
import tempfile
from PIL import Image
import pytesseract
import cv2
import numpy as np

def extract_pill_info(image_path):
    """
    약봉투 이미지에서 정보를 추출하는 함수
    """
    try:
        # 이미지 읽기
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("이미지를 읽을 수 없습니다.")

        # 이미지 전처리
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # OCR 수행
        text = pytesseract.image_to_string(thresh, lang='kor+eng')
        
        # 텍스트에서 약 이름과 종류 추출
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else "알 수 없는 약"
        
        # 약 종류 판단
        pill_type = 'TAB'  # 기본값은 정제
        type_keywords = {
            'TAB': ['정제', '정'],
            'CAP': ['캡슐', '캡'],
            'SYR': ['시럽', '액'],
            'INJ': ['주사제', '주사'],
            'POW': ['가루약', '분말'],
            'GEL': ['겔제', '겔'],
        }
        
        for line in lines:
            for type_code, keywords in type_keywords.items():
                if any(keyword in line for keyword in keywords):
                    pill_type = type_code
                    break
            if pill_type != 'TAB':
                break
        
        return {
            'name': name,
            'type': pill_type
        }
    except Exception as e:
        print(f"Error in extract_pill_info: {str(e)}")
        return {
            'name': '알 수 없는 약',
            'type': 'TAB'
        }
    finally:
        # 임시 파일 삭제
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error deleting temporary file: {str(e)}")
