/** @type {import('tailwindcss').Config} */
export default {
  content: ['./*.html', './src/**/*.{js,ts,html}'],
  theme: {
    extend: {
      colors: {
        rose:   '#A24053',
        'rose-dark': '#8a3346',
        blue:   '#1C4E6D',
        aqua:   '#22524D',
        page:   '#FAFAF8',
        muted:  '#6B6B6B',
        border: '#E5E5E5',
      },
      fontFamily: {
        heading: ['Tinos', 'Georgia', 'serif'],
        body:    ['DM Sans', 'system-ui', 'sans-serif'],
      },
      maxWidth: { site: '1280px' },
    },
  },
  plugins: [],
}

