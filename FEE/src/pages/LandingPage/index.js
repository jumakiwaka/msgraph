import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import MicrosoftLogin from 'react-microsoft-login';
import { config } from '../../config';
import { setAuthUser } from '../../reducers';
import WelcomeText from '../../app/WelcomeText';
import { Row, Col, Card } from 'react-bootstrap';
import './landing-page.scss';

function LandingPage(props) {
  const [msalInstance, onMsalInstanceChange] = useState();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const loginHandler = (err, data, msal) => {
    console.log(err, data, msal);
    // some actions
    if (!err && data) {
      onMsalInstanceChange(msal);
      dispatch(setAuthUser(data));
      navigate('/dashboard');
    }
  };

  const logoutHandler = () => {
    msalInstance.logout();
  };

  return (
    <Row className="landing-page align-items-center">
      <Col md={{ span: 4, offset: 4 }}>
        <Card className="border shadow-sm">
          <Card.Body className="text-center">
            <WelcomeText />
            {msalInstance ? (
              <button onClick={logoutHandler}>Logout</button>
            ) : (
              <MicrosoftLogin
                clientId={config.clientId}
                authCallback={loginHandler}
                redirectUri="http://localhost:3000"
              />
            )}
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
}

export default LandingPage;
