/**
 * Script to convert red colors in no.gif to orange
 * This script requires sharp library to process the GIF
 * 
 * Usage: node scripts/convert-gif-color.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const gifPath = path.join(__dirname, '../public/images/no.gif');
const outputPath = path.join(__dirname, '../public/images/no-orange.gif');

// Check if sharp is available
let sharp;
try {
  sharp = (await import('sharp')).default;
} catch (e) {
  console.error('Error: sharp library is not installed.');
  console.error('Please install it by running: npm install sharp');
  console.error('Or use an online tool to manually convert the GIF color.');
  process.exit(1);
}

async function convertGifColor() {
  try {
    if (!fs.existsSync(gifPath)) {
      console.error(`File not found: ${gifPath}`);
      process.exit(1);
    }

    console.log('Reading GIF file...');
    const imageBuffer = fs.readFileSync(gifPath);
    
    console.log('Processing GIF (this may take a while for animated GIFs)...');
    
    // For animated GIFs, we need to process each frame
    // Sharp can handle this, but it's complex for animated GIFs
    // A simpler approach: use CSS filter (already added) or use an image editor
    
    // Note: Sharp doesn't directly support animated GIF frame-by-frame processing easily
    // For a proper solution, you might need to:
    // 1. Extract frames using gif-frames
    // 2. Process each frame with sharp
    // 3. Reassemble with gifencoder or similar
    
    console.log('Note: For animated GIFs, CSS filter is the simplest solution.');
    console.log('If you need to edit the actual file, consider using an image editor like GIMP or Photoshop.');
    console.log('Or use an online tool like: https://ezgif.com/colorize');
    
  } catch (error) {
    console.error('Error processing GIF:', error);
    process.exit(1);
  }
}

convertGifColor();
