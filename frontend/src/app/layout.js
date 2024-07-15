import './globals.css'

export const metadata = {
  title: 'Purchase List',
  description: 'A list of purchases',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
