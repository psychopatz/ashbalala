// src/components/VoiceSelector.js
import React from 'react';
import styled from '@emotion/styled';
import { Typography, Grid, Paper } from '@mui/material';

const SelectorPaper = styled(Paper)`
  padding: 2rem;
  margin-bottom: 2rem;
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

const VoiceSelector = ({ voices, selectedVoice, onVoiceSelect }) => {
  return (
    <SelectorPaper>
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
                    onClick={() => onVoiceSelect(voice.name)}
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
    </SelectorPaper>
  );
};

export default VoiceSelector;