<template>
  <div class="login-container">
    <div class="form-box">
      <div class="header">
        <h1 class="title">Hey! 👋</h1>
        <p class="subtitle">Ready to continue your learning journey?</p>
      </div>

      <form @submit.prevent="logIn" class="login-form">
        <div class="form-group">
          <label for="username">
            <i class="fas fa-user"></i>
            아이디
          </label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            placeholder="Enter your username"
          />
        </div>

        <div class="form-group">
          <label for="password">
            <i class="fas fa-lock"></i>
            비밀번호
          </label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password" 
            placeholder="Enter your password"
          />
        </div>

        <button type="submit" class="submit-btn">
          <span>Sign In</span>
          <i class="fas fa-sign-in-alt"></i>
        </button>

        <p class="signup-link">
          Don't have an account? 
          <router-link to="/signup">Join Now</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";

const store = useAuthStore();
const username = ref(null);
const password = ref(null);

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);
};
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  // 혹시 스크롤이 생기는 것을 방지
  overflow-x: hidden;
  
}
.form-box {
  width: 100%;
  // max-width: 480px; // SignUpView
  max-width: 420px; // LoginView
  padding: 40px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); // 그림자를 좀 더 은은하게 조정
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 2.5rem;
  color: #ff6b6b;
  margin-bottom: 10px;
  font-weight: 700;
}

.subtitle {
  color: #868e96;
  font-size: 1.1rem;
}

.login-form {
  .form-group {
    margin-bottom: 24px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    color: #495057;
    font-weight: 500;
    font-size: 0.95rem;
    
    i {
      margin-right: 8px;
      color: #ff6b6b;
    }
  }

  input {
    width: 90%;
    padding: 12px 16px;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.3s ease;

    &:focus {
      border-color: #ff6b6b;
      outline: none;
      box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
    }

    &::placeholder {
      color: #adb5bd;
    }
  }

  .submit-btn {
    width: 98%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: #ff6b6b;
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;

    &:hover {
      background: #fa5252;
      transform: translateY(-2px);
    }
  }

  .signup-link {
    text-align: center;
    margin-top: 20px;
    color: #868e96;

    a {
      color: #ff6b6b;
      text-decoration: none;
      font-weight: 600;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
}

@media (max-width: 480px) {
  .form-box {
    padding: 30px 20px;
  }

  .title {
    font-size: 2rem;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.login-container {
  animation: fadeInUp 0.6s ease-out;
}

.form-box {
  animation: fadeInUp 0.6s ease-out 0.2s;
  animation-fill-mode: both;
}
</style>