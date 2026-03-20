import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';
import { authClient, getToken } from '../lib/auth';
import { useAuth } from '../hooks/useAuth';

function Settings() {
  const { isLoggedIn, loading, email } = useAuth();
  const navigate = useNavigate();
  const [confirming, setConfirming] = useState(false);
  const [deleting, setDeleting]     = useState(false);
  const [error, setError]           = useState('');

  async function handleDeleteAccount() {
    setDeleting(true);
    setError('');
    try {
      const t = await getToken();
      await api.delete('/account', {
        headers: { Authorization: `Bearer ${t}` },
      });
      await authClient.signOut();
      navigate('/');
    } catch {
      setError('COULD NOT DELETE ACCOUNT. TRY AGAIN.');
      setDeleting(false);
    }
  }

  if (loading) return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />
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
        <h1 className="text-nes-gold text-xl">SETTINGS</h1>

        <div className="w-full max-w-lg flex flex-col gap-6">

          {/* Account Info */}
          <div className="border-4 border-nes-gold bg-nes-black p-6 flex flex-col gap-4">
            <h2 className="text-nes-white text-xs">ACCOUNT</h2>
            <p className="text-nes-gray text-xs leading-loose">
              EMAIL: <span className="text-nes-white">{email ?? 'N/A'}</span>
            </p>
          </div>

          {/* Danger Zone */}
          <div className="border-4 border-nes-red bg-nes-black p-6 flex flex-col gap-4">
            <h2 className="text-nes-red text-xs">DANGER ZONE</h2>

            {error && (
              <p className="text-nes-red text-xs">{error}</p>
            )}

            {!confirming ? (
              <button
                onClick={() => setConfirming(true)}
                className="w-full border-2 border-nes-red text-nes-red text-xs py-3 hover:bg-nes-red hover:text-nes-black transition-colors cursor-pointer"
              >
                DELETE ACCOUNT
              </button>
            ) : (
              <div className="flex flex-col gap-4">
                <p className="text-nes-white text-xs leading-loose">
                  ARE YOU SURE? THIS CANNOT BE UNDONE. ALL YOUR SAVED GAMES AND SEARCH HISTORY WILL BE DELETED.
                </p>
                <div className="flex gap-4">
                  <button
                    onClick={() => setConfirming(false)}
                    disabled={deleting}
                    className="flex-1 border-2 border-nes-white text-nes-white text-xs py-3 hover:bg-nes-white hover:text-nes-black transition-colors disabled:opacity-50 cursor-pointer"
                  >
                    ✕ CANCEL
                  </button>
                  <button
                    onClick={handleDeleteAccount}
                    disabled={deleting}
                    className="flex-1 border-2 border-nes-red bg-nes-red text-nes-black text-xs py-3 hover:opacity-80 transition-opacity disabled:opacity-50 cursor-pointer"
                  >
                    {deleting ? 'DELETING...' : '▶ DELETE'}
                  </button>
                </div>
              </div>
            )}
          </div>

        </div>
      </main>
    </div>
  );
}

export default Settings;
