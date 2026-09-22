import { readFile, writeFile, mkdir, mkdtemp, rename, access } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const origin='https://venture-publisher.vercel.app/lodgehelm/journal/';
const source=process.env.PUBLISHER_DIST;
const get=async name=>{
 if(source)return readFile(path.join(source,name));
 const response=await fetch(new URL(name,origin),{redirect:'error',signal:AbortSignal.timeout(30000)});
 if(!response.ok)throw Error(`Journal source ${name}: HTTP ${response.status}`);
 if(Number(response.headers.get('content-length')||0)>20_000_000)throw Error('Journal file too large');
 const chunks=[];let size=0;
 for await(const chunk of response.body){size+=chunk.length;if(size>20_000_000)throw Error('Journal file too large');chunks.push(chunk);}
 return Buffer.concat(chunks);
};
const manifest=JSON.parse(await get('manifest.json'));
if(manifest.brand!=='lodgehelm'||!Array.isArray(manifest.files)||!manifest.files.length||manifest.files.length>10000)throw Error('Invalid journal manifest');
const seen=new Set();let total=0;
for(const entry of manifest.files){
 if(!/^[a-zA-Z0-9_-]+(?:\/[a-zA-Z0-9_-]+)*\.(?:html|xml|json|png|webp|svg|woff2|txt)$/.test(entry.path)||entry.path==='manifest.json'||seen.has(entry.path))throw Error('Unsafe or duplicate journal path');
 if(!/^[a-f0-9]{64}$/.test(entry.sha256)||!Number.isInteger(entry.bytes)||entry.bytes<1||entry.bytes>20_000_000)throw Error('Invalid journal file metadata');
 total+=entry.bytes;seen.add(entry.path);
}
if(total>200_000_000||!seen.has('index.html')||!seen.has('sitemap.xml'))throw Error('Incomplete or oversized journal');
const staging=await mkdtemp(path.join(root,'.journal-staging-'));
for(const entry of manifest.files){
 const bytes=await get(entry.path);
 if(bytes.length!==entry.bytes||createHash('sha256').update(bytes).digest('hex')!==entry.sha256)throw Error(`Journal changed during sync: ${entry.path}`);
 const target=path.join(staging,entry.path);await mkdir(path.dirname(target),{recursive:true});await writeFile(target,bytes);
}
await writeFile(path.join(staging,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');
const target=path.join(root,'journal');
try{
 await access(target);
 // Refuse to replace a hand-maintained folder. Previous generated versions
 // stay recoverable locally and in Git history; no homepage files are touched.
 const previous=JSON.parse(await readFile(path.join(target,'manifest.json'),'utf8'));
 if(previous.brand!=='lodgehelm')throw Error('Existing journal is not managed by this publisher');
 await mkdir(path.join(root,'.journal-backups'),{recursive:true});
 await rename(target,path.join(root,'.journal-backups',String(Date.now())));
}catch(error){if(error.code!=='ENOENT')throw error;}
await rename(staging,target);
console.log(`Synced ${manifest.files.length} verified LodgeHelm journal files.`);
