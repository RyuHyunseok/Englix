import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SurveyView from "../views/SurveyView.vue";
import MovieView from "../views/MovieView.vue";
import { useAuthStore } from "@/stores/auth";
import LoginView from "@/views/LoginView.vue";
import SignUpView from "@/views/SignUpView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import CommunityView from "@/views/CommunityView.vue";
import FreeBoard from "@/views/community/FreeBoard.vue";
import PostCreateView from "@/views/PostCreateView.vue";
import PostDetail from "@/views/PostDetail.vue";
import ProfileView from "@/views/ProfileView.vue";
import FavoriteMovies from "@/views/FavoriteMovies.vue";
import MyPageView from "@/views/MyPageView.vue";
import MovieListView from "@/views/MovieListView.vue";
import LearningResources from "@/views/community/LearningResources.vue";
import QandA from "@/views/community/QandA.vue";
import ResourceView from "@/views/ResourceView.vue";
import QandAView from "@/views/QandAView.vue";
import SearchResultsView from "@/views/SearchResultsView.vue";
import CommunitySearchResults from "@/views/CommunitySearchResults.vue";
import RankingView from "@/views/RankingView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomeView,
    },
    {
      path: "/survey",
      name: "survey",
      component: SurveyView,
      meta: { requiresAuth: true },
    },
    {
      path: "/movie",
      name: "movie",
      component: MovieView,
      props: (route) => ({
        category: route.query.category,
        level: route.query.level,
        genre: route.query.genre,
        prefer_genre: route.query.prefer_genre,
      }),
    },
    {
      path: "/movie-detail/:tmdbId",
      name: "MovieDetail",
      component: MovieDetailView,
    },
    {
      path: "/movielist",
      name: "movielist",
      component: MovieListView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignUpView,
    },
    {
      path: "/community",
      name: "community",
      component: CommunityView,
    },
    {
      path: "/free-board",
      name: "freeBoard",
      component: FreeBoard,
    },
    {
      path: "/QandA",
      name: "QandA",
      component: QandA,
    },
    {
      path: "/LearningResources",
      name: "LearningResources",
      component: LearningResources,
    },
    {
      path: "/posts/create",
      name: "postCreate",
      component: PostCreateView,
    },
    {
      path: "/posts/:id",
      name: "postDetail",
      component: PostDetail,
    },
    {
      path: "/profile/:username",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/favorite-movies",
      name: "favoriteMovies",
      component: FavoriteMovies,
      meta: { requiresAuth: true },
    },
    {
      path: "/mypage",
      name: "mypage",
      component: MyPageView,
    },
    {
      path: "/resource",
      name: "resource",
      component: ResourceView,
    },
    {
      path: "/Q&A",
      name: "Q&A",
      component: QandAView,
    },
    {
      path: "/ranking",
      name: "ranking",
      component: RankingView,
    },
    {
      path: "/search",
      name: "searchResults",
      component: SearchResultsView,
    },
    {
      path: "/community/search",
      name: "communitySearchResults",
      component: CommunitySearchResults,
    },
  ],
});

router.beforeEach((to, from, next) => {
  // next 매개변수 추가
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: "login" }); // 'Login' -> 'login' (라우터에 정의된 name과 일치시킴)
  } else {
    next();
  }
});
export default router;
