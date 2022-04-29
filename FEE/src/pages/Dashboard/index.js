import React from 'react';
import { Row, Card, Col } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { useQuery } from 'react-query';
import { getSummary, intlNumberFormat } from '../../lib';
import './dashboard.css';
import ErrorHandler from '../../app/ErrorHandler';
import Loader from '../../app/Loader';
import Header from '../../app/Header';

function Dashboard(props) {
  const authUser = useSelector((state) => state.authUser.value);
  const { isLoading, isSuccess, isError, status, data, error } = useQuery(
    ['get_dashboard_summary', authUser],
    getSummary,
  );

  if (isLoading) return <Loader />;
  if (isError) return <ErrorHandler error={error} />;

  const { data: resData } = data;
  const { result } = resData;

  return (
    <>
      <Header />
      <Row className="mt-4 text-center">
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Average Read Time</Card.Title>
            <Card.Body>{result.avg_read_time}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Response Time</Card.Title>
            <Card.Body>{intlNumberFormat(result.response_time)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Send Ratio</Card.Title>
            <Card.Body>{intlNumberFormat(result.send_ratio)}</Card.Body>
          </Card>
        </Col>
      </Row>
      <Row className="mt-4 text-center">
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Today Emails</Card.Title>
            <Card.Body>{intlNumberFormat(result.today_emails)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Unread Mails</Card.Title>
            <Card.Body>{intlNumberFormat(result.unreads)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>All Mails(Inbox & Sent)</Card.Title>
            <Card.Body>{intlNumberFormat(result.all_mails)}</Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}

export default Dashboard;
