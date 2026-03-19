import { createInternalNeonAuth } from '@neondatabase/neon-js/auth';

const neonAuth = createInternalNeonAuth(import.meta.env.VITE_NEON_AUTH_URL);

// adapter is passed to NeonAuthUIProvider and used by useAuthenticate()
export const authClient = neonAuth.adapter;

// getToken() returns the JWT for Authorization headers to the FastAPI backend
export function getToken(): Promise<string | null> {
  return neonAuth.getJWTToken();
}
