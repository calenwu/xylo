import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'primary': {
          100: '#ffd372',
          200: '#ffcb5b',
          300: '#ffc443',
          400: '#ffbc2c',
          500: '#ffb514',
          600: '#e6a312',
          700: '#cc9110',
          800: '#b37f0e',
          900: '#996d0c',
        }, 
        'secondary': {
          100: '#97e0f0',
          200: '#85dbee',
          300: '#74d5eb',
          400: '#62d0e9',
          500: '#51cbe6',
          600: '#49b7cf',
          700: '#41a2b8',
          800: '#398ea1',
          900: '#317a8a',
        },
        'quinary': {
          100: '#dcef8c',
          200: '#d6ec79',
          300: '#d1e965',
          400: '#cbe752',
          500: '#c5e43f',
          600: '#b1cd39',
          700: '#9eb632',
          800: '#8aa02c',
          900: '#768926',
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
