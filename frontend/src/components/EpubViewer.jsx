// EpubViewer.js
import React, { useState } from 'react';
import { Box, Typography, Pagination } from '@mui/material';

const EpubViewer = ({ content }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
  };

  return (
    <Box textAlign="center" p={4}>
      {content.length > 0 ? (
        <>
          <Box my={2}>
            <Typography
              variant="body1"
              component="pre"
              style={{ whiteSpace: 'pre-wrap', textAlign: 'left' }}
              dangerouslySetInnerHTML={{ __html: content[currentPage - 1].xHtml }}
            />
          </Box>
          <Pagination
            count={content.length}
            page={currentPage}
            onChange={handlePageChange}
            color="primary"
          />
        </>
      ) : (
        <Typography variant="body1">No content available</Typography>
      )}
    </Box>
  );
};

export default EpubViewer;