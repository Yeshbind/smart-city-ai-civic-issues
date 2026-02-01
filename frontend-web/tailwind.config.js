/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#60a5fa',
        primaryDark: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        lightBg: '#f3f4f6',
      },
    },
  },
  plugins: [],
}