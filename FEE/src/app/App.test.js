import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { store } from '../store';
import { Provider } from 'react-redux';

it('renders without crashing', () => {
  const div = document.createElement('div');
  const root = createRoot(div);
  root.render(
    <Provider store={store}>
      <App />
    </Provider>,
  );
  root.unmount();
});
