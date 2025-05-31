/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'Helvetica', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', '"Noto Sans"', 'sans-serif'],
      },
      colors: {
        'editor-bg': '#fafafa',
        'sidebar-bg': '#ffffff',
        'border-light': '#e5e7eb',
        'text-primary': '#1f2937',
        'text-secondary': '#6b7280',
        'accent-blue': '#3b82f6',
        'accent-red': '#ef4444',
      }
    },
  },
  plugins: [],
} 