import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography, Card, CardContent, LinearProgress } from '@mui/material';
import { styled } from '@mui/material/styles';
import ReactH5AudioPlayer from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';

// Styled components
const PlayerContainer = styled(Card)(({ theme }) => ({
  maxWidth: '600px',
  margin: '40px auto',
  textAlign: 'center',
  boxShadow: theme.shadows[5],
  borderRadius: theme.shape.borderRadius,
}));

const Title = styled(Typography)(({ theme }) => ({
  fontWeight: 'bold',
  margin: theme.spacing(2, 0),
  color: theme.palette.primary.main,
}));

const ImageContainer = styled(Box)(({ theme, isPlaying }) => ({
  width: '100%',
  height: '250px',
  overflow: 'hidden',
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[3],
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  img: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transition: 'transform 0.5s ease-in-out',
    transform: isPlaying ? 'scale(1.05)' : 'scale(1)', // Smooth scale transition
  },
}));

const StyledProgress = styled(LinearProgress)(({ theme }) => ({
  height: 8,
  borderRadius: theme.shape.borderRadius,
  margin: theme.spacing(2, 2),
}));

const StyledAudioPlayer = styled(ReactH5AudioPlayer)(({ theme }) => ({
  '.rhap_container': {
    boxShadow: theme.shadows[3],
    borderRadius: theme.shape.borderRadius,
  },
  '.rhap_progress-bar': {
    backgroundColor: theme.palette.primary.main,
  },
  '.rhap_time': {
    color: theme.palette.text.primary,
  },
  '.rhap_controls-section button': {
    color: theme.palette.text.primary,
  },
}));

const AudioPlayerPage = () => {
  const audioSrc =
    'https://od.lk/s/NTJfNDc2MDQ0NTZf/Children%20Who%20Chase%20Lost%20Voices.mp3';
  const imageSrc = 'https://od.lk/s/NTJfNDc2MDQ0NTdf/5cm.jpg';

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef(null);

  const startTime = 30; // Start playback at 30 seconds

  // Set the start time and duration on mount
  useEffect(() => {
    const audio = audioRef.current?.audio.current;
    if (audio) {
      audio.currentTime = startTime;
      audio.onloadedmetadata = () => setDuration(audio.duration);
    }
  }, [startTime]);

  // Track playback progress
  const onTimeUpdate = () => {
    const audio = audioRef.current?.audio.current;
    if (audio) {
      setCurrentTime(audio.currentTime);
    }
  };

  const handlePlay = () => setIsPlaying(true);
  const handlePause = () => setIsPlaying(false);

  return (
    <PlayerContainer>
      <ImageContainer isPlaying={isPlaying}>
        <img src={imageSrc} alt="Album Cover" />
      </ImageContainer>
      <CardContent>
        <Title variant="h5">Enhanced Audio Player</Title>
        <StyledAudioPlayer
          src={audioSrc}
          ref={audioRef}
          onPlay={handlePlay}
          onPause={handlePause}
          onListen={onTimeUpdate}
          autoPlay={false}
          classNamePrefix="custom-audio-player"
                      style={{
                        backgroundColor: 'transparent',
                         boxShadow: 'none',
                      }}
        />
        <StyledProgress
          variant="determinate"
          value={duration > 0 ? (currentTime / duration) * 100 : 0}
        />
        <Typography variant="body2">
          {`Current Time: ${currentTime.toFixed(2)}s / ${duration.toFixed(2)}s`}
        </Typography>
      </CardContent>
    </PlayerContainer>
  );
};

export default AudioPlayerPage;