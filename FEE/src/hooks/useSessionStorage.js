import { useState } from 'react';

function setSessionStorage(key, value) {
  sessionStorage.setItem(key, JSON.stringify(value));
}

function useSessionStorage(key, initialValue = null) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      // Get from local storage by key
      const item = sessionStorage.getItem(key);
      // Parse stored json or if none return initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      // If error also return initialValue
      console.error(error);
      return initialValue;
    }
  });

  // Return a wrapped version of useState's setter function that ...
  // ... persists the new value to sessionStorage.
  const setValue = (value) => {
    try {
      // Allow value to be a function so we have same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      setSessionStorage(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [JSON.parse(storedValue), setValue];
}

export { useSessionStorage };
