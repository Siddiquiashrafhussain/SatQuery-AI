import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: '--font-family' });

export const metadata: Metadata = {
  title: "SatQuery AI | ISRO SIH 2026",
  description: "Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries. Built for Smart India Hackathon 2026 by Team LIFTOFF.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
