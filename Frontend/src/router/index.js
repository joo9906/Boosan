import { createRouter, createWebHistory } from 'vue-router'
import WelfareCenterList from '../components/WelfareCenterList.vue'
import HospitalList from '../components/HospitalList.vue'
import Register from '../components/Register.vue'
import Quiz from '../views/quizView.vue'
import Pillupload from '../components/Pillupload.vue'
import HealthRecordView from '../views/HealthRecordView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: WelfareCenterList,
  },
  {
    path: '/welfare-centers',
    name: 'welfare-centers',
    component: WelfareCenterList,
  },
  {
    path: '/hospitals',
    name: 'hospitals',
    component: HospitalList,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/health-record',
    name: 'health-record',
    component: HealthRecordView,
  },
  {
    path: '/quiz',
    name: 'quiz',
    component: Quiz,
  },
  {
    path: '/pill-upload',
    name: 'pill-upload',
    component: Pillupload,
    // compoent: () => import('../components/Quiz.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
