import { createRouter, createWebHistory } from 'vue-router'
import WelfareCenterList from '../components/WelfareCenterList.vue'
import HospitalList from '../components/HospitalList.vue'
import Register from '../components/Register.vue'

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
    path: '/quiz',
    name: 'quiz',
    compoent: () => import('../components/Quiz.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
