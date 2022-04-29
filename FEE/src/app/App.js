import {
  Route,
  BrowserRouter as Router,
  Routes,
  useLocation,
  Navigate,
  Outlet,
} from 'react-router-dom';
import { Container } from 'react-bootstrap';
import Dashboard from '../pages/Dashboard';
import Login from './Login';
import { useIsUserLoggedIn } from '../hooks';
import './App.scss';
import Loader from './Loader';

/**
 * Handles application level routing.
 * It sets a middleware for private and public routes.
 */
function App() {
  return (
    <Container className="main">
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<PrivateRoute />}>
            <Route index element={<Dashboard />} />
          </Route>
        </Routes>
      </Router>
    </Container>
  );
}

/** Middleware for private routes. */
const PrivateRoute = () => {
  const location = useLocation();
  const { isLoading, isLoggedIn } = useIsUserLoggedIn();

  if (isLoading) return <Loader />;

  return isLoggedIn ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: location }} />
  );
};

export default App;
