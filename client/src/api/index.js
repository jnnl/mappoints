import axios from 'axios';
import config from '@/config'
import router from '@/router'
import store from '@/store'

export default() => {
  let headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }

  if (store.state.token != null) {
    headers.Authorization = 'JWT ' + store.state.token
  }

  const api = axios.create({
    baseURL: config.API_URL,
    headers: headers,
  })

  api.interceptors.response.use((response) => {
    return response
  }, (error) => {
    // Logout if the response is 401
    if (error.request && error.request.status === 401) {
      router.push('/login') 
      store.dispatch('logout')
    }
    return Promise.reject(error);
  });

  return api
}
