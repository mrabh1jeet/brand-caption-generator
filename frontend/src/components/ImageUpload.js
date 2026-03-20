import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import './ImageUpload.css';

function ImageUpload({ onImageSelect }) {
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      onImageSelect(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, [onImageSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    multiple: false
  });

  return (
    <div className="image-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <p className="preview-text">Click or drag to change image</p>
          </div>
        ) : (
          <div className="dropzone-content">
            <div className="upload-icon">📸</div>
            <p className="dropzone-text">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag & drop an image here, or click to select'}
            </p>
            <p className="dropzone-hint">Supports: PNG, JPG, JPEG, WEBP</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ImageUpload;
