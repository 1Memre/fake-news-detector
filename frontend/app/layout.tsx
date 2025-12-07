import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Fake News Detector",
  description: "Detect fake news using AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-900 text-white`}
      >
        <nav className="bg-gray-800 border-b border-gray-700 p-4">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <Link href="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent hover:opacity-80 transition-opacity">
              AI Detector
            </Link>
            <div className="space-x-6">
              <Link href="/" className="text-gray-300 hover:text-white transition-colors font-medium">
                Analyze
              </Link>
              <Link href="/history" className="text-gray-300 hover:text-white transition-colors font-medium">
                History
              </Link>
            </div>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
