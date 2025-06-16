import axios from 'axios'

const API_URL = 'http://localhost:8000' // Django 서버 주소

export async function fetchQuiz(type = 'number') {
  const res = await axios.get(`${API_URL}/quiz/create/`, {
    params: { type },
  })
  return res.data
}

export async function submitAnswer(quizId, userAnswer) {
  const res = await axios.post(`${API_URL}/quiz/${quizId}/submit/`, {
    user_answer: userAnswer,
  })
  return res.data
}
