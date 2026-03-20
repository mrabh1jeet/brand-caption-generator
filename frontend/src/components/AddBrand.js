import React, { useState } from 'react';
import axios from 'axios';
import './AddBrand.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function AddBrand({ onAddBrand, onCancel }) {
  const [brandName, setBrandName] = useState('');
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [instagramHandle, setInstagramHandle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!brandName || !websiteUrl) {
      setError('Brand name and website URL are required');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await axios.post(`${API_URL}/api/brands/add`, {
        brand_name: brandName,
        website_url: websiteUrl,
        instagram_handle: instagramHandle
      });

      if (response.data.success) {
        setSuccess(true);
        onAddBrand(brandName);
        setTimeout(() => {
          onCancel();
        }, 1500);
      } else {
        setError(response.data.error || 'Failed to add brand');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error adding brand');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-brand-container">
      <div className="add-brand-header">
        <h2>Add New Brand</h2>
        <button className="btn-close" onClick={onCancel}>
          ✕
        </button>
      </div>

      <form onSubmit={handleSubmit} className="add-brand-form">
        <div className="form-group">
          <label>Brand Name *</label>
          <input
            type="text"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            placeholder="e.g., Nike, Apple, Coca-Cola"
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label>Website URL *</label>
          <input
            type="url"
            value={websiteUrl}
            onChange={(e) => setWebsiteUrl(e.target.value)}
            placeholder="https://www.example.com"
            className="form-input"
            required
          />
        </div>

        <div className="form-group">
          <label>Instagram Handle (Optional)</label>
          <input
            type="text"
            value={instagramHandle}
            onChange={(e) => setInstagramHandle(e.target.value)}
            placeholder="@brandname"
            className="form-input"
          />
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            ✓ Brand added successfully!
          </div>
        )}

        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Adding Brand...' : 'Add Brand'}
          </button>
        </div>

        <div className="form-note">
          <p>
            ℹ️ The system will scrape the website and collect brand information
            to build the knowledge base. This may take a few moments.
          </p>
        </div>
      </form>
    </div>
  );
}

export default AddBrand;
