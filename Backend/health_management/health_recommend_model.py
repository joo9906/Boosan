import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import random

class HealthRecommendModel:
    def __init__(self):
        self.le_bp = LabelEncoder()
        self.le_glucose = LabelEncoder()
        self.le_exercise = LabelEncoder()
        self.le_diet = LabelEncoder()
        self.ex_model = None
        self.di_model = None
        self.is_trained = False
        
        # 혈압 단계별 기준 (수축기/이완기)
        self.bp_levels = {
            '저혈압': {'systolic': (0, 89), 'diastolic': (0, 59)},
            '정상': {'systolic': (90, 119), 'diastolic': (60, 79)},
            '주의혈압': {'systolic': (120, 129), 'diastolic': (0, 79)},
            '고혈압전단계': {'systolic': (130, 139), 'diastolic': (80, 89)},
            '고혈압': {'systolic': (140, 300), 'diastolic': (90, 200)}
        }
        
        # 혈당 단계별 기준 (mg/dL)
        self.glucose_levels = {
            '위험저혈당': {'min': 0, 'max': 53},
            '저혈당': {'min': 54, 'max': 69},
            '정상': {'min': 70, 'max': 100},
            '고혈당전단계': {'min': 101, 'max': 125},
            '당뇨진단기준': {'min': 126, 'max': 179},
            '심한고혈당': {'min': 180, 'max': 500}
        }
        
        # 혈압별 운동 추천
        self.bp_exercise = {
            '저혈압': [
                '느린 산책 10-15분씩 여러 번',
                '의자 체조·고무밴드',
                '가벼운 스트레칭',
                '천천히 걷기'
            ],
            '정상': [
                '편안한 걷기 30분 주 5일',
                '밴드 근력 2회',
                '가벼운 조깅',
                '자전거 타기'
            ],
            '주의혈압': [
                '실내 자전거 20-30분',
                '따뜻한 물속 체조 주 2회',
                '천천히 걷기',
                '스트레칭'
            ],
            '고혈압전단계': [
                '속도 바꿔 걷기 30분×5일',
                '천천히 요가',
                '수영',
                '가벼운 근력운동'
            ],
            '고혈압': [
                '수영장 물속 걷기 30분×5일',
                '1-2kg 아령 10회×2세트',
                '천천히 걷기',
                '스트레칭'
            ]
        }
        
        # 혈압별 식단 추천
        self.bp_diet = {
            '저혈압': [
                '수분 넉넉히 마시기',
                '된장국·멸치국 등 약간 짭짤하게',
                '세끼 챙겨 드시기',
                '소금 간을 조금 더 하기'
            ],
            '정상': [
                '저염·채소 듬뿍 식단',
                '채소·과일 4-5번',
                '현미·잡곡밥 3공기',
                '저지방 우유·요거트 2번'
            ],
            '주의혈압': [
                '소금 더 줄이기(≤4g/일)',
                '가공 햄·김치 국물 절제',
                '채소 중심 식단',
                '저염 식단'
            ],
            '고혈압전단계': [
                '채소·과일 6번',
                '올리브유 1큰술/일',
                '생선 2회/주',
                '체중 3% 줄이기'
            ],
            '고혈압': [
                '채소·과일 6번 이상',
                '올리브유 2큰술/일',
                '붉은 고기 월 2회만',
                '소금 ≤3g/일'
            ]
        }
        
        # 혈당별 운동 추천
        self.glucose_exercise = {
            '위험저혈당': [
                '운동 중단',
                '사탕 3개·주스 ½컵 먼저',
                '휴식 취하기',
                '단맛 음식 섭취'
            ],
            '저혈당': [
                '회복 후 느린 스트레칭',
                '산책 10-15분',
                '가벼운 운동',
                '천천히 걷기'
            ],
            '정상': [
                '속보 30분×5일',
                '밴드 근력 2회',
                '조깅',
                '자전거 타기'
            ],
            '고혈당전단계': [
                '따뜻한 물속 체조 40분×4일',
                '벽 짚고 스쿼트',
                '천천히 걷기',
                '스트레칭'
            ],
            '당뇨진단기준': [
                '천천히 산책 30분×5일',
                '밴드 근력 3회',
                '가벼운 운동',
                '수영'
            ],
            '심한고혈당': [
                '집 안 걷기 10분×2',
                '가벼운 스트레칭',
                '휴식',
                '천천히 걷기'
            ]
        }
        
        # 혈당별 식단 추천
        self.glucose_diet = {
            '위험저혈당': [
                '단맛 음식 즉시',
                '통밀빵 ½ + 치즈',
                '주스나 사탕',
                '꿀 한 스푼'
            ],
            '저혈당': [
                '규칙 3끼 + 과일·견과 간식',
                '통곡물 빵',
                '과일 섭취',
                '견과류 간식'
            ],
            '정상': [
                '현미밥, 생선, 두부',
                '단 음료·과자 줄이기',
                '균형잡힌 식단',
                '채소 중심'
            ],
            '고혈당전단계': [
                '채소·과일 5번',
                '콩·견과 자주',
                '현미죽 저녁 소식',
                '저탄수화물 식단'
            ],
            '당뇨진단기준': [
                '밥 양 줄이고 채소·단백질 늘리기',
                '설탕·과일즙 제한',
                '저탄수화물 식단',
                '단백질 중심'
            ],
            '심한고혈당': [
                '맑은 야채국',
                '통곡물 죽',
                '물 2L',
                '소금 조심'
            ]
        }
    
    def get_bp_level(self, systolic, diastolic):
        """수축기/이완기 혈압으로 혈압 단계 판정"""
        for level, ranges in self.bp_levels.items():
            if (ranges['systolic'][0] <= systolic <= ranges['systolic'][1] and
                ranges['diastolic'][0] <= diastolic <= ranges['diastolic'][1]):
                return level
        return '정상'  # 기본값
    
    def get_glucose_level(self, glucose):
        """혈당 수치로 혈당 단계 판정"""
        for level, ranges in self.glucose_levels.items():
            if ranges['min'] <= glucose <= ranges['max']:
                return level
        return '정상'  # 기본값
    
    def create_dummy_data(self):
        """더미 데이터 생성"""
        random.seed(42)
        n_samples = 2000
        
        data = []
        
        # 혈압 범위별 샘플 생성
        bp_ranges = [
            (60, 89, 40, 59, '저혈압'),      # 저혈압
            (90, 119, 60, 79, '정상'),       # 정상
            (120, 129, 60, 79, '주의혈압'),   # 주의혈압
            (130, 139, 80, 89, '고혈압전단계'), # 고혈압전단계
            (140, 180, 90, 120, '고혈압')     # 고혈압
        ]
        
        # 혈당 범위별 샘플 생성
        glucose_ranges = [
            (30, 53, '위험저혈당'),
            (54, 69, '저혈당'),
            (70, 100, '정상'),
            (101, 125, '고혈당전단계'),
            (126, 179, '당뇨진단기준'),
            (180, 300, '심한고혈당')
        ]
        
        for _ in range(n_samples):
            # 혈압 랜덤 생성
            bp_range = random.choices(bp_ranges, weights=[0.1, 0.4, 0.2, 0.2, 0.1])[0]
            systolic = random.randint(bp_range[0], bp_range[1])
            diastolic = random.randint(bp_range[2], bp_range[3])
            bp_level = bp_range[4]
            
            # 혈당 랜덤 생성
            glucose_range = random.choices(glucose_ranges, weights=[0.05, 0.1, 0.4, 0.25, 0.15, 0.05])[0]
            glucose = random.randint(glucose_range[0], glucose_range[1])
            glucose_level = glucose_range[2]
            
            # 혈압과 혈당에 따른 운동/식단 추천 로직
            if bp_level == '저혈압':
                exercise = random.choice(self.bp_exercise['저혈압'])
                diet = random.choice(self.bp_diet['저혈압'])
            elif bp_level == '정상' and glucose_level in ['정상', '저혈당']:
                exercise = random.choice(self.bp_exercise['정상'])
                diet = random.choice(self.bp_diet['정상'])
            elif glucose_level in ['고혈당전단계', '당뇨진단기준', '심한고혈당']:
                exercise = random.choice(self.glucose_exercise[glucose_level])
                diet = random.choice(self.glucose_diet[glucose_level])
            elif bp_level in ['주의혈압', '고혈압전단계', '고혈압']:
                exercise = random.choice(self.bp_exercise[bp_level])
                diet = random.choice(self.bp_diet[bp_level])
            else:
                exercise = random.choice(self.bp_exercise['정상'])
                diet = random.choice(self.bp_diet['정상'])
            
            data.append({
                'systolic': systolic,
                'diastolic': diastolic,
                'glucose': glucose,
                'bp_level': bp_level,
                'glucose_level': glucose_level,
                'exercise_label': exercise,
                'diet_label': diet
            })
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """모델 학습"""
        print("더미 데이터 생성 중...")
        df = self.create_dummy_data()
        print(f"생성된 데이터: {len(df)}개 샘플")
        
        # 인코딩
        df['bp_level_enc'] = self.le_bp.fit_transform(df['bp_level'])
        df['glucose_level_enc'] = self.le_glucose.fit_transform(df['glucose_level'])
        df['exercise_label_enc'] = self.le_exercise.fit_transform(df['exercise_label'])
        df['diet_label_enc'] = self.le_diet.fit_transform(df['diet_label'])
        
        # 입력, 정답 분리
        X = df[['bp_level_enc', 'glucose_level_enc']]
        y_exercise = df['exercise_label_enc']
        y_diet = df['diet_label_enc']
        
        # 학습/평가 분할
        X_train, X_test, y_ex_train, y_ex_test = train_test_split(X, y_exercise, test_size=0.2, random_state=42)
        _, _, y_di_train, y_di_test = train_test_split(X, y_diet, test_size=0.2, random_state=42)
        
        # 모델 학습
        self.ex_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.ex_model.fit(X_train, y_ex_train)
        
        self.di_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.di_model.fit(X_train, y_di_train)
        
        self.is_trained = True
        
        # 모델 성능 평가
        ex_score = self.ex_model.score(X_test, y_ex_test)
        di_score = self.di_model.score(X_test, y_di_test)
        
        return {
            'exercise_accuracy': ex_score,
            'diet_accuracy': di_score,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def recommend_by_levels(self, bp_level, glucose_level):
        """혈압/혈당 단계로 추천"""
        if not self.is_trained:
            self.train_model()
        
        try:
            # 인코딩
            bp_enc = self.le_bp.transform([bp_level])[0]
            gl_enc = self.le_glucose.transform([glucose_level])[0]
            X_input = [[bp_enc, gl_enc]]
            
            # 예측
            ex_pred = self.ex_model.predict(X_input)[0]
            di_pred = self.di_model.predict(X_input)[0]
            
            # 디코딩
            ex_label = self.le_exercise.inverse_transform([ex_pred])[0]
            di_label = self.le_diet.inverse_transform([di_pred])[0]
            
            # 랜덤하게 하나씩 선택
            if bp_level == '저혈압':
                exercise = random.choice(self.bp_exercise['저혈압'])
                diet = random.choice(self.bp_diet['저혈압'])
            elif bp_level == '정상' and glucose_level in ['정상', '저혈당']:
                exercise = random.choice(self.bp_exercise['정상'])
                diet = random.choice(self.bp_diet['정상'])
            elif glucose_level in ['고혈당전단계', '당뇨진단기준', '심한고혈당']:
                exercise = random.choice(self.glucose_exercise[glucose_level])
                diet = random.choice(self.glucose_diet[glucose_level])
            elif bp_level in ['주의혈압', '고혈압전단계', '고혈압']:
                exercise = random.choice(self.bp_exercise[bp_level])
                diet = random.choice(self.bp_diet[bp_level])
            else:
                exercise = random.choice(self.bp_exercise['정상'])
                diet = random.choice(self.bp_diet['정상'])
            
            return {
                "추천_운동": f"'{exercise}'의 운동을 추천해요!",
                "추천_식단": f"'{diet}' 드시기를 추천드려요!!",
                "혈압_상태": bp_level,
                "혈당_상태": glucose_level
            }
        except Exception as e:
            return {
                "error": f"추천 생성 중 오류 발생: {str(e)}",
                "혈압_상태": bp_level,
                "혈당_상태": glucose_level
            }
    
    def recommend_by_values(self, systolic, diastolic, glucose):
        """실제 혈압/혈당 수치로 추천"""
        bp_level = self.get_bp_level(systolic, diastolic)
        glucose_level = self.get_glucose_level(glucose)
        
        return self.recommend_by_levels(bp_level, glucose_level)

# 전역 모델 인스턴스
health_model = HealthRecommendModel()

def get_health_recommendation_by_levels(bp_level, glucose_level):
    """혈압/혈당 단계로 건강 추천"""
    return health_model.recommend_by_levels(bp_level, glucose_level)

def get_health_recommendation_by_values(systolic, diastolic, glucose):
    """실제 혈압/혈당 수치로 건강 추천"""
    return health_model.recommend_by_values(systolic, diastolic, glucose)

def train_health_model():
    """모델 재학습"""
    return health_model.train_model()

# 테스트 실행 코드 추가
if __name__ == "__main__":
    print("=== 건강 추천 AI 모델 테스트 ===\n")
    
    # 1. 모델 학습
    print("1. 모델 학습 중...")
    training_result = train_health_model()
    print(f"학습 완료!")
    print(f"운동 모델 정확도: {training_result['exercise_accuracy']:.3f}")
    print(f"식단 모델 정확도: {training_result['diet_accuracy']:.3f}")
    print(f"학습 샘플 수: {training_result['training_samples']}")
    print(f"테스트 샘플 수: {training_result['test_samples']}\n")
    
    # 2. 추천 테스트
    print("2. 추천 테스트:")
    test_cases = [
        ("저혈압", "정상"),
        ("정상", "고혈당전단계"),
        ("고혈압", "심한고혈당"),
    ]
    
    for i, (bp, glucose) in enumerate(test_cases, 1):
        print(f"\n테스트 {i}: 혈압={bp}, 혈당={glucose}")
        result = get_health_recommendation_by_levels(bp, glucose)
        
        if 'error' in result:
            print(f"오류: {result['error']}")
        else:
            print(f"추천 운동: {result['추천_운동']}")
            print(f"추천 식단: {result['추천_식단']}")
    
    print("\n=== 테스트 완료 ===") 