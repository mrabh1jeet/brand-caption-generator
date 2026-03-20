import React, { useState } from 'react';
import './CaptionDisplay.css';

function CaptionDisplay({ result }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const fullCaption = `${result.final_caption}\n\n${result.hashtags.join(' ')}${
      result.mentions.length > 0 ? '\n' + result.mentions.join(' ') : ''
    }`;
    
    navigator.clipboard.writeText(fullCaption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="caption-display">
      <h2>✨ Generated Caption</h2>
      
      <div className="caption-section">
        <h3>Base Caption (Image Description)</h3>
        <div className="caption-box base-caption">
          {result.base_caption}
        </div>
      </div>

      <div className="caption-section">
        <h3>Final Brand-Aligned Caption</h3>
        <div className="caption-box final-caption">
          {result.final_caption}
        </div>
      </div>

      {result.hashtags && result.hashtags.length > 0 && (
        <div className="caption-section">
          <h3>Hashtags</h3>
          <div className="tags-box">
            {result.hashtags.map((tag, index) => (
              <span key={index} className="tag hashtag">
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}

      {result.mentions && result.mentions.length > 0 && (
        <div className="caption-section">
          <h3>Mentions</h3>
          <div className="tags-box">
            {result.mentions.map((mention, index) => (
              <span key={index} className="tag mention">
                {mention}
              </span>
            ))}
          </div>
        </div>
      )}

      <button
        className="btn-copy"
        onClick={handleCopy}
      >
        {copied ? '✓ Copied!' : '📋 Copy Full Caption'}
      </button>
    </div>
  );
}

export default CaptionDisplay;
