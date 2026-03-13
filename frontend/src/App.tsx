import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Auth from './pages/Auth';
import SavedGames from './pages/SavedGames';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Auth />} />
      <Route path="/signup" element={<Auth />} />
      <Route path="/auth/sign-up" element={<Auth />} />
      <Route path="/auth/sign-in" element={<Auth />} />
      <Route path="/saved" element={<SavedGames />} />
    </Routes>
  );
}

export default App;
