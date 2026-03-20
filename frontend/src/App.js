import React, { useState, useEffect } from 'react';
import './App.css';
import ImageUpload from './components/ImageUpload';
import BrandSelector from './components/BrandSelector';
import CaptionDisplay from './components/CaptionDisplay';
import AddBrand from './components/AddBrand';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [brands, setBrands] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState('');
  const [personality, setPersonality] = useState('excitement');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showAddBrand, setShowAddBrand] = useState(false);

  const personalities = [
    'sincerity',
    'excitement',
    'competence',
    'sophistication',
    'ruggedness'
  ];

  // Fetch available brands on mount
  useEffect(() => {
    fetchBrands();
  }, []);

  const fetchBrands = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/brands`);
      if (response.data.success) {
        setBrands(response.data.brands);
      }
    } catch (err) {
      console.error('Error fetching brands:', err);
    }
  };

  const handleGenerateCaption = async () => {
    if (!selectedBrand) {
      setError('Please select a brand');
      return;
    }

    if (!image) {
      setError('Please upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('brand_name', selectedBrand);
      formData.append('personality', personality);

      const response = await axios.post(
        `${API_URL}/api/caption/generate`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.error || 'Failed to generate caption');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error generating caption');
    } finally {
      setLoading(false);
    }
  };

  const handleAddBrand = (newBrand) => {
    setBrands([...brands, newBrand]);
    setShowAddBrand(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎨 Brand Caption Generator</h1>
        <p>RAG-Enhanced Social Media Caption Generation</p>
      </header>

      <main className="App-main">
        {!showAddBrand ? (
          <>
            <div className="controls-section">
              <BrandSelector
                brands={brands}
                selectedBrand={selectedBrand}
                onSelectBrand={setSelectedBrand}
              />

              <div className="personality-selector">
                <label>Brand Personality:</label>
                <select
                  value={personality}
                  onChange={(e) => setPersonality(e.target.value)}
                  className="select-input"
                >
                  {personalities.map((p) => (
                    <option key={p} value={p}>
                      {p.charAt(0).toUpperCase() + p.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <button
                className="btn-secondary"
                onClick={() => setShowAddBrand(true)}
              >
                + Add New Brand
              </button>
            </div>

            <ImageUpload onImageSelect={setImage} />

            <button
              className="btn-primary"
              onClick={handleGenerateCaption}
              disabled={loading || !selectedBrand || !image}
            >
              {loading ? 'Generating...' : 'Generate Caption'}
            </button>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}

            {result && <CaptionDisplay result={result} />}
          </>
        ) : (
          <AddBrand
            onAddBrand={handleAddBrand}
            onCancel={() => setShowAddBrand(false)}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by BLIP-2, ChromaDB & Google Gemini</p>
      </footer>
    </div>
  );
}

export default App;
