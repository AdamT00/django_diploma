/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["../posts/templates/posts/*.{html,js}"],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [
            {
                mytheme: {
                    "primary": "#064e3b",
                    "secondary": "#84cc16",
                    "accent": "#1fb2a6",
                    "neutral": "#2a323c",
                    "base-100": "#1d232a",
                    "info": "#3abff8",
                    "success": "#36d399",
                    "warning": "#fbbd23",
                    "error": "#f87272",
                },
            },
        ],
    },
}

