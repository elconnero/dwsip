import type { GameResult } from '../types';

interface Props {
  game: GameResult;
  onSave?: (game: GameResult) => void;
  saved?: boolean;
}

function GameCard({ game, onSave, saved = false }: Props) {
  return (
    <div className="border-4 border-nes-gold bg-nes-black flex flex-col overflow-hidden hover:border-nes-white transition-colors">
      {game.background_image ? (
        <img
          src={game.background_image}
          alt={game.name}
          className="w-full aspect-video object-cover"
        />
      ) : (
        <div className="w-full aspect-video bg-nes-gray flex items-center justify-center text-nes-black text-xs">
          NO IMAGE
        </div>
      )}

      <div className="p-4 flex flex-col gap-3 flex-1">
        <h2 className="text-nes-gold text-xs leading-relaxed">{game.name}</h2>

        <div className="flex flex-col gap-2 text-xs mt-auto">
          {game.rating !== null && (
            <p className="text-nes-green">⭐ {game.rating?.toFixed(1)} / 5</p>
          )}
          {game.metacritic !== null && (
            <p className="text-nes-blue">META: {game.metacritic}</p>
          )}
          {game.released && (
            <p className="text-nes-gray">{game.released}</p>
          )}
        </div>

        {onSave && (
          <button
            onClick={() => onSave(game)}
            disabled={saved}
            className="mt-3 w-full border-2 border-nes-gold text-nes-gold text-xs py-2 hover:bg-nes-gold hover:text-nes-black transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            {saved ? '✓ SAVED' : '+ SAVE'}
          </button>
        )}
      </div>
    </div>
  );
}

export default GameCard;
