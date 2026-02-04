/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'file2.aitohumanize.com',
      },
      {
        protocol: 'https',
        hostname: 'grsai.dakka.com.cn',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
      },
    ],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', 'framer-motion'],
  },
  async rewrites() {
    return [
      {
        source: '/static/:path*',
        destination: 'http://localhost:8000/static/:path*',
      },
    ]
  },
}

export default nextConfig
