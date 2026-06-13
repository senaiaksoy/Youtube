import { youtubeApiFetch } from '../lib/youtube-token';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config({ path: path.join(process.cwd(), '.env.local') });

async function run() {
  try {
    const data = await youtubeApiFetch('https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=FI2kj2cDe8k');
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('Error fetching video:', err);
  }
}
run();
