import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // Custom SatQuery AI Colors (High-Contrast Dark Theme)
        'sat-bg-primary': '#0a0a0a',
        'sat-bg-secondary': '#171717',
        'sat-accent': '#10b981',
        'sat-accent-hover': '#059669',
        'sat-border': '#333333',
        'sat-surface': '#171717',
      },
    },
  },
  plugins: [],
};
export default config;
