import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

function Navbar() {
  const { isLoggedIn, loading } = useAuth();

  return (
    <nav className="w-full border-b-4 border-nes-gold bg-nes-black px-6 py-4 flex items-center justify-between">
      <Link to="/" className="text-nes-gold text-sm no-underline hover:text-nes-white transition-colors">
        🎮 DWISP
      </Link>

      <div className="flex gap-6 items-center">
        {!loading && (
          <>
            {isLoggedIn ? (
              <>
                <Link to="/profile" className="text-nes-white text-xs no-underline hover:text-nes-gold transition-colors">
                  PROFILE
                </Link>
                <Link to="/saved" className="text-nes-white text-xs no-underline hover:text-nes-gold transition-colors">
                  SAVED
                </Link>
              </>
            ) : (
              <>
                <Link to="/auth/sign-in" className="text-nes-white text-xs no-underline hover:text-nes-gold transition-colors">
                  LOGIN
                </Link>
                <Link to="/auth/sign-up" className="text-nes-gold text-xs no-underline border-2 border-nes-gold px-3 py-1 hover:bg-nes-gold hover:text-nes-black transition-colors">
                  SIGN UP
                </Link>
              </>
            )}
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
