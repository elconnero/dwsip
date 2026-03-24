import { useAuthenticate } from '@neondatabase/neon-js/auth/react';
import { useEffect, useRef } from 'react';

export function useAuth() {
  const { user, isPending } = useAuthenticate({ enabled: false });
  const wasLoggedIn = useRef(false);

  useEffect(() => {
    if (user) {
      if (!wasLoggedIn.current) {
        localStorage.removeItem('guestRequestUsed');
      }
      wasLoggedIn.current = true;
    } else if (!isPending) {
      wasLoggedIn.current = false;
    }
  }, [user, isPending]);

  return {
    user,
    email: user?.email ?? null,
    isLoggedIn: !!user,
    loading: isPending,
  };
}
