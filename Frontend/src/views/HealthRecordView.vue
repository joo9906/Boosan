<template>
  <div class="health-record-container">
    <div class="max-w-4xl mx-auto p-6">
      <h1 class="text-3xl font-bold text-gray-800 mb-8">건강 기록 관리</h1>
      
      <!-- 건강 기록 입력 폼 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">오늘의 건강 기록</h2>
        
        <form @submit.prevent="submitHealthRecord" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- 수축기 혈압 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                수축기 혈압 (mmHg)
              </label>
              <input
                v-model="formData.systolic"
                type="number"
                min="60"
                max="200"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="예: 120"
              />
            </div>
            
            <!-- 이완기 혈압 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                이완기 혈압 (mmHg)
              </label>
              <input
                v-model="formData.diastolic"
                type="number"
                min="40"
                max="120"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="예: 80"
              />
            </div>
            
            <!-- 혈당 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                혈당 (mg/dL)
              </label>
              <input
                v-model="formData.glucose"
                type="number"
                min="30"
                max="500"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="예: 100"
              />
            </div>
          </div>
          
          <!-- 메모 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              메모 (선택사항)
            </label>
            <textarea
              v-model="formData.notes"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="오늘의 건강 상태나 특이사항을 기록해주세요..."
            ></textarea>
          </div>
          
          <!-- 제출 버튼 -->
          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="isLoading"
              class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-6 rounded-md transition duration-200"
            >
              {{ isLoading ? '처리 중...' : '기록 저장 및 추천 받기' }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- 건강 기록 목록 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">최근 건강 기록</h2>
        
        <div v-if="healthRecords.length === 0" class="text-gray-500 text-center py-8">
          아직 기록된 건강 데이터가 없습니다.
        </div>
        
        <div v-else class="space-y-3">
          <div
            v-for="record in healthRecords"
            :key="record.id"
            class="border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
          >
            <div class="flex justify-between items-start">
              <div>
                <div class="flex space-x-4 text-sm text-gray-600">
                  <span>혈압: {{ record.blood_pressure }}</span>
                  <span>혈당: {{ record.blood_sugar }} mg/dL</span>
                </div>
                <div class="text-xs text-gray-500 mt-1">
                  {{ record.record_date }}
                </div>
                <div v-if="record.notes" class="text-sm text-gray-700 mt-2">
                  {{ record.notes }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- AI 추천 팝업 -->
    <div
      v-if="showRecommendationPopup"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click="closePopup"
    >
      <div
        class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6"
        @click.stop
      >
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-gray-800">AI 건강 추천</h3>
          <button
            @click="closePopup"
            class="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>
        
        <div v-if="recommendation" class="space-y-4">
          <!-- 혈압/혈당 상태 -->
          <div class="bg-blue-50 rounded-lg p-4">
            <div class="text-sm text-blue-800">
              <div>혈압 상태: {{ recommendation.혈압_상태 }}</div>
              <div>혈당 상태: {{ recommendation.혈당_상태 }}</div>
            </div>
          </div>
          
          <!-- 운동 추천 -->
          <div class="bg-green-50 rounded-lg p-4">
            <h4 class="font-semibold text-green-800 mb-2">🏃‍♂️ 운동 추천</h4>
            <p class="text-green-700">{{ recommendation.추천_운동 }}</p>
          </div>
          
          <!-- 식단 추천 -->
          <div class="bg-orange-50 rounded-lg p-4">
            <h4 class="font-semibold text-orange-800 mb-2">🍽️ 식단 추천</h4>
            <p class="text-orange-700">{{ recommendation.추천_식단 }}</p>
          </div>
        </div>
        
        <div class="mt-6 flex justify-end">
          <button
            @click="closePopup"
            class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
          >
            확인
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HealthRecordView',
  data() {
    return {
      formData: {
        systolic: '',
        diastolic: '',
        glucose: '',
        notes: ''
      },
      healthRecords: [],
      recommendation: null,
      showRecommendationPopup: false,
      isLoading: false
    }
  },
  
  async mounted() {
    await this.loadHealthRecords()
  },
  
  methods: {
    async submitHealthRecord() {
      this.isLoading = true
      
      try {
        const response = await axios.post('/health/save-record/', this.formData, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response.data.success) {
          // 추천 결과 저장
          this.recommendation = response.data.data.recommendation
          
          // 폼 초기화
          this.formData = {
            systolic: '',
            diastolic: '',
            glucose: '',
            notes: ''
          }
          
          // 팝업 표시
          this.showRecommendationPopup = true
          
          // 건강 기록 목록 새로고침
          await this.loadHealthRecords()
          
          // 성공 메시지
          alert('건강 기록이 저장되었습니다!')
        }
      } catch (error) {
        console.error('Error submitting health record:', error)
        const errorMessage = error.response?.data?.error || '건강 기록 저장 중 오류가 발생했습니다.'
        alert(errorMessage)
      } finally {
        this.isLoading = false
      }
    },
    
    async loadHealthRecords() {
      try {
        const response = await axios.get('/health/records/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        
        if (response.data.success) {
          this.healthRecords = response.data.data
        }
      } catch (error) {
        console.error('Error loading health records:', error)
      }
    },
    
    closePopup() {
      this.showRecommendationPopup = false
      this.recommendation = null
    }
  }
}
</script>

<style scoped>
.health-record-container {
  min-height: 100vh;
  background-color: #f8fafc;
}
</style> 