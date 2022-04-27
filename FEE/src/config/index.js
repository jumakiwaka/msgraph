export const config = {
  clientId: process.env.REACT_APP_CLIENT_ID,
  scopes: process.env.REACT_APP_SCOPES,
  redirectUrl: process.env.REACT_APP_REDIRECT_URI,
  msBaseAuthUrl:
    'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
  apiEndpoint: process.env.REACT_APP_BEE_ENDPOINT,
  supportedLocales: ['en-US'],
};
