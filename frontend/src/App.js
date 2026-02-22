import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Navbar from './components/Navbar';
import Categories from './components/Categories';
import ProductList from './components/ProductList';
import ProductModal from './components/ProductModal';

const API_URL = 'http://localhost:8000/api';

function App() {
  const [products, setProducts] = useState([]);
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('electronics');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [sortBy, setSortBy] = useState('relevant');
  const [priceFilter, setPriceFilter] = useState(100000);

  // Fetch categories
  useEffect(() => {
    fetchCategories();
    fetchTrendingProducts();
    fetchProducts(searchQuery);
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/categories`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTrendingProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/trending`);
      setTrendingProducts(response.data.trending);
    } catch (error) {
      console.error('Error fetching trending products:', error);
    }
  };

  const fetchProducts = async (query = searchQuery) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/search`, {
        params: { q: query, limit: 24 }
      });
      let productsData = response.data.products;
      
      // Apply filters and sorting
      productsData = applyFilters(productsData);
      productsData = applySorting(productsData);
      
      setProducts(productsData);
      setSearchQuery(query);
    } catch (error) {
      console.error('Error fetching products:', error);
      // Show error notification
      alert('Error fetching products. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = (productsData) => {
    return productsData.filter(product => {
      // Extract price as number
      const priceStr = product.price.replace(/[^\d]/g, '');
      const price = parseInt(priceStr) || 0;
      
      if (price > priceFilter) {
        return false;
      }
      
      return true;
    });
  };

  const applySorting = (productsData) => {
    const sorted = [...productsData];
    
    switch (sortBy) {
      case 'price-low':
        sorted.sort((a, b) => {
          const priceA = parseInt(a.price.replace(/[^\d]/g, '')) || 0;
          const priceB = parseInt(b.price.replace(/[^\d]/g, '')) || 0;
          return priceA - priceB;
        });
        break;
      case 'price-high':
        sorted.sort((a, b) => {
          const priceA = parseInt(a.price.replace(/[^\d]/g, '')) || 0;
          const priceB = parseInt(b.price.replace(/[^\d]/g, '')) || 0;
          return priceB - priceA;
        });
        break;
      case 'rating':
        sorted.sort((a, b) => {
          const ratingA = parseFloat(a.rating) || 0;
          const ratingB = parseFloat(b.rating) || 0;
          return ratingB - ratingA;
        });
        break;
      case 'relevant':
      default:
        // Default order
        break;
    }
    
    return sorted;
  };

  const handleSearch = (query) => {
    if (query.trim()) {
      fetchProducts(query);
    }
  };

  const handleCategoryClick = (categoryName) => {
    fetchProducts(categoryName.toLowerCase());
  };

  const handleSortChange = (sortOption) => {
    setSortBy(sortOption);
    let productsData = products;
    productsData = applySorting(productsData);
    setProducts([...productsData]);
  };

  const handlePriceChange = (value) => {
    setPriceFilter(value);
    let productsData = products;
    productsData = applyFilters(productsData);
    productsData = applySorting(productsData);
    setProducts([...productsData]);
  };

  return (
    <div className="App">
      <Navbar onSearch={handleSearch} />
      <Categories categories={categories} onCategoryClick={handleCategoryClick} />
      
      {/* Trending Section */}
      {trendingProducts.length > 0 && (
        <section className="featured-section">
          <div className="container">
            <h2>🔥 Trending Now</h2>
            <div className="products-grid">
              {trendingProducts.map((product) => (
                <div
                  key={product.id}
                  className="product-card"
                  onClick={() => setSelectedProduct(product)}
                >
                  <div className="product-image">
                    <img src={product.image_url} alt={product.name} />
                  </div>
                  <div className="product-info">
                    <h3>{product.name}</h3>
                    <div className="product-rating">
                      <span>⭐ {product.rating}</span>
                      <span>({product.reviews})</span>
                    </div>
                    <div className="product-price">{product.price}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Main Products Section */}
      <ProductList
        products={products}
        loading={loading}
        searchQuery={searchQuery}
        sortBy={sortBy}
        priceFilter={priceFilter}
        onSortChange={handleSortChange}
        onPriceChange={handlePriceChange}
        onProductClick={(product) => setSelectedProduct(product)}
      />

      {/* Product Modal */}
      {selectedProduct && (
        <ProductModal
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
        />
      )}
    </div>
  );
}

export default App;
