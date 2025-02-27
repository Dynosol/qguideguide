import React, { createContext, useState, useContext, useMemo } from 'react';
import { createTheme, ThemeProvider as MUIThemeProvider } from '@mui/material/styles';
import { colorPalettes } from './colors';

// const HARVARD_COLOR = '#963b3c';

export type ThemeMode = 'light' | 'dark';

type ThemeContextValue = {
  mode: 'light' | 'dark';
  toggleMode: (isDark: boolean) => void;
};

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export const useThemeContext = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useThemeContext must be used inside a ThemeProvider');
  return ctx;
};

export const ThemeContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Initialize mode from localStorage or default
  const [mode, setMode] = useState<'light' | 'dark'>(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark' ? 'dark' : 'light';
  });

  const toggleMode = (isDark: boolean) => {
    setMode(isDark ? 'dark' : 'light');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  };

  // Create MUI theme based on mode
  const theme = useMemo(() => createTheme({
    palette: {
      mode,
      primary: {
        main: colorPalettes[mode].harvard,
      },
    },
  }), [mode]);

  return (
    <ThemeContext.Provider value={{ mode, toggleMode }}>
      <MUIThemeProvider theme={theme}>
        {children}
      </MUIThemeProvider>
    </ThemeContext.Provider>
  );
};
