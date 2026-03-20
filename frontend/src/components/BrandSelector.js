import React from 'react';
import './BrandSelector.css';

function BrandSelector({ brands, selectedBrand, onSelectBrand }) {
  return (
    <div className="brand-selector">
      <label>Select Brand:</label>
      {brands.length > 0 ? (
        <select
          value={selectedBrand}
          onChange={(e) => onSelectBrand(e.target.value)}
          className="select-input"
        >
          <option value="">Choose a brand...</option>
          {brands.map((brand) => (
            <option key={brand} value={brand}>
              {brand}
            </option>
          ))}
        </select>
      ) : (
        <div className="no-brands">
          <p>No brands available. Add a brand to get started!</p>
        </div>
      )}
    </div>
  );
}

export default BrandSelector;
