const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const markedPath = path.join(__dirname, 'vendor', 'marked', 'lib', 'marked.esm.js');
  const { marked } = await import(pathToFileURL(markedPath).href);
  const sourcePath = process.argv[2];
  if (!sourcePath) {
    throw new Error('report.md 路径必填');
  }
  const markdown = fs.readFileSync(sourcePath, 'utf8');
  process.stdout.write(marked.parse(markdown));
})().catch((error) => {
  process.stderr.write(error.stack + '\n');
  process.exitCode = 1;
});
