import React from 'react';

function ProductList({
  products,
  loading,
  searchQuery,
  sortBy,
  priceFilter,
  onSortChange,
  onPriceChange,
  onProductClick,
}) {
  return (
    <section className="products-section">
      <div className="container">
        <div className="section-header">
          <h2>Search Results for "{searchQuery}"</h2>
          <div className="sort-options">
            <button
              className={`sort-btn ${sortBy === 'relevant' ? 'active' : ''}`}
              onClick={() => onSortChange('relevant')}
            >
              Relevant
            </button>
            <button
              className={`sort-btn ${sortBy === 'price-low' ? 'active' : ''}`}
              onClick={() => onSortChange('price-low')}
            >
              Price: Low to High
            </button>
            <button
              className={`sort-btn ${sortBy === 'price-high' ? 'active' : ''}`}
              onClick={() => onSortChange('price-high')}
            >
              Price: High to Low
            </button>
            <button
              className={`sort-btn ${sortBy === 'rating' ? 'active' : ''}`}
              onClick={() => onSortChange('rating')}
            >
              Highest Rating
            </button>
          </div>
        </div>

        <div className="products-container">
          <aside className="filters-sidebar">
            <div className="filter-group">
              <h3>Price Range</h3>
              <input
                type="range"
                min="0"
                max="100000"
                value={priceFilter}
                onChange={(e) => onPriceChange(e.target.value)}
                className="range-slider"
              />
              <div className="price-display">
                ₹0 - ₹{priceFilter.toLocaleString()}
              </div>
            </div>

            <div className="filter-group">
              <h3>Rating</h3>
              <label>
                <input type="checkbox" /> 4★ & Above
              </label>
              <label>
                <input type="checkbox" /> 3★ & Above
              </label>
            </div>

            <div className="filter-group">
              <h3>Availability</h3>
              <label>
                <input type="checkbox" /> In Stock
              </label>
              <label>
                <input type="checkbox" /> Out of Stock
              </label>
            </div>
          </aside>

          <div className="products-grid">
            {loading ? (
              <div className="loading">⏳ Loading products...</div>
            ) : products.length > 0 ? (
              products.map((product) => (
                <div
                  key={product.id}
                  className="product-card"
                  onClick={() => onProductClick(product)}
                >
                  <div className="product-image">
                    <img src={product.image_url} alt={product.name} />
                  </div>
                  <div className="product-info">
                    <h3>{product.name}</h3>
                    <div className="product-details">
                      <span className="price">{product.price}</span>
                      <span className="rating">⭐ {product.rating}</span>
                    </div>
                    <div className="review-count">({product.reviews} reviews)</div>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-products">
                No products found. Try a different search!
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

export default ProductList;
