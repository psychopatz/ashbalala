import React, { useState, useEffect, useRef } from 'react';
import styled from '@emotion/styled';
import { ThemeProvider } from '@mui/material/styles';
import { Typography, Alert, Container } from '@mui/material';
import { theme } from './theme/theme';
import VoiceFilters from './components/VoiceFilters';
import VoiceSelector from './components/VoiceSelector';
import TextInput from './components/TextInput';
import AudioPlayer from './components/AudioPlayer';
import { TTSService } from './services/api';
import { base64ToBlob } from './utils/audioUtils';

const StyledContainer = styled(Container)`
  padding-top: 2rem;
  padding-bottom: 2rem;
`;

const TTSApp = () => {
  const [text, setText] = useState('');
  const [voices, setVoices] = useState({});
  const [selectedVoice, setSelectedVoice] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [audio, setAudio] = useState(null);
  const [audioPlaying, setAudioPlaying] = useState(false);
  const [filters, setFilters] = useState({
    locale: '',
    gender: '',
    neural: true,
  });
  const [customization, setCustomization] = useState({
    rate: 0,
    pitch: 0,
    style: 'neutral',
  });

  const audioRef = useRef(null);

  const fetchVoices = async () => {
    try {
      setError(null);
      const voices = await TTSService.getVoices(filters);
      setVoices(voices);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchVoices();
  }, []);

  const handleSynthesis = async () => {
    try {
      setLoading(true);
      setError(null);

      const audioBase64 = await TTSService.synthesizeSpeech({
        text,
        voice: selectedVoice,
        rate: customization.rate,
        pitch: customization.pitch,
        style: customization.style,
      });
      
      const audioBlob = base64ToBlob(audioBase64, 'audio/mp3');
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudio(audioUrl);
      
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (audioPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setAudioPlaying(!audioPlaying);
    }
  };

  const handleDownload = () => {
    if (audio) {
      const a = document.createElement('a');
      a.href = audio;
      a.download = 'synthesized_speech.mp3';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <StyledContainer maxWidth="lg">
        <Typography variant="h3" gutterBottom>
          Text to Speech Synthesizer
        </Typography>

        <VoiceFilters 
          filters={filters}
          setFilters={setFilters}
          onRefresh={fetchVoices}
        />

        <VoiceSelector
          voices={voices}
          selectedVoice={selectedVoice}
          onVoiceSelect={setSelectedVoice}
        />

        <TextInput
          text={text}
          setText={setText}
          customization={customization}
          setCustomization={setCustomization}
          onSynthesize={handleSynthesis}
          loading={loading}
          disabled={!text || !selectedVoice}
        />

        {audio && (
          <AudioPlayer
            audioRef={audioRef}
            audioPlaying={audioPlaying}
            onPlayPause={handlePlayPause}
            onDownload={handleDownload}
          />
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </StyledContainer>
    </ThemeProvider>
  );
};

export default TTSApp;