import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import LoginPageView from '@/views/LoginPageView.vue'
import SignupPageView from '@/views/SignupPageView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieCredit from '@/components/MovieCredit/MovieCredit.vue'
import MovieReview from '@/components/MovieReview/MovieReview.vue'
import SearchPageView from '@/views/SearchPageView.vue'
import DirecDetailView from '@/views/DirecDetailView.vue'
import ActorDetailView from '@/views/ActorDetailView.vue'
import GenreSelectionView from '@/views/GenreSelectionView.vue'
import MyPageView from '@/views/MyPageView.vue'
import MyPlaylistView from '@/views/MyPlaylistView.vue'
import MyPlaylistDetailView from '@/views/MyPlaylistDetailView.vue'
import MyMovieView from '@/views/MyMovieView.vue'
import MyDirectorView from '@/views/MyDirectorView.vue'
import MyActorView from '@/views/MyActorView.vue'
import GoogleCallbackView from '@/views/GoogleCallbackView.vue'

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
        { path: '', name: 'MovieCredit', component: MovieCredit },
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
    {
      path: '/detail/actor/:actor_id',
      name: 'ActorDetailView',
      component: ActorDetailView
    },
    {
      path: '/genre-selection',
      name: 'GenreSelectionView',
      component: GenreSelectionView
    },
    {
      path: '/mypage/:id',
      name: 'MyPageView',
      component: MyPageView
    },
    {
      path: '/mypage/:id/my-playlist',
      name: 'MyPlaylistView',
      component: MyPlaylistView
    },
    {
      path: '/mypage/:id/my-playlist/:playlist_id',
      name: 'MyPlaylistDetailView',
      component: MyPlaylistDetailView
    },
    {
      path: '/mypage/:id/my-movie',
      name: 'MyMovieView',
      component: MyMovieView
    },
    {
      path: '/mypage/:id/my-director',
      name: 'MyDirectorView',
      component: MyDirectorView
    },
    {
      path: '/mypage/:id/my-actor',
      name: 'MyActorView',
      component: MyActorView
    },
    { path: '/google/callback/', name: 'GoogleCallbackView', component: GoogleCallbackView },
  ],

  scrollBehavior(to, from, savedPosition) {
    if (to.name.startsWith('Movie') && from.name?.startsWith('Movie')) {
      // MovieDetailView의 children route 간 이동 시 스크롤 유지
      return false
    }
    if (savedPosition) {
      // 뒤로가기/앞으로가기 시 저장된 위치로 이동
      return savedPosition
    }
    // 기본 동작: 항상 상단으로 스크롤
    return { top: 0 }
  }
})

export default router
