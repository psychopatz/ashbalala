// EpubExtractor.js
import React, { useState } from 'react';
import { Box, Typography } from '@mui/material';
import ePub from 'epubjs';
import UploadButton from './UploadButton';

const EpubExtractor = ({ onExtract }) => {
  const [fileName, setFileName] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      const book = ePub(file);
      const extractedContent = [];
      await book.ready;
      const spine = book.spine;
      for (let i = 0; i < spine.items.length; i++) {
        const section = await spine.get(i).load(book.load.bind(book));
        extractedContent.push({
          page: i + 1,
          xHtml: section ? section.contents : '',
        });
      }
      onExtract(extractedContent);
    }
  };

  return (
    <Box textAlign="center" p={4}>
      <UploadButton handleFileChange={handleFileChange} fileName={fileName} />
    </Box>
  );
};

export default EpubExtractor;