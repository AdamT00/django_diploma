/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../posts/templates/posts/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}

