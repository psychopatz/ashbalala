// src/components/AudioPlayer.js
import React from 'react';
import styled from '@emotion/styled';
import { Typography, IconButton, Paper, Box } from '@mui/material';
import { PlayArrow, Stop, Download } from '@mui/icons-material';

const PlayerPaper = styled(Paper)`
  padding: 2rem;
  margin-bottom: 2rem;
`;

const AudioControls = styled(Box)`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
`;

const AudioPlayer = ({ audioRef, audioPlaying, onPlayPause, onDownload }) => {
  return (
    <PlayerPaper>
      <Typography variant="h6" gutterBottom>
        Audio Player
      </Typography>
      <audio ref={audioRef} />
      <AudioControls>
        <IconButton onClick={onPlayPause}>
          {audioPlaying ? <Stop /> : <PlayArrow />}
        </IconButton>
        <IconButton onClick={onDownload}>
          <Download />
        </IconButton>
      </AudioControls>
    </PlayerPaper>
  );
};

export default AudioPlayer;