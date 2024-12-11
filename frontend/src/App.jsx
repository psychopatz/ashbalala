// App.js
import React, { useState } from 'react';
import EpubExtractor from './components/EpubExtractor';
import EpubViewer from './components/EpubViewer';


const App = () => {
  const [content, setContent] = useState([]);
  console.log(content);

  const handleExtract = (extractedContent) => {
    setContent(extractedContent);
  };

  return (
    <div>
      <EpubExtractor onExtract={handleExtract} />
      <EpubViewer content={content} />
    </div>
  );
};

export default App;
