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
        // Custom SatQuery AI Colors
        'sat-bg-primary': '#0f111a',
        'sat-bg-secondary': '#1a1d2d',
        'sat-accent': '#3b82f6',
        'sat-accent-hover': '#2563eb',
        'sat-glass': 'rgba(26, 29, 45, 0.7)',
      },
    },
  },
  plugins: [],
};
export default config;
