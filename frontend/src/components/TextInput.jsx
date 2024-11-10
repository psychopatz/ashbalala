// src/components/TextInput.js
import React from 'react';
import styled from '@emotion/styled';
import { Typography, TextField, Grid, Slider, Button, CircularProgress, Paper } from '@mui/material';
import { VolumeUp } from '@mui/icons-material';

const InputPaper = styled(Paper)`
  padding: 2rem;
  margin-bottom: 2rem;
`;

const TextInput = ({ text, setText, customization, setCustomization, onSynthesize, loading, disabled }) => {
  return (
    <InputPaper>
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
        onClick={onSynthesize}
        disabled={disabled || loading}
        startIcon={loading ? <CircularProgress size={20} /> : <VolumeUp />}
        sx={{ mt: 2 }}
        fullWidth
      >
        Synthesize Speech
      </Button>
    </InputPaper>
  );
};

export default TextInput;