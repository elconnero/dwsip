import { useEffect, useState } from 'react';
import { authClient } from '../lib/auth';

export function useAuth() {
  const [token, setToken]   = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    authClient.getToken()
      .then(t => setToken(t ?? null))
      .catch(() => setToken(null))
      .finally(() => setLoading(false));
  }, []);

  return { token, isLoggedIn: !!token, loading };
}
