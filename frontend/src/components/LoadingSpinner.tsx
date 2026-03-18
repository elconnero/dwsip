function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center gap-6 py-12">
      <div className="w-12 h-12 border-4 border-nes-gray border-t-nes-gold animate-spin" />
      <p className="text-nes-gold text-xs animate-pulse">LOADING...</p>
    </div>
  );
}

export default LoadingSpinner;
