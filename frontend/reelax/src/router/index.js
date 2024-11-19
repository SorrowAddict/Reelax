import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import LoginPageView from '@/views/LoginPageView.vue'
import SignupPageView from '@/views/SignupPageView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieCredit from '@/components/Movie/MovieCredit.vue'
import MovieReview from '@/components/Movie/MovieReview.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainPageView',
      component: MainPageView
    },
    {
      path: '/login',
      name: 'LoginPageView',
      component: LoginPageView
    },
    {
      path: '/signup',
      name: 'SignupPageView',
      component: SignupPageView
    },
    {
      path: '/detail',
      name: 'MovieDetailView',
      component: MovieDetailView,
      children: [
        { path: 'credit', name: 'MovieCredit', component: MovieCredit },
        { path: 'review', name: 'MovieReview', component: MovieReview }
      ]
    },
  ],
})

export default router
