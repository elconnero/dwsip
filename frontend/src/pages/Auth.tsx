import { AuthView } from '@neondatabase/neon-js/auth/react';
import { useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Auth() {
  const { pathname } = useLocation();

  return (
    <div className="min-h-screen bg-nes-dark flex flex-col items-center justify-center px-4 py-12">
      <Link to="/" className="text-nes-gold text-sm no-underline mb-8 hover:text-nes-white transition-colors">
        🎮 DWISP
      </Link>
      <div className="w-full max-w-2xl border-4 border-nes-gold bg-nes-black p-12">
        <AuthView pathname={pathname} />
      </div>
    </div>
  );
}

export default Auth;
