import { useState, useEffect } from 'react';
import { getAuthStatus } from '../lib/index';
import { useSessionStorage } from './useSessionStorage';
import { useDispatch } from 'react-redux';
import { setAuthUser } from '../reducers/';

function useIsUserLoggedIn() {
  const [isLoggedIn, setIsLoggedIn] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const [token] = useSessionStorage('token');
  const dispatch = useDispatch();

  useEffect(() => {
    setIsLoading(true);
    const payload = {
      token: token?.key || '',
    };
    getAuthStatus(payload)
      .then((res) => {
        if (res.status === 200) {
          const { data } = res;
          const { result } = data;

          if (result) {
            setIsLoggedIn(true);
            dispatch(setAuthUser(token));
            setIsLoading(false);
          } else {
            setIsLoggedIn(false);
            setIsLoading(false);
          }
        } else {
          setIsLoggedIn(false);
          setIsLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
        setIsLoggedIn(false);
        setIsLoading(false);
      });
  }, []);

  return { isLoggedIn, isLoading };
}

export { useIsUserLoggedIn };
