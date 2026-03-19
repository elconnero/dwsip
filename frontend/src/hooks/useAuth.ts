import { useAuthenticate } from '@neondatabase/neon-js/auth/react';
import { useEffect, useRef, useState } from 'react';
import { getToken } from '../lib/auth';

export function useAuth() {
  const { user, isPending } = useAuthenticate();
  const [token, setToken] = useState<string | null>(null);
  const wasLoggedIn = useRef(false);

  useEffect(() => {
    if (user) {
      getToken().then(t => setToken(t ?? null));

      // Just transitioned from logged-out → logged-in: clear guest lock
      if (!wasLoggedIn.current) {
        localStorage.removeItem('guestRequestUsed');
      }
      wasLoggedIn.current = true;
    } else if (!isPending) {
      setToken(null);
      wasLoggedIn.current = false;
    }
  }, [user, isPending]);

  return {
    user,
    token,
    email: user?.email ?? null,
    isLoggedIn: !!user,
    loading: isPending,
  };
}
