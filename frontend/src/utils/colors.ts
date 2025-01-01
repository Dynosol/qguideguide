export type ThemeMode = 'light' | 'dark';

export interface ColorPalette {
  navbarBgDark: string;
  textColorLight: string;
  textColorDark: string;
  linkHoverBgLight: string;
  linkHoverBgDark: string;
  hamburgerColorLight: string;
  hamburgerColorDark: string;
  greyish: string;
  harvard: string;
  darkGreyish: string;
}

export const colorPalettes: Record<ThemeMode, ColorPalette> = {
  light: {
    navbarBgDark: 'rgba(29, 29, 29, 1)',
    textColorLight: 'rgb(59, 59, 59)',
    textColorDark: '#ccc',
    linkHoverBgLight: '#8e8e8e',
    linkHoverBgDark: '#444',
    hamburgerColorLight: '#333',
    hamburgerColorDark: '#ffffff',
    greyish: 'rgba(230, 230, 237)',
    harvard: '#963b3c',
    darkGreyish: '#3c3c3c',
  },
  dark: {
    navbarBgDark: '#1d1d1d',
    textColorLight: '#ffffff',
    textColorDark: '#ccc',
    linkHoverBgLight: '#555555',
    linkHoverBgDark: '#333333',
    hamburgerColorLight: '#ffffff',
    hamburgerColorDark: '#ffffff',
    greyish: '#2c2c2c',
    harvard: '#963b3c',
    darkGreyish: '#3c3c3c',
  },
};