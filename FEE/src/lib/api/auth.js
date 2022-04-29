import axios from 'axios';
import { config } from '../../config';

let cancel;
const { CancelToken } = axios;

function login(payload) {
  if (cancel !== undefined) {
    cancel();
  }
  const url = `${config.apiEndpoint}/auth/login`;
  const reqConfig = {
    cancelToken: new CancelToken((c) => {
      cancel = c;
    }),
  };
  return axios.post(url, payload, reqConfig);
}

function getAuthStatus(payload) {
  const { token } = payload;

  const url = `${config.apiEndpoint}/auth/status`;
  const reqConfig = {
    headers: {
      authorization: `Token ${token}`,
    },
  };
  return axios.get(url, reqConfig);
}

function logout(payload) {}

export { login, logout, getAuthStatus };
