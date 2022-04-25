import React from 'react';
import { Spinner } from 'react-bootstrap';
import './Loader.scss';

const Loader = ({ className = '' }) => {
  return (
    <div className={`Loader pt-5 pb-5 ${className}`}>
      <Spinner animation="border" variant="primary" />
    </div>
  );
};

export default Loader;
