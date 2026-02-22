import React from 'react';

function Categories({ categories, onCategoryClick }) {
  return (
    <section className="categories-section">
      <div className="container">
        <h2>Shop by Category</h2>
        <div className="categories-grid">
          {categories.map((category) => (
            <div
              key={category.id}
              className="category-card"
              onClick={() => onCategoryClick(category.name)}
            >
              <div className="category-icon">{category.icon}</div>
              <div className="category-name">{category.name}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Categories;
