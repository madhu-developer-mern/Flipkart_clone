import React from 'react';

function ProductModal({ product, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <span className="close-btn" onClick={onClose}>
          ✕
        </span>
        <div className="modal-body">
          <div className="modal-image">
            <img src={product.image_url} alt={product.name} />
          </div>
          <div className="modal-details">
            <h2>{product.name}</h2>
            <div className="modal-rating">
              <span className="rating">⭐ {product.rating}</span>
              <span className="reviews">({product.reviews} customer reviews)</span>
            </div>
            <div className="modal-price">
              <h3>{product.price}</h3>
            </div>
            <div className="modal-actions">
              <button className="btn-primary">🛒 Add to Cart</button>
              <button className="btn-secondary">❤️ Add to Wishlist</button>
            </div>
            <div className="modal-info">
              <div className="info-item">
                <span className="info-icon">🚚</span>
                <div>
                  <strong>Free Delivery</strong>
                  <p>Free delivery available on this product</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">↩️</span>
                <div>
                  <strong>30 Day Return Policy</strong>
                  <p>Return within 30 days for a full refund</p>
                </div>
              </div>
              <div className="info-item">
                <span className="info-icon">🛡️</span>
                <div>
                  <strong>1 Year Warranty</strong>
                  <p>1 year manufacturer warranty included</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductModal;
