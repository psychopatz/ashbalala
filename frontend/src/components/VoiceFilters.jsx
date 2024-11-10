// src/components/VoiceFilters.js
import React from 'react';
import styled from '@emotion/styled';
import {
  Typography,
  Select,
  MenuItem,
  Button,
  Grid,
  InputLabel,
  Paper,
  FormControl,
} from '@mui/material';
import { Refresh } from '@mui/icons-material';

const FiltersPaper = styled(Paper)`
  padding: 2rem;
  margin-bottom: 2rem;
`;

const StyledFormControl = styled(FormControl)`
  min-width: 200px;
  margin-bottom: 1rem;
`;

const VoiceFilters = ({ filters, setFilters, onRefresh }) => {
  return (
    <FiltersPaper>
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
            onClick={onRefresh}
            fullWidth
          >
            Refresh Voices
          </Button>
        </Grid>
      </Grid>
    </FiltersPaper>
  );
};

export default VoiceFilters;