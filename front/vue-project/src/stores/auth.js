import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { useToastStore } from "./toast";

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter();
  const token = ref(null);
  const userProfile = ref(null);
  const toastStore = useToastStore();

  // 초기화 함수를 단순화
  const initializeAuth = () => {
    const auth = localStorage.getItem("auth");
    if (auth) {
      try {
        const parsedAuth = JSON.parse(auth);
        token.value = parsedAuth.token;
      } catch (e) {
        localStorage.removeItem("auth");
        token.value = null;
      }
    } else {
      token.value = null;
    }
  };

  const getUserProfile = async () => {
    try {
      const storedAuth = JSON.parse(localStorage.getItem("auth"));
      if (!storedAuth?.token) return null;

      const response = await axios({
        method: "get",
        url: "http://127.0.0.1:8000/accounts/user/",
        headers: {
          Authorization: `Token ${storedAuth.token}`,
        },
      });

      userProfile.value = response.data;
      return response.data;
    } catch (error) {
      console.error("userProfile을 불러오지 못했습니다", error);
      return null;
    }
  };

  // 회원가입
  const signUp = function (payload) {
    axios({
      method: "post",
      url: "http://127.0.0.1:8000/accounts/signup/",
      data: {
        username: payload.username,
        nickname: payload.nickname,
        password1: payload.password1,
        password2: payload.password2,
      },
    })
      .then((res) => {
        console.log("회원가입 응답:", res);
        toastStore.addToast("회원가입이 완료되었습니다.", "success");
        // alert("회원가입이 완료되었습니다.");
        router.push({ name: "login" });
      })
      .catch((err) => {
        console.error("회원가입 에러:", err.response?.data || err);
        if (err.response?.data) {
          // 서버에서 오는 에러 메시지 표시
          const errors = err.response.data;
          for (const field in errors) {
            alert(`${field}: ${errors[field].join(" ")}`);
          }
        } else {
          toastStore.addToast("회원가입 중 오류가 발생했습니다.", "error");
        }
      });
  };

  // isLogin computed를 단순화
  const isLogin = computed(() => {
    const hasToken = token.value !== null;
    return hasToken;
  });

  // 로그인 상태 확인
  const isAuthenticated = computed(() => token.value !== null);
  // 로그인
  const logIn = async (payload) => {
    try {
      const { username, password } = payload;
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/accounts/login/",
        data: { username, password },
      });

      token.value = response.data.key;
      localStorage.setItem(
        "auth",
        JSON.stringify({
          token: response.data.key,
          username: username,
        })
      );
      toastStore.addToast(`${username} 님 환영합니다!`, "success");
      router.push({ name: "Home" });
    } catch (error) {
      console.error("Login error:", error);
      toastStore.addToast("로그인에 실패했습니다.", "error");
      // alert("로그인에 실패했습니다.");
    }
  };

  // 로그아웃
  const logout = async () => {
    try {
      if (token.value) {
        await axios({
          method: "post",
          url: "http://127.0.0.1:8000/accounts/logout/",
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      token.value = null;
      localStorage.removeItem("auth");
      // toastStore.addToast("로그아웃 되었습니다.", "success");
      router.push({ name: "Home" });
    }
  };
  initializeAuth();
  return { signUp, logIn, token, isLogin, logout, isAuthenticated, initializeAuth, getUserProfile };
});
