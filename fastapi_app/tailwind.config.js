/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["static/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        background_light: '#f5f5f5',
        background_light_secondary: '#f0f0f0',
        background_dark: '#1f2123',
        background_dark_secondary: '#242729',
        content_background_light: '#6e6e6e',
        content_background_dark: '#1f1f1f',
        text_light: '#1Ff2123',
        text_light_secondary: '#242729',
        text_dark: '#ffffff',
        text_dark_secondary: '#fafafa',
        contrast: '#fa0000'
      },
    },
    container: {
      center: true,
    },
  },
  plugins: [],
  darkMode: 'class',
}