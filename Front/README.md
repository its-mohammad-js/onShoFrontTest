# Nuxt 3 Minimal Starter

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## Google OAuth Setup

برای تنظیم لاگین با گوگل، به [راهنمای کامل Google OAuth](docs/GOOGLE_OAUTH_SETUP.md) مراجعه کنید.

خلاصه مراحل:
1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. یک پروژه ایجاد کنید و OAuth Client ID بسازید
3. Authorized redirect URIs را اضافه کنید: `http://localhost:3000/auth/google/callback`
4. Client ID را در فایل `.env` قرار دهید: `GOOGLE_CLIENT_ID=your-client-id`

## Download Standards PDFs (Node Script)

This project includes a helper script to parse a standards HTML table and download the PDFs named like `نام استاندارد(کد).pdf`.

Usage examples:

```bash
# 1) Parse a local HTML file and use base URL for relative links
npm run download-standards -- --source ./standards.html --baseUrl https://your-domain.tld --outDir ./downloads

# 2) Fetch and parse a remote page directly
node scripts/download-standards.js --url https://your-domain.tld/page-with-standards --outDir ./downloads --limit 4
```

Arguments:
- `--source` Local HTML file containing the table `#standards`
- `--url` Remote page to fetch and parse
- `--baseUrl` Required when links in the table are relative (e.g. `/home/dn-std/10326`)
- `--outDir` Destination directory for downloaded PDFs (default `./downloads`)
- `--limit` Concurrency limit for downloads (default `4`)

Notes:
- The script looks for links like `/home/dn-std/<code>` in the "استاندارد آموزش" column; if not found, it falls back to direct `/uploads/...pdf` links.
- File names are sanitized for Windows/macOS/Linux.
