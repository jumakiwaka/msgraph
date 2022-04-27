import axios from 'axios';
import { config } from '../../config';

function login(payload) {
  const url = `${config.apiEndpoint}/auth/login`;
  return axios.post(url, payload);
}

function logout(payload) {}

export { login, logout };
