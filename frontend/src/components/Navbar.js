import React from 'react';

function Navbar({ onSearch }) {
  const [searchQuery, setSearchQuery] = React.useState('');

  const handleSearch = () => {
    if (searchQuery.trim()) {
      onSearch(searchQuery);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <header className="navbar">
      <div className="navbar-container">
        <div className="logo">
          <h1>🛍️ ECommerce</h1>
        </div>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Search for products, brands and more..."
            className="search-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button className="search-btn" onClick={handleSearch}>
            Search
          </button>
        </div>

        <div className="nav-icons">
          <div className="icon-item">
            <span className="icon">🏠</span>
            <span className="icon-label">Home</span>
          </div>
          <div className="icon-item">
            <span className="icon">❤️</span>
            <span className="icon-label">Wishlist</span>
          </div>
          <div className="icon-item">
            <span className="icon">🛒</span>
            <span className="icon-label">Cart</span>
          </div>
          <div className="icon-item">
            <span className="icon">👤</span>
            <span className="icon-label">Account</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
