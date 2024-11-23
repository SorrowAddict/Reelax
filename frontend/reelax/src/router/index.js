import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'
import LoginPageView from '@/views/LoginPageView.vue'
import SignupPageView from '@/views/SignupPageView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieCredit from '@/components/Movie/MovieCredit.vue'
import MovieReview from '@/components/Movie/MovieReview.vue'
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
    }
  ],
})

export default router
