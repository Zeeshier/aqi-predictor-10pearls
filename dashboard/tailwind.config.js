/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          50: "#FAFAFA",
          100: "#F4F4F5",
          200: "#E4E4E7",
          300: "#D4D4D8"
        },
        card: "#FFFFFF",
        primary: {
          900: "#09090B",
          800: "#18181B",
          700: "#27272A",
          500: "#3F3F46"
        },
        aqi: {
          good: "#059669",
          moderate: "#D97706",
          sensitive: "#EA580C",
          unhealthy: "#DC2626",
          veryUnhealthy: "#7C3AED",
          hazardous: "#991B1B"
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
};
