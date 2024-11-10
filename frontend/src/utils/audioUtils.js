// src/utils/audioUtils.js
export const base64ToBlob = (base64, type) => {
  const byteCharacters = atob(base64);
  const byteArray = new Uint8Array(byteCharacters.length);
  
  for (let i = 0; i < byteCharacters.length; i++) {
    byteArray[i] = byteCharacters.charCodeAt(i);
  }
  
  return new Blob([byteArray], { type });
};