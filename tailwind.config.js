const colors = require("tailwindcss/colors")

module.exports = {
  purge: ['./dashboard/**/*.html', "./main/**/*.html"],
  mode: 'jit',
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      bland: 'rgba(0, 0, 0, 0.5)',
      ...colors,
    },
    fontFamily: {
      sans: ['"Libre Franklin"', 'sans-serif']
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
