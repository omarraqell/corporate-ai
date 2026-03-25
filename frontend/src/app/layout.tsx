import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Corporate AI — Command Center",
  description: "Multi-Agent Corporate AI Orchestration System",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
