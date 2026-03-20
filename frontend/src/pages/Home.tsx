import { useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import GameCard from '../components/GameCard';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../services/api';
import { getToken } from '../lib/auth';
import { useAuth } from '../hooks/useAuth';
import type { GameFilters, GameResult } from '../types';

const GUEST_REQUEST_KEY = 'guestRequestUsed';

function Home() {
  const { isLoggedIn } = useAuth();
  const [prompt, setPrompt]         = useState('');
  const [games, setGames]           = useState<GameResult[]>([]);
  const [savedIds, setSavedIds]     = useState<Set<number>>(new Set());
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState('');
  const [showSignupBanner, setShowSignupBanner] = useState(false);

  function guestRequestUsed(): boolean {
    return localStorage.getItem(GUEST_REQUEST_KEY) === 'true';
  }

  async function handleSearch() {
    if (!prompt.trim()) return;

    // Block guest if they already used their free request
    if (!isLoggedIn && guestRequestUsed()) {
      setShowSignupBanner(true);
      return;
    }

    setLoading(true);
    setError('');
    setGames([]);
    setShowSignupBanner(false);

    try {
      const { data: filters } = await api.post<GameFilters>('/prompt/parse', { prompt });
      const { data: results } = await api.post<GameResult[]>('/games/recommend', filters);
      setGames(results);

      // Mark guest request as used
      if (!isLoggedIn) {
        localStorage.setItem(GUEST_REQUEST_KEY, 'true');
        setShowSignupBanner(true);
      }
    } catch {
      setError('SOMETHING WENT WRONG. TRY AGAIN.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSave(game: GameResult) {
    try {
      const t = await getToken();
      if (!t) {
        setShowSignupBanner(true);
        return;
      }
      await api.post('/saved-games', {
        rawg_id:          game.id,
        name:             game.name,
        background_image: game.background_image,
        rating:           game.rating,
        metacritic:       game.metacritic,
        released:         game.released,
      }, {
        headers: { Authorization: `Bearer ${t}` },
      });
      setSavedIds(prev => new Set(prev).add(game.id));
    } catch {
      setError('COULD NOT SAVE GAME. TRY AGAIN.');
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) handleSearch();
  }

  return (
    <div className="min-h-screen flex flex-col bg-nes-dark">
      <Navbar />

      <main className="flex flex-col items-center px-6 py-16 gap-12 flex-1">

        {/* Title */}
        <div className="text-center flex flex-col gap-4">
          <h1 className="text-nes-gold text-2xl leading-loose">DWISP</h1>
          <p className="text-nes-white text-xs leading-loose">DUDE, WHAT SHOULD I PLAY?</p>
        </div>

        {/* Input */}
        <div className="w-full max-w-2xl flex flex-col gap-4">
          <textarea
            className="w-full bg-nes-black border-4 border-nes-gold text-nes-white text-xs p-4 leading-loose resize-none focus:outline-none focus:border-nes-white placeholder-nes-gray"
            rows={4}
            placeholder="DESCRIBE WHAT YOU WANT TO PLAY..."
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={handleSearch}
            disabled={loading || !prompt.trim()}
            className="w-full bg-nes-gold text-nes-black text-xs py-4 border-4 border-nes-gold hover:bg-nes-black hover:text-nes-gold transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? 'SEARCHING...' : '▶ FIND MY GAME'}
          </button>
        </div>

        {loading && <LoadingSpinner />}

        {error && (
          <p className="text-nes-red text-xs border-4 border-nes-red px-6 py-4">{error}</p>
        )}

        {/* Sign up banner */}
        {showSignupBanner && (
          <div className="w-full max-w-2xl border-4 border-nes-gold bg-nes-black p-6 flex flex-col gap-4 items-center text-center">
            <p className="text-nes-gold text-xs leading-loose">
              {!isLoggedIn && guestRequestUsed() && games.length === 0
                ? 'YOU HAVE USED YOUR FREE SEARCH.'
                : 'WANT UNLIMITED SEARCHES AND TO SAVE GAMES?'}
            </p>
            <p className="text-nes-white text-xs leading-loose">
              CREATE A FREE ACCOUNT TO KEEP PLAYING.
            </p>
            <Link
              to="/auth/sign-up"
              className="border-4 border-nes-gold text-nes-gold text-xs px-8 py-4 hover:bg-nes-gold hover:text-nes-black transition-colors"
            >
              ▶ CREATE ACCOUNT
            </Link>
          </div>
        )}

        {/* Results */}
        {games.length > 0 && (
          <div className="w-full max-w-5xl flex flex-col gap-6">
            <h2 className="text-nes-white text-xs text-center">— YOUR GAMES —</h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {games.map(game => (
                <GameCard
                  key={game.id}
                  game={game}
                  onSave={handleSave}
                  saved={savedIds.has(game.id)}
                />
              ))}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}

export default Home;
