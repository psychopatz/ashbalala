import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const TTSService = {
  getVoices: async (filters) => {
    const queryParams = new URLSearchParams({
      ...filters,
      neural: filters.neural.toString(),
    }).toString();
    
    try {
      const { data } = await api.get(`/voices?${queryParams}`);
      return data.voices_by_locale;
    } catch (error) {
      throw new Error('Failed to fetch voices');
    }
  },

  synthesizeSpeech: async (params) => {
    try {
      const { data } = await api.post('/tts', {
        text: params.text,
        voice: params.voice,
        rate: `${params.rate}%`,
        pitch: `${params.pitch}Hz`,
        style: params.style,
      });
      
      return data.audio_base64;
    } catch (error) {
      throw new Error('Failed to synthesize speech');
    }
  },
};