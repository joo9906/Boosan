import axios from 'axios'

const API_URL = 'http://localhost:8000' // Django 서버 주소

export async function fetchQuiz(type = 'number') {
  try {
    const res = await axios.get(`${API_URL}/medical/quiz/create/`, {
      params: { type },
    })
    return res.data
  } catch (error) {
    console.error('퀴즈 생성 중 오류:', error)
    throw error
  }
}

export async function submitAnswer(quizId, userAnswer) {
  try {
    const res = await axios.post(`${API_URL}/medical/quiz/${quizId}/submit/`, {
      user_answer: userAnswer,
    })
    return res.data
  } catch (error) {
    console.error('답변 제출 중 오류:', error)
    throw error
  }
}
