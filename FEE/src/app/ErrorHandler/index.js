import React, { Component } from 'react';
import { Alert, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

class ErrorHandler extends Component {
  render() {
    const error = this.props.error;
    let status = '';
    let statusText = 'Oh snap! You got an error!';
    let message = 'Something unexpected happened. Please try again.';
    if (error) {
      status = error.status || status;
      statusText = error.statusText || statusText;
      if (error.data && error.data.error) {
        message = error.data.error.message || message;
      }
    }
    return (
      <Alert color="warning" className="mt-4 mb-4">
        <h4>{statusText}</h4>
        <p>{this.props.message || message}</p>
        <p>
          <small>{status}</small>
        </p>

        <Link to="/">
          <Button variant="outline-primary">Go Home</Button>
        </Link>
      </Alert>
    );
  }
}

export default ErrorHandler;
