import axios from 'axios';
import { config } from '../../config';

function get_summary({ queryKey }) {
  const [, payload] = queryKey;
  const url = `${config.apiEndpoint}/dashboard/summary`;
  const authUser = payload;
  const reqConfig = {
    headers: {
      authorization: `Token ${authUser.result.key}`,
    },
  };

  return axios.get(url, reqConfig);
}

export { get_summary };
