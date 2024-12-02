import axios from "axios";
import { ref } from "vue";
import { defineStore } from "pinia";

export const usePostStore = defineStore("posts", () => {
  const posts = ref([]);

  const getPosts = function () {
    const auth = localStorage.getItem('auth');
    const token = auth ? JSON.parse(auth).token : null;

    return axios({
      method: "get",
      url: "http://127.0.0.1:8000/community/posts/",
      headers: token ? {
        'Authorization': `Token ${token}`
      } : {}
    })
    .then((res) => {
      posts.value = res.data;
    })
    .catch(error => {
      console.error('Error fetching posts:', error);
      throw error;
    });
  };

  const getPostDetail = function (postId) {
    const auth = localStorage.getItem('auth');
    const token = auth ? JSON.parse(auth).token : null;
  
    return axios({
      method: "get",
      url: `http://127.0.0.1:8000/community/posts/${postId}/`,
      headers: token ? {
        'Authorization': `Token ${token}`
      } : {}
    })
    .then((res) => {
      console.log('Post detail response:', res.data);  // 응답 데이터 확인
      return res.data;
    })
    .catch(error => {
      console.error('Error fetching post detail:', error);
      throw error;
    });
  };


const createPost = function (title, content, category) { 
  const auth = localStorage.getItem('auth');
  const token = JSON.parse(auth).token;

  return axios({
    url: "http://127.0.0.1:8000/community/posts/",
    method: "POST",
    headers: {
      'Authorization': `Token ${token}`
    },
    data: { title, content, category } 
  })
  .then((res) => {
    posts.value.unshift(res.data);
    return res.data.id;
  });
};

  const updatePost = function (postId, title, content) {
    const auth = localStorage.getItem('auth');
    const token = JSON.parse(auth).token;

    return axios({
      url: `http://127.0.0.1:8000/community/posts/${postId}/`,
      method: "PUT",
      headers: {
        'Authorization': `Token ${token}`
      },
      data: { title, content }
    });
  };

  const deletePost = function (postId) {
    const auth = localStorage.getItem('auth');
    const token = JSON.parse(auth).token;

    return axios({
      url: `http://127.0.0.1:8000/community/posts/${postId}/`,
      method: "DELETE",
      headers: {
        'Authorization': `Token ${token}`
      }
    });
  };

  return { posts, getPosts, getPostDetail, createPost, updatePost, deletePost };
});