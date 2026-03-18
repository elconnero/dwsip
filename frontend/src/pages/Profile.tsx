import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';

interface ProfileData {
  user_id:        string;
  email:          string | null;
  saved_games:    number;
  total_searches: number;
  requests_today: number;
  daily_limit:    number;
}

function Profile() {
  const { token, isLoggedIn, loading: authLoading } = useAuth();
  const [profile, setProfile]   = useState<ProfileData | null>(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState('');

  useEffect(() => {
    if (authLoading) return;
    if (!isLoggedIn) {
      setLoading(false);
      return;
    }
    fetchProfile();
  }, [authLoading, isLoggedIn]);

  async function fetchProfile() {
    try {
      const { data } = await api.get('/profile', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProfile(data);
    } catch {
      setError('COULD NOT LOAD PROFILE.');
    } finally {
      setLoading(false);
    }
  }

  if (authLoading || loading) return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />
      <main className="flex flex-col items-center py-16"><LoadingSpinner /></main>
    </div>
  );

  if (!isLoggedIn) return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />
      <main className="flex flex-col items-center gap-6 py-16">
        <p className="text-nes-red text-xs">YOU MUST BE LOGGED IN.</p>
        <Link to="/auth/sign-in" className="text-nes-gold text-xs border-4 border-nes-gold px-6 py-4 hover:bg-nes-gold hover:text-nes-black transition-colors">
          ▶ LOGIN
        </Link>
      </main>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />

      <main className="flex flex-col items-center px-6 py-16 gap-10 flex-1">
        <h1 className="text-nes-gold text-xl">PROFILE</h1>

        {error && <p className="text-nes-red text-xs">{error}</p>}

        {profile && (
          <div className="w-full max-w-lg flex flex-col gap-6">

            {/* User Info */}
            <div className="border-4 border-nes-gold bg-nes-black p-6 flex flex-col gap-4">
              <h2 className="text-nes-white text-xs">ACCOUNT</h2>
              <p className="text-nes-gray text-xs leading-loose">
                EMAIL: <span className="text-nes-white">{profile.email ?? 'N/A'}</span>
              </p>
            </div>

            {/* Stats */}
            <div className="border-4 border-nes-gold bg-nes-black p-6 flex flex-col gap-4">
              <h2 className="text-nes-white text-xs">STATS</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <p className="text-nes-gray text-xs">SAVED GAMES</p>
                  <p className="text-nes-gold text-xl">{profile.saved_games}</p>
                </div>
                <div className="flex flex-col gap-2">
                  <p className="text-nes-gray text-xs">TOTAL SEARCHES</p>
                  <p className="text-nes-gold text-xl">{profile.total_searches}</p>
                </div>
              </div>
            </div>

            {/* Daily Usage */}
            <div className="border-4 border-nes-gold bg-nes-black p-6 flex flex-col gap-4">
              <h2 className="text-nes-white text-xs">TODAY'S USAGE</h2>
              <p className="text-nes-gray text-xs leading-loose">
                {profile.requests_today} / {profile.daily_limit} SEARCHES USED
              </p>
              <div className="w-full bg-nes-gray h-2">
                <div
                  className="bg-nes-gold h-2 transition-all"
                  style={{ width: `${(profile.requests_today / profile.daily_limit) * 100}%` }}
                />
              </div>
            </div>

            {/* Quick Links */}
            <div className="flex gap-4">
              <Link
                to="/saved"
                className="flex-1 text-center border-4 border-nes-gold text-nes-gold text-xs py-4 hover:bg-nes-gold hover:text-nes-black transition-colors"
              >
                SAVED GAMES
              </Link>
              <Link
                to="/"
                className="flex-1 text-center border-4 border-nes-white text-nes-white text-xs py-4 hover:bg-nes-white hover:text-nes-black transition-colors"
              >
                FIND GAMES
              </Link>
            </div>

          </div>
        )}
      </main>
    </div>
  );
}

export default Profile;
