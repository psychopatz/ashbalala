// frontend/src/hooks/useSnackbar.jsx
import { useContext } from 'react';
import { SnackbarContext } from '../context/SnackbarContext';

const useSnackbar = () => {
  return useContext(SnackbarContext);
};

export default useSnackbar;