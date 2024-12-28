import {loadStripe} from '@stripe/stripe-js';
const stripe = loadStripe("pk_test_51QN5rkDs4Bx5tcZCdzyFujoE5o8EdupmuSrkMNmHtKkzHuMv3Zx3mHxeEp3nCCIcyymSFkZ8oPW93qXA6FCm5mZz00GkzfcJUA", {
  betas: ['custom_checkout_beta_4'],
});

import React from 'react';
import {CustomCheckoutProvider} from '@stripe/react-stripe-js';

const App = ({clientSecret}) => {
  const [clientSecret, setClientSecret] = React.useState(null);
  React.useEffect(() => {
    fetch('/create-checkout-session', {method: 'POST'})
      .then((response) => response.json())
      .then((json) => setClientSecret(json.clientSecret))
  });

  if (clientSecret) {
    return (
      <CustomCheckoutProvider
        stripe={stripe}
        options={{clientSecret}}
      >
        <CheckoutForm />
      </CustomCheckoutProvider>
    );
  } else {
    return null;
  }
};

export default App;