import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload, FileText, Download } from 'lucide-react';
import JSZip from 'jszip';

const EpubConverter = () => {
  const [converting, setConverting] = useState(false);
  const [status, setStatus] = useState('');
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setConverting(true);
      setStatus('Reading EPUB file...');
      
      // Read the EPUB file (which is essentially a ZIP file)
      const zip = new JSZip();
      const epubContent = await file.arrayBuffer();
      const epub = await zip.loadAsync(epubContent);
      
      setStatus('Processing EPUB content...');
      
      // Create a new ZIP to store XHTML files
      const outputZip = new JSZip();
      
      // Process each file in the EPUB
      for (const [path, zipEntry] of Object.entries(epub.files)) {
        if (path.endsWith('.html') || path.endsWith('.xhtml')) {
          // Get the content of HTML/XHTML files
          const content = await zipEntry.async('string');
          
          // Convert to XHTML if needed
          const xhtmlContent = convertToXHTML(content);
          
          // Store in the output ZIP
          const newPath = path.replace('.html', '.xhtml');
          outputZip.file(newPath, xhtmlContent);
        } else if (path.includes('images/') || path.includes('css/')) {
          // Copy images and CSS files as-is
          const content = await zipEntry.async('uint8array');
          outputZip.file(path, content);
        }
      }
      
      setStatus('Generating output file...');
      
      // Generate the output ZIP file
      const outputContent = await outputZip.generateAsync({
        type: 'blob',
        mimeType: 'application/zip'
      });
      
      // Create download URL
      const url = URL.createObjectURL(outputContent);
      setDownloadUrl(url);
      setStatus('Conversion complete!');
    } catch (error) {
      setStatus(`Error: ${error.message}`);
    } finally {
      setConverting(false);
    }
  };

  const convertToXHTML = (htmlContent) => {
    // Add XHTML doctype
    const doctype = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n';
    
    // Convert void elements to self-closing tags
    const xhtmlContent = htmlContent
      .replace(/<(img|br|hr|input|meta|link)([^>]*)>/gi, '<$1$2/>')
      .replace(/\s+>/g, '>');
    
    return doctype + xhtmlContent;
  };

  return (
    <Card className="w-full max-w-lg mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-6 h-6" />
          EPUB to XHTML Converter
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-col items-center gap-4">
          <label className="relative cursor-pointer">
            <input
              type="file"
              accept=".epub"
              onChange={handleFileUpload}
              className="hidden"
              disabled={converting}
            />
            <Button 
              variant="outline" 
              className="flex items-center gap-2"
              disabled={converting}
            >
              <Upload className="w-4 h-4" />
              Select EPUB File
            </Button>
          </label>
          
          {status && (
            <div className="text-sm text-gray-600">
              {status}
            </div>
          )}
          
          {downloadUrl && (
            <a
              href={downloadUrl}
              download="converted.zip"
              className="no-underline"
            >
              <Button className="flex items-center gap-2">
                <Download className="w-4 h-4" />
                Download Converted Files
              </Button>
            </a>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default EpubConverter;