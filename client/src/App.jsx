import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import Axios

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);

  // Handle file selection from the computer
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file);
      setError(null); // Clear previous errors
    }
  };

  // Handle image paste from the clipboard
  const handlePaste = (event) => {
    const items = event.clipboardData.items;
    for (let item of items) {
      if (item.type.indexOf('image') !== -1) {
        const blob = item.getAsFile();
        setImageFile(blob);
        setError(null); // Clear previous errors
        break;
      }
    }
  };

  // Send the image to the API when imageFile changes
  useEffect(() => {
    if (imageFile) {
      const formData = new FormData();
      formData.append('file', imageFile);

      // Use Axios to send the form data as multipart/form-data
      axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((response) => {
          setApiResponse(response.data);
          setError(null); // Clear previous errors
        })
        .catch((error) => {
          console.error('Error:', error);
          setError('Failed to upload image. Please try again.');
        });
    }
  }, [imageFile]);

  // Add event listener for paste events
  useEffect(() => {
    window.addEventListener('paste', handlePaste);
    return () => {
      window.removeEventListener('paste', handlePaste);
    };
  }, []);

  return (
    <div>
      <h1>Image Upload App</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <p>Or paste an image from the clipboard.</p>

      {/* Display error message */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Display API response */}
      {apiResponse && (
        <div>
          <h2>API Response:</h2>
          <pre>{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
