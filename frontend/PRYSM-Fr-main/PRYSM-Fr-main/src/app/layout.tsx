import type { Metadata } from "next";
import { GFS_Didot, Geist_Mono } from "next/font/google";
import "./globals.css";
const gfsDidot = GFS_Didot({
  weight: "400",
  variable: "--font-gfs-didot",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PRYSM | Audit Intelligence Platform",
  description: "AI-powered Audit Intelligence Platform built by Team Ragnarok.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${gfsDidot.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className={`min-h-full flex flex-col bg-background text-foreground ${gfsDidot.className}`}>
        {children}
      </body>
    </html>
  );
}
