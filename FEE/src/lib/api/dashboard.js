import axios from 'axios';
import { config } from '../../config';

function getSummary({ queryKey }) {
  const [, payload] = queryKey;
  const url = `${config.apiEndpoint}/dashboard/summary`;
  const authUser = payload;
  const reqConfig = {
    headers: {
      authorization: `Token ${authUser.key}`,
    },
  };

  return axios.get(url, reqConfig);
}

export { getSummary };
