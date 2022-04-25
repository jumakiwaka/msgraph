import { configureStore } from '@reduxjs/toolkit';
import authUserSlice from '../reducers';

export const store = configureStore({
  reducer: {
    authUser: authUserSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});
