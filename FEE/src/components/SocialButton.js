import React, { useState } from 'react';
import { Button, Image } from 'react-bootstrap';
import MSlogo from '../assets/images/ms-icon.png';
import { config } from '../config';
class SocialButton extends React.Component {
  openMsLoginWindow() {
    const requestConfig = {
      url: config.msBaseAuthUrl,
      params: {
        client_id: config.clientId,
        response_type: 'code',
        redirect_uri: config.redirectUrl,
        response_mode: 'query',
        scope: config.scopes,
        state: Math.random() * 1000,
      },
    };

    const url = `${requestConfig.url}?
    client_id=${requestConfig.params.client_id}&
    response_type=code&
    redirect_uri=${requestConfig.params.redirect_uri}&
    response_mode=${requestConfig.params.response_mode}&
    scope=${requestConfig.params.scope}&
    state=${requestConfig.params.state}`;

    window.open(url, '_parent');
  }

  render() {
    const { children } = this.props;
    return (
      <Button onClick={this.openMsLoginWindow} {...this.props}>
        <Image src={MSlogo} width={25} height={25} /> {children}
      </Button>
    );
  }
}

export default SocialButton;
