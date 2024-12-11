// UploadButton.js
import React from 'react';
import { Button } from '@mui/material';

const UploadButton = ({ handleFileChange, fileName }) => {
  return (
    <div>
      <input
        type="file"
        accept=".epub"
        style={{ display: 'none' }}
        id="epub-upload"
        onChange={handleFileChange}
      />
      <label htmlFor="epub-upload">
        <Button variant="contained" component="span">
          {fileName ? `Selected: ${fileName}` : 'Upload EPUB File'}
        </Button>
      </label>
    </div>
  );
};

export default UploadButton;