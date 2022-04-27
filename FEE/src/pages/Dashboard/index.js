import React from 'react';
import { Row, Card, Col } from 'react-bootstrap';
import { useSelector } from 'react-redux';
import { useQuery } from 'react-query';
import { get_summary, intl_number_format } from '../../lib';
import './dashboard.css';
import ErrorHandler from '../../app/ErrorHandler';
import Loader from '../../app/Loader';

function Dashboard(props) {
  const authUser = useSelector((state) => state.authUser.value);
  const { isLoading, isSuccess, isError, status, data, error } = useQuery(
    ['get_dashboard_summary', authUser],
    get_summary,
  );

  const { data: resData } = data;

  console.log(isLoading, isSuccess, isError, status, data, error);

  if (isLoading) return <Loader />;
  if (isError) return <ErrorHandler error={error} />;

  return (
    <>
      <Row className="mt-4 text-center">
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Average Read Time</Card.Title>
            <Card.Body>{intl_number_format(resData.avg_read_time)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Response Time</Card.Title>
            <Card.Body>{intl_number_format(resData.response_time)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Send Ratio</Card.Title>
            <Card.Body>{intl_number_format(resData.send_ratio)}</Card.Body>
          </Card>
        </Col>
      </Row>
      <Row className="mt-4 text-center">
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Today Emails</Card.Title>
            <Card.Body>{intl_number_format(resData.today_emails)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Unread Mails</Card.Title>
            <Card.Body>{intl_number_format(resData.unread)}</Card.Body>
          </Card>
        </Col>
        <Col>
          <Card bg="" className="shadow-sm">
            <Card.Title>Reply Ratio</Card.Title>
            <Card.Body>{intl_number_format(resData.send_ratio)}</Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}

export default Dashboard;
