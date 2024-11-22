import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import LoginPageView from '@/views/LoginPageView.vue'
import SignupPageView from '@/views/SignupPageView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieCredit from '@/components/Movie/MovieCredit.vue'
import MovieReview from '@/components/Movie/MovieReview.vue'
import SearchPageView from '@/views/SearchPageView.vue'
import DirecDetailView from '@/views/DirecDetailView.vue'

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
      path: '/detail/:id',
      name: 'MovieDetailView',
      component: MovieDetailView,
      children: [
        { path: '', name: 'MovieCreditDefault', component: MovieCredit },
        { path: 'credit', name: 'MovieCredit', component: MovieCredit },
        { path: 'review', name: 'MovieReview', component: MovieReview }
      ]
    },
    {
      path: '/search',
      name: 'SearchPageView',
      component: SearchPageView,
    },
    {
      path: '/detail/direc/:direc_id',
      name: 'DirecDetailView',
      component: DirecDetailView
    },
  ],
})

export default router
