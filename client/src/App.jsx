import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [option, setOption] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleOptionChange = (event) => {
    setOption(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!selectedFile) {
      alert('Please select a file to upload.');
      return;
    }
    if (!option) {
      alert('Please select an option.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('type', option);

    axios
      .post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
        console.log(response)
        if (response.data.text) {
          setResult(response.data.text);
        }
        
        if (response.data.error) {
          setError(response.data.error);
        } else {
          setError('');
        }
        
        if (response.data.urls) {
          window.location.href = response.data.urls[0];
        }
      })
      .catch((error) => {
        console.error('There was an error uploading the file!', error);
        setResult('Error uploading file.');
      });
  };

  return (
    <div className='box'>
      <h1>img2url</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            <input type="file" onChange={handleFileChange} />
          </label>
        </div>

        <div style={{ marginTop: '20px' }}>
          <label>Select an option:</label>
          <div>
            <label>
              <input
                type="radio"
                value="text"
                checked={option === 'text'}
                onChange={handleOptionChange}
              />
              Extract Text
            </label>
          </div>
          <div>
            <label>
              <input
                type="radio"
                value="url"
                checked={option === 'url'}
                onChange={handleOptionChange}
              />
              Visit URL
            </label>
          </div>
        </div>

        <button type="submit" style={{ marginTop: '20px' }}>
          Submit
        </button>
      </form>

      {error && <div style={{ color: 'red', marginTop: '20px' }}>{error}</div>}

    {result && (
      <div style={{ marginTop: '20px' }}>
        <label>Output:</label>
        <textarea
          value={result}
          readOnly
          rows="10"
          cols="80"
          style={{ width: '100%' }}
        />
      </div>)}
    </div>
  );
}

export default App;
