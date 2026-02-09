#!/usr/bin/env node
/**
 * Parse an HTML table with id `standards` and download PDFs.
 * File names follow: `${standardName}(${code}).pdf`
 *
 * Usage:
 *   node scripts/download-standards.js --source ./standards.html --baseUrl https://example.com --outDir ./downloads --limit 4
 *   node scripts/download-standards.js --url https://example.com/page-with-standards --outDir ./downloads
 */

const fs = require('fs')
const path = require('path')
const axios = require('axios')
const cheerio = require('cheerio')

// Simple CLI args parser
function parseArgs() {
  const args = process.argv.slice(2)
  const opts = {}
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a.startsWith('--')) {
      const key = a.replace(/^--/, '')
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true
      opts[key] = val
    }
  }
  return opts
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true })
  }
}

function sanitizeFileName(name) {
  // Remove characters invalid on Windows/macOS/Linux
  return name.replace(/[\\/:*?"<>|\n\r]+/g, '').trim()
}

async function loadHtml({ source, url }) {
  if (source) {
    return fs.readFileSync(path.resolve(source), 'utf8')
  }
  if (url) {
    const res = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    })
    return res.data
  }
  throw new Error('Provide --source <file.html> or --url <http-url>')
}

function extractRows($) {
  const rows = []
  $('#standards tbody tr').each((_, tr) => {
    const $tr = $(tr)
    const tds = $tr.find('td')
    if (!tds || tds.length === 0) return

    const nameCell = tds.eq(1) // second column: نام استاندارد
    const name = sanitizeFileName(nameCell.text().trim())

    // Find the "استاندارد آموزش" download link: href like /home/dn-std/<code>
    const pdfCell = $tr.find('td a[href*="/home/dn-std/"]').first()
    let pdfHref = pdfCell.attr('href') || ''

    // Fallback: if no /home/dn-std/, try direct uploads link
    if (!pdfHref) {
      const uploadsCell = $tr.find('td a[href*="/uploads/"]').first()
      pdfHref = uploadsCell.attr('href') || ''
    }

    if (!name || !pdfHref) return

    // Try to extract code from href
    let code = ''
    const match = pdfHref.match(/(\d+)/)
    if (match) code = match[1]

    rows.push({ name, pdfHref, code })
  })
  return rows
}

function absolutize(urlOrPath, baseUrl) {
  if (!urlOrPath) return ''
  if (/^https?:\/\//i.test(urlOrPath)) return urlOrPath
  if (!baseUrl) throw new Error(`Relative URL "${urlOrPath}" provided but --baseUrl was not set`)
  return baseUrl.replace(/\/$/, '') + (urlOrPath.startsWith('/') ? '' : '/') + urlOrPath
}

async function downloadFile(url, destPath) {
  const res = await axios.get(url, {
    responseType: 'arraybuffer',
    maxRedirects: 5,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      Accept: 'application/pdf,application/octet-stream;q=0.9,*/*;q=0.8'
    }
  })
  fs.writeFileSync(destPath, res.data)
}

async function main() {
  const opts = parseArgs()
  const { source, url, baseUrl, outDir = './downloads', limit = 4 } = opts

  ensureDir(outDir)
  const html = await loadHtml({ source, url })
  const $ = cheerio.load(html)
  const rows = extractRows($)

  if (!rows.length) {
    console.log('No rows found in #standards table.')
    return
  }

  console.log(`Found ${rows.length} standards. Starting downloads...`)

  // Concurrency control
  const concurrency = Math.max(1, Number(limit) || 4)
  let index = 0

  async function worker(id) {
    while (index < rows.length) {
      const current = rows[index++]
      const { name, pdfHref, code } = current
      const fileName = sanitizeFileName(`${name}${code ? `(${code})` : ''}.pdf`)
      const targetPath = path.join(outDir, fileName)

      if (fs.existsSync(targetPath)) {
        console.log(`[skip] ${fileName} (already exists)`) 
        continue
      }

      const absoluteUrl = absolutize(pdfHref, baseUrl)
      try {
        console.log(`[${id}] downloading: ${fileName} -> ${absoluteUrl}`)
        await downloadFile(absoluteUrl, targetPath)
        console.log(`[${id}] done: ${fileName}`)
      } catch (err) {
        console.error(`[${id}] failed: ${fileName} | ${err.message}`)
      }
    }
  }

  const workers = Array.from({ length: concurrency }, (_, i) => worker(i + 1))
  await Promise.all(workers)
  console.log('All downloads attempted.')
}

main().catch(err => {
  console.error('Fatal error:', err)
  process.exit(1)
})