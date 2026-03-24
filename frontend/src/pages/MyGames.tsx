import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';
import { getToken } from '../lib/auth';
import { useAuth } from '../hooks/useAuth';

interface SavedGame {
  id: number;
  rawg_id: number;
  name: string;
  background_image: string | null;
  metacritic: number | null;
}

interface MyGameItem {
  rawg_id: number;
  name: string;
  background_image: string | null;
}

interface MyRecommendation {
  id: number;
  user_prompt: string;
  created_at: string;
  games: MyGameItem[];
}

function MyGames() {
  const { isLoggedIn, loading } = useAuth();
  const [saved, setSaved]       = useState<SavedGame[]>([]);
  const [recs, setRecs]         = useState<MyRecommendation[]>([]);
  const [fetching, setFetching] = useState(true);
  const [error, setError]       = useState('');

  useEffect(() => {
    if (loading) return;
    if (!isLoggedIn) { setFetching(false); return; }

    async function load() {
      try {
        const t = await getToken();
        const headers = { Authorization: `Bearer ${t}` };
        const [savedRes, recsRes] = await Promise.all([
          api.get<SavedGame[]>('/saved-games', { headers }),
          api.get<MyRecommendation[]>('/my-games', { headers }),
        ]);
        setSaved(savedRes.data);
        setRecs(recsRes.data.slice(0, 10));
      } catch {
        setError('COULD NOT LOAD DATA. TRY AGAIN.');
      } finally {
        setFetching(false);
      }
    }
    load();
  }, [isLoggedIn, loading]);

  async function handleRemove(rawgId: number) {
    try {
      const t = await getToken();
      await api.delete(`/saved-games/${rawgId}`, {
        headers: { Authorization: `Bearer ${t}` },
      });
      setSaved(prev => prev.filter(g => g.rawg_id !== rawgId));
    } catch {
      setError('COULD NOT REMOVE GAME.');
    }
  }

  if (!loading && !isLoggedIn) {
    return (
      <div className="min-h-screen flex flex-col bg-nes-dark">
        <Navbar />
        <main className="flex flex-col items-center px-6 py-16 gap-4 flex-1">
          <p className="text-nes-white text-xs leading-loose">YOU MUST BE LOGGED IN TO VIEW THIS PAGE.</p>
          <Link to="/auth/sign-in" className="text-nes-gold text-xs border-4 border-nes-gold px-6 py-3 hover:bg-nes-gold hover:text-nes-black transition-colors">
            ▶ LOGIN
          </Link>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />

      <main className="flex flex-col items-center px-6 py-16 gap-16 flex-1">

        {error && <p className="text-nes-red text-xs border-4 border-nes-red px-6 py-4">{error}</p>}

        {/* ── SAVED GAMES ── */}
        <section className="w-full max-w-5xl flex flex-col gap-6">
          <h2 className="text-nes-gold text-lg text-center">— SAVED GAMES —</h2>

          {fetching && <p className="text-nes-white text-xs text-center">LOADING...</p>}

          {!fetching && saved.length === 0 && (
            <p className="text-nes-gray text-xs text-center leading-loose">NO SAVED GAMES YET.</p>
          )}

          {saved.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {saved.map(game => (
                <div key={game.rawg_id} className="border-4 border-nes-gold bg-nes-black flex flex-col overflow-hidden">
                  {game.background_image
                    ? <img src={game.background_image} alt={game.name} className="w-full aspect-video object-cover" />
                    : <div className="w-full aspect-video bg-nes-gray flex items-center justify-center text-xs text-nes-white">NO IMAGE</div>
                  }
                  <div className="p-4 flex flex-col gap-3 flex-1">
                    <p className="text-nes-gold text-xs leading-relaxed">{game.name}</p>
                    {game.metacritic && (
                      <p className="text-nes-blue text-xs">META: {game.metacritic}</p>
                    )}
                    <button
                      onClick={() => handleRemove(game.rawg_id)}
                      className="mt-auto w-full border-2 border-nes-red text-nes-red text-xs py-2 hover:bg-nes-red hover:text-nes-black transition-colors cursor-pointer"
                    >
                      ✕ REMOVE
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* ── RECENT SEARCHES ── */}
        <section className="w-full max-w-5xl flex flex-col gap-6">
          <h2 className="text-nes-gold text-lg text-center">— RECENT SEARCHES —</h2>

          {fetching && <p className="text-nes-white text-xs text-center">LOADING...</p>}

          {!fetching && recs.length === 0 && (
            <p className="text-nes-gray text-xs text-center leading-loose">NO SEARCHES YET.</p>
          )}

          {recs.map(rec => (
            <div key={rec.id} className="w-full border-4 border-nes-gold bg-nes-black flex flex-row items-center gap-4 p-4">
              {/* Prompt + date */}
              <div className="flex flex-col gap-2 w-48 shrink-0">
                <p className="text-nes-gold text-xs leading-loose">"{rec.user_prompt}"</p>
                <p className="text-nes-gray text-xs">{new Date(rec.created_at).toLocaleDateString()}</p>
              </div>

              {/* Divider */}
              <div className="w-px self-stretch bg-nes-gold opacity-30 shrink-0" />

              {/* Games */}
              <div className="flex flex-row gap-3 flex-1">
                {rec.games.map(game => (
                  <div key={game.rawg_id} className="flex flex-col border-2 border-nes-gold overflow-hidden flex-1">
                    {game.background_image
                      ? <img src={game.background_image} alt={game.name} className="w-full aspect-video object-cover" />
                      : <div className="w-full h-20 bg-nes-gray flex items-center justify-center text-xs text-nes-white">NO IMAGE</div>
                    }
                    <p className="text-nes-white text-xs p-2 leading-loose">{game.name}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </section>

      </main>
    </div>
  );
}

export default MyGames;
