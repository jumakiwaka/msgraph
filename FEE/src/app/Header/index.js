import React from 'react';
import { useSelector } from 'react-redux';
import { Navbar, Container, NavDropdown, Nav } from 'react-bootstrap';
import msLogo from '../../assets/images/ms-icon.png';

function Header(props) {
  const authUser = useSelector((state) => state.authUser.value);
  const { user_profile: userProfile } = authUser;

  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand href="/">
          <img
            alt=""
            src={msLogo}
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{' '}
          Microsoft Graph
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <NavDropdown
              title={`Hi, ${userProfile.givenName}`}
              id="basic-nav-dropdown"
              align={'end'}>
              <NavDropdown.Item disabled>
                {userProfile.userPrincipalName}
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="">Logout</NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
