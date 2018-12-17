import axios from 'axios';

import { resetState, setLoginError } from 'actions';
import store from 'Store';

const config = require('../config.json');

const { APISERVER } = config;

const errorCodesToErrorMsg = (errorCode) => {
  switch (errorCode) {
    case 400:
      return 'Wrong login credentials.';
    case 401:
      return 'You need to be logged in to view this page.';
    case 404:
      return 'Couldnt connect to Server. Please try again.';
    case 504:
      return 'Active Directory timeout. Please try again.';
    case 520:
      return 'An unknown error occured. Please try again.';
    default:
      return 'An unknown error occured. Please try again.';
  }
};

class RestCom {
  constructor(restPoint, data) {
    this.restApi = APISERVER + restPoint;
    this.data = data;
  }

  async post() {
    const headers = {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
    };
    return axios
      .post(this.restApi, this.data, headers)
      .then(ServerResponse => ServerResponse)
      .catch((error) => {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          const errorMsg = errorCodesToErrorMsg(error.response.status);
          if (error.response.status === 401) {
            // user is not logged in and has no permission to do the request
            store.dispatch(resetState);
            store.dispatch(setLoginError(errorMsg));
          } else {
            throw new Error(errorMsg);
          }
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
          // http.ClientRequest in node.js
          throw new Error(
            'An error occured while connecting to the server. Please check your Internet connection.',
          );
        } else {
          // Something happened in setting up the request that triggered an Error
          throw new Error(errorCodesToErrorMsg(520));
        }
      });
  }
}
export default RestCom;
