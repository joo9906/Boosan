<template>
  <div class="p-4">
    <div class="flex gap-2 mb-4">
      <button @click="generateQuiz('number')" class="btn">숫자 퀴즈</button>
      <button @click="generateQuiz('word')" class="btn">단어 퀴즈</button>
      <button @click="generateQuiz('time')" class="btn">시간 퀴즈</button>
      <button @click="generateQuiz('memory')" class="btn">기억 퀴즈</button>
    </div>

    <div v-if="quiz" class="mt-4">
      <p><strong>문제:</strong> {{ quiz.question }}</p>
      <input v-model="userAnswer" class="border p-2 mt-2 w-full" placeholder="정답 입력" />
      <button @click="submit" class="bg-green-500 text-white mt-2 px-4 py-2 rounded">제출</button>
    </div>

    <div v-if="result !== null" class="mt-4 text-xl">
      {{ result ? '정답입니다! 🎉' : '틀렸어요 😢' }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { fetchQuiz, submitAnswer } from '@/api/quiz'

const quiz = ref(null)
const userAnswer = ref('')
const result = ref(null)

async function generateQuiz(type) {
  quiz.value = await fetchQuiz(type)
  userAnswer.value = ''
  result.value = null
}

async function submit() {
  const res = await submitAnswer(quiz.value.id, userAnswer.value)
  result.value = res.is_correct
}
</script>
