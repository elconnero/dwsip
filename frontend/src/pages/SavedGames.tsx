import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../services/api';
import { getToken } from '../lib/auth';
import type { GameResult } from '../types';

function SavedGames() {
  const [games, setGames]     = useState<GameResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState('');

  useEffect(() => {
    fetchSaved();
  }, []);

  async function fetchSaved() {
    try {
      const token = await getToken();
      if (!token) {
        setError('YOU MUST BE LOGGED IN TO VIEW SAVED GAMES.');
        setLoading(false);
        return;
      }
      const { data } = await api.get('/saved-games', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setGames(data);
    } catch {
      setError('COULD NOT LOAD SAVED GAMES.');
    } finally {
      setLoading(false);
    }
  }

  async function handleRemove(rawgId: number) {
    try {
      const token = await getToken();
      await api.delete(`/saved-games/${rawgId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setGames(prev => prev.filter(g => g.id !== rawgId));
    } catch {
      setError('COULD NOT REMOVE GAME.');
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />

      <main className="flex flex-col items-center px-6 py-16 gap-12 flex-1">
        <h1 className="text-nes-gold text-xl leading-loose">SAVED GAMES</h1>

        {loading && <LoadingSpinner />}

        {error && (
          <p className="text-nes-red text-xs border-4 border-nes-red px-6 py-4">{error}</p>
        )}

        {!loading && !error && games.length === 0 && (
          <div className="text-center flex flex-col gap-6">
            <p className="text-nes-gray text-xs leading-loose">NO SAVED GAMES YET.</p>
            <Link
              to="/"
              className="text-nes-gold text-xs border-4 border-nes-gold px-6 py-4 hover:bg-nes-gold hover:text-nes-black transition-colors"
            >
              ▶ FIND SOME GAMES
            </Link>
          </div>
        )}

        {games.length > 0 && (
          <div className="w-full max-w-5xl grid grid-cols-1 sm:grid-cols-3 gap-6">
            {games.map(game => (
              <div key={game.id} className="border-4 border-nes-gold bg-nes-black flex flex-col overflow-hidden">
                {game.background_image ? (
                  <img src={game.background_image} alt={game.name} className="w-full h-40 object-cover" />
                ) : (
                  <div className="w-full h-40 bg-nes-gray flex items-center justify-center text-xs">NO IMAGE</div>
                )}
                <div className="p-4 flex flex-col gap-3 flex-1">
                  <h2 className="text-nes-gold text-xs leading-relaxed">{game.name}</h2>
                  {game.metacritic && (
                    <p className="text-nes-blue text-xs">META: {game.metacritic}</p>
                  )}
                  <button
                    onClick={() => handleRemove(game.id)}
                    className="mt-auto w-full border-2 border-nes-red text-nes-red text-xs py-2 hover:bg-nes-red hover:text-nes-black transition-colors cursor-pointer"
                  >
                    ✕ REMOVE
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default SavedGames;
