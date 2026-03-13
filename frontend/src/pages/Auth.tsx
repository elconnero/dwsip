import { AuthView } from '@neondatabase/neon-js/auth/react';
import { useLocation } from 'react-router-dom';

function Auth() {
  const { pathname } = useLocation();
  return <AuthView pathname={pathname} />;
}

export default Auth;
