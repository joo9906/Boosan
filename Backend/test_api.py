#!/usr/bin/env python3
"""
건강 기록 API 테스트 스크립트
"""

import requests
import json

# Django 서버 URL (기본 포트 8000)
BASE_URL = "http://localhost:8000"

def test_health_recommendation_options():
    """건강 추천 옵션 API 테스트"""
    print("=== 건강 추천 옵션 API 테스트 ===")
    
    try:
        response = requests.get(f"{BASE_URL}/health/options/")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API 호출 성공!")
            print(f"혈압 레벨: {data['bp_levels']}")
            print(f"혈당 레벨: {data['glucose_levels']}")
            print("설명:", json.dumps(data['description'], indent=2, ensure_ascii=False))
        else:
            print(f"❌ API 호출 실패: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Django 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_health_record_save():
    """건강 기록 저장 API 테스트 (인증 없이)"""
    print("\n=== 건강 기록 저장 API 테스트 (인증 없이) ===")
    
    test_data = {
        "systolic": 120,
        "diastolic": 80,
        "glucose": 100,
        "notes": "테스트 기록입니다."
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/health/save-record/",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 401:
            print("✅ 예상된 결과: 인증이 필요합니다 (401)")
            print("이는 정상적인 동작입니다. 실제 사용시에는 로그인 후 토큰을 사용해야 합니다.")
        else:
            print(f"❌ 예상과 다른 응답: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Django 서버에 연결할 수 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_ai_model_direct():
    """AI 모델 직접 테스트"""
    print("\n=== AI 모델 직접 테스트 ===")
    
    try:
        # health_management 앱의 AI 모델 직접 테스트
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'health_management'))
        
        from health_recommend_model import get_health_recommendation_by_values
        
        # 테스트 케이스들
        test_cases = [
            (120, 80, 100),  # 정상
            (140, 90, 120),  # 고혈압 + 고혈당
            (90, 60, 70),    # 저혈압 + 정상혈당
        ]
        
        for systolic, diastolic, glucose in test_cases:
            print(f"\n테스트: 혈압 {systolic}/{diastolic}, 혈당 {glucose}")
            result = get_health_recommendation_by_values(systolic, diastolic, glucose)
            
            if 'error' not in result:
                print(f"✅ 혈압 상태: {result['혈압_상태']}")
                print(f"✅ 혈당 상태: {result['혈당_상태']}")
                print(f"✅ 운동 추천: {result['추천_운동']}")
                print(f"✅ 식단 추천: {result['추천_식단']}")
            else:
                print(f"❌ 오류: {result['error']}")
                
    except ImportError as e:
        print(f"❌ 모듈 import 오류: {e}")
    except Exception as e:
        print(f"❌ AI 모델 테스트 오류: {e}")

if __name__ == "__main__":
    print("건강 기록 API 테스트를 시작합니다...\n")
    
    # 1. AI 모델 직접 테스트
    test_ai_model_direct()
    
    # 2. API 엔드포인트 테스트
    test_health_recommendation_options()
    test_health_record_save()
    
    print("\n=== 테스트 완료 ===")
    print("\n웹 브라우저에서 다음 URL들을 확인해보세요:")
    print(f"1. 프론트엔드: http://localhost:5173/health-record")
    print(f"2. API 옵션: {BASE_URL}/health/options/")
    print("\n참고: 실제 건강 기록 저장은 로그인이 필요합니다.") 