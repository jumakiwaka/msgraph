import React from 'react';
import { Row, Card, Col } from 'react-bootstrap';
import './dashboard.css';

function Dashboard(props) {
  return (
    <Row className="mt-4 text-center">
      <Col>
        <Card bg="" className="shadow-sm">
          <Card.Title>Incoming Mails</Card.Title>
          <Card.Body>{Math.random() * 1000}</Card.Body>
        </Card>
      </Col>
      <Col>
        <Card bg="" className="shadow-sm">
          <Card.Title>Outgoing Mail</Card.Title>
          <Card.Body>{Math.random() * 1000}</Card.Body>
        </Card>
      </Col>
      <Col>
        <Card bg="" className="shadow-sm">
          <Card.Title>Reply Ratio</Card.Title>
          <Card.Body>{Math.random() * 1000}</Card.Body>
        </Card>
      </Col>
    </Row>
  );
}

export default Dashboard;
