import React from 'react';
import MicrosoftLogin from 'react-microsoft-login';

class SocialButton extends React.Component {
  render() {
    const { children, clientId, authCallbackHandler, ...props } = this.props;
    return (
      <MicrosoftLogin
        authCallback={authCallbackHandler}
        clientId={clientId}
        {...props}>
        {children}
      </MicrosoftLogin>
    );
  }
}

export default SocialButton;
