import {
  Route,
  BrowserRouter as Router,
  Routes,
  useLocation,
  Navigate,
  Outlet,
} from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Container } from 'react-bootstrap';
import Dashboard from '../pages/Dashboard';
import LandingPage from '../pages/LandingPage';
import './App.scss';

/**
 * Handles application level routing.
 * It sets a middleware for private and public routes.
 */
function App() {
  return (
    <Container className="main">
      <Router>
        <Routes>
          <Route path="/login" element={<LandingPage />} />
          <Route path="/" element={<PrivateRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
        </Routes>
      </Router>
    </Container>
  );
}

/** Middleware for private routes. */
const PrivateRoute = () => {
  const location = useLocation();
  const user = useSelector((state) => state.authUser.value);
  return user ? (
    <Outlet />
  ) : (
    <Navigate to="/login" state={{ from: location }} />
  );
};

export default App;
