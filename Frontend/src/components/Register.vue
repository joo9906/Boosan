<template>
  <div class="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">회원가입</h2>
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div class="space-y-2">
        <label for="user_id" class="block text-sm font-medium text-gray-700">아이디</label>
        <input
          type="text"
          id="user_id"
          v-model="formData.user_id"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="password" class="block text-sm font-medium text-gray-700">비밀번호</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="password2" class="block text-sm font-medium text-gray-700">비밀번호 확인</label>
        <input
          type="password"
          id="password2"
          v-model="formData.password2"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="name" class="block text-sm font-medium text-gray-700">이름</label>
        <input
          type="text"
          id="name"
          v-model="formData.name"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="birth_date" class="block text-sm font-medium text-gray-700">생년월일</label>
        <input
          type="date"
          id="birth_date"
          v-model="formData.birth_date"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="gender" class="block text-sm font-medium text-gray-700">성별</label>
        <select
          id="gender"
          v-model="formData.gender"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        >
          <option value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <div class="space-y-2">
        <label for="phone_number" class="block text-sm font-medium text-gray-700">전화번호</label>
        <input
          type="tel"
          id="phone_number"
          v-model="formData.phone_number"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="space-y-2">
        <label for="address" class="block text-sm font-medium text-gray-700">주소</label>
        <input
          type="text"
          id="address"
          v-model="formData.address"
          required
          class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
        />
      </div>

      <div class="flex items-center space-x-2">
        <input
          type="checkbox"
          id="is_guardian"
          v-model="formData.is_guardian"
          class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
        />
        <label for="is_guardian" class="text-sm text-gray-700">보호자로 가입하기</label>
      </div>

      <button
        type="submit"
        class="w-full bg-emerald-600 text-white py-3 px-4 rounded-md hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition-colors"
      >
        가입하기
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      formData: {
        user_id: '',
        password: '',
        password2: '',
        name: '',
        birth_date: '',
        gender: '',
        phone_number: '',
        address: '',
        is_guardian: false,
        guardian_for: '',
      },
    }
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/account/signup/',
          this.formData
        )
        if (response.status === 201) {
          alert('회원가입이 완료되었습니다.')
          this.$router.push('/login')
        }
      } catch (error) {
        if (error.response) {
          alert(error.response.data.message || '회원가입 중 오류가 발생했습니다.')
        } else {
          alert('서버와의 통신 중 오류가 발생했습니다.')
        }
      }
    },
  },
}
</script>

<style scoped>
.register-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: left;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
}

.form-control {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-control:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.submit-btn {
  background-color: #42b983;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #3aa876;
}

@media (max-width: 768px) {
  .register-container {
    margin: 1rem;
    padding: 1rem;
  }
}
</style>
