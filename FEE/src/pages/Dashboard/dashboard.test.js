import React from 'react';
import { createRoot } from 'react-dom/client';
import Dashboard from './index';
import { Provider } from 'react-redux';
import { store } from '../../store';

it('renders without crashing', () => {
  const div = document.createElement('div');
  const root = createRoot(div);
  root.render(
    <Provider store={store}>
      <Dashboard />
    </Provider>,
  );
  root.unmount();
});
