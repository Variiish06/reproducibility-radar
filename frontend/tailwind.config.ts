import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        radar: {
          blue: "#0F4C81",
          teal: "#00A896",
          amber: "#F4A261",
          red: "#E63946",
        },
      },
    },
  },
  plugins: [],
};

export default config;
