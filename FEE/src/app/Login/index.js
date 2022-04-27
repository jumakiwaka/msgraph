import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate, useSearchParams } from 'react-router-dom';
import SocialButton from '../../components/SocialButton';
import { setAuthUser } from '../../reducers';
import WelcomeText from '../WelcomeText';
import { Row, Col, Card } from 'react-bootstrap';
import Loader from '../Loader';
import { login } from '../../lib';
import './login.scss';
import ErrorHandler from '../ErrorHandler';

function LandingPage(props) {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState();

  useEffect(() => {
    const authCode = searchParams.get('code');
    if (authCode && !isLoading) {
      setIsLoading(true);
      const payload = {
        code: authCode,
      };

      login(payload)
        .then((res) => {
          if (res.status === 200) {
            setIsLoading(false);
            dispatch(setAuthUser(res.data));
            navigate('/dashboard');
          } else {
            setIsLoading(false);
            const error = {
              error: res.data.error,
              statusText: res.statusText,
              status: res.status,
            };
            setError(error);
          }
        })
        .catch((err) => {
          console.log(err);
          setIsLoading(false);
          setError(err.response || err);
        });
    }
  }, [searchParams.get('code')]);

  if (isLoading) return <Loader />;
  if (error) return <ErrorHandler error={error} />;

  if (searchParams.get('error')) {
    const error = {
      statusText: searchParams.get('error'),
      message: searchParams.get('error_description'),
    };
    return <ErrorHandler error={error} />;
  }

  return (
    <Row className="login align-items-center">
      <Col md={{ span: 4, offset: 4 }}>
        <Card className="border shadow-sm">
          <Card.Body className="text-center">
            <WelcomeText />
            <SocialButton>Login with Miscrosoft</SocialButton>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
}

export default LandingPage;
