import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Slider,
  CircularProgress,
  Alert,
  Grid,
  IconButton,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Download,
  Refresh,
  VolumeUp,
} from '@mui/icons-material';
import { ThemeProvider, createTheme } from '@mui/material/styles';

// Styled Components
const StyledContainer = styled(Container)`
  padding-top: 2rem;
  padding-bottom: 2rem;
`;

const StyledPaper = styled(Paper)`
  padding: 2rem;
  margin-bottom: 2rem;
`;

const StyledFormControl = styled(FormControl)`
  min-width: 200px;
  margin-bottom: 1rem;
`;

const AudioControls = styled(Box)`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
`;

const VoiceCard = styled(Paper)`
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
`;

// Theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Main Component
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

  // Audio player reference
  const audioRef = React.useRef(null);

  // Fetch voices on component mount
  useEffect(() => {
    fetchVoices();
  }, []);

  const fetchVoices = async () => {
    try {
      const queryParams = new URLSearchParams({
        ...filters,
        neural: filters.neural.toString(),
      }).toString();
      
      const response = await fetch(`http://localhost:8000/voices?${queryParams}`);
      const data = await response.json();
      setVoices(data.voices_by_locale);
    } catch (err) {
      setError('Failed to fetch voices');
    }
  };

  const handleSynthesis = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('http://localhost:8000/tts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          voice: selectedVoice,
          rate: `${customization.rate}%`,
          pitch: `${customization.pitch}Hz`,
          style: customization.style,
        }),
      });

      const data = await response.json();
      
      if (data.audio_base64) {
        const audioBlob = base64ToBlob(data.audio_base64, 'audio/mp3');
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudio(audioUrl);
        
        if (audioRef.current) {
          audioRef.current.src = audioUrl;
        }
      }
    } catch (err) {
      setError('Failed to synthesize speech');
    } finally {
      setLoading(false);
    }
  };

  const base64ToBlob = (base64, type) => {
    const byteCharacters = atob(base64);
    const byteArray = new Uint8Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteArray[i] = byteCharacters.charCodeAt(i);
    }
    
    return new Blob([byteArray], { type });
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

        {/* Filters Section */}
        <StyledPaper>
          <Typography variant="h6" gutterBottom>
            Voice Filters
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <StyledFormControl fullWidth>
                <InputLabel>Locale</InputLabel>
                <Select
                  value={filters.locale}
                  onChange={(e) => setFilters({ ...filters, locale: e.target.value })}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="en-US">English (US)</MenuItem>
                  <MenuItem value="en-GB">English (UK)</MenuItem>
                  {/* Add more locales as needed */}
                </Select>
              </StyledFormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <StyledFormControl fullWidth>
                <InputLabel>Gender</InputLabel>
                <Select
                  value={filters.gender}
                  onChange={(e) => setFilters({ ...filters, gender: e.target.value })}
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="Male">Male</MenuItem>
                  <MenuItem value="Female">Female</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                variant="contained"
                startIcon={<Refresh />}
                onClick={fetchVoices}
                fullWidth
              >
                Refresh Voices
              </Button>
            </Grid>
          </Grid>
        </StyledPaper>

        {/* Voice Selection */}
        <StyledPaper>
          <Typography variant="h6" gutterBottom>
            Available Voices
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(voices).map(([locale, voiceList]) => (
              <Grid item xs={12} key={locale}>
                <Typography variant="subtitle1" gutterBottom>
                  {locale}
                </Typography>
                <Grid container spacing={2}>
                  {voiceList.map((voice) => (
                    <Grid item xs={12} md={4} key={voice.name}>
                      <VoiceCard
                        onClick={() => setSelectedVoice(voice.name)}
                        elevation={selectedVoice === voice.name ? 8 : 1}
                      >
                        <Typography variant="h6">{voice.name}</Typography>
                        <Typography variant="body2">
                          {voice.gender} • {voice.type}
                        </Typography>
                        {voice.styles.length > 0 && (
                          <Typography variant="body2">
                            Styles: {voice.styles.join(', ')}
                          </Typography>
                        )}
                      </VoiceCard>
                    </Grid>
                  ))}
                </Grid>
              </Grid>
            ))}
          </Grid>
        </StyledPaper>

        {/* Text Input and Customization */}
        <StyledPaper>
          <Typography variant="h6" gutterBottom>
            Text Input
          </Typography>
          <TextField
            fullWidth
            multiline
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to synthesize..."
            variant="outlined"
            margin="normal"
          />

          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
            Customization
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography gutterBottom>Rate</Typography>
              <Slider
                value={customization.rate}
                onChange={(e, value) => setCustomization({ ...customization, rate: value })}
                min={-50}
                max={50}
                valueLabelDisplay="auto"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography gutterBottom>Pitch</Typography>
              <Slider
                value={customization.pitch}
                onChange={(e, value) => setCustomization({ ...customization, pitch: value })}
                min={-50}
                max={50}
                valueLabelDisplay="auto"
              />
            </Grid>
          </Grid>

          <Button
            variant="contained"
            color="primary"
            onClick={handleSynthesis}
            disabled={!text || !selectedVoice || loading}
            startIcon={loading ? <CircularProgress size={20} /> : <VolumeUp />}
            sx={{ mt: 2 }}
            fullWidth
          >
            Synthesize Speech
          </Button>
        </StyledPaper>

        {/* Audio Player */}
        {audio && (
          <StyledPaper>
            <Typography variant="h6" gutterBottom>
              Audio Player
            </Typography>
            <audio ref={audioRef} />
            <AudioControls>
              <IconButton onClick={handlePlayPause}>
                {audioPlaying ? <Stop /> : <PlayArrow />}
              </IconButton>
              <IconButton onClick={handleDownload}>
                <Download />
              </IconButton>
            </AudioControls>
          </StyledPaper>
        )}

        {/* Error Display */}
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