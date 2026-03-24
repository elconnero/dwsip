export interface GameFilters {
  genres:          string[];
  tags:            string[];
  mood:            string;
  multiplayer:     boolean;
  platforms:       string[];
  search_query:    string;
  predicted_game:  string | null;
}

export interface GameResult {
  id:               number;
  name:             string;
  background_image: string | null;
  rating:           number | null;
  metacritic:       number | null;
  released:         string | null;
}
