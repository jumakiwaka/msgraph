import React from 'react';
import { createRoot } from 'react-dom/client';
import ErrorHandler from './index';

it('renders without crashing', () => {
  const div = document.createElement('div');
  const root = createRoot(div);
  root.render(<ErrorHandler />);
  root.unmount();
});
