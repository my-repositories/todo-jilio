import { resolve } from 'path';
import type { NextConfig } from "next";


const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      app: resolve(__dirname, 'src/app'),
    },
  },
};

export default nextConfig;
