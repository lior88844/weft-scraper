const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const docsDir = path.join(projectRoot, 'docs');
const sourceIndex = path.join(projectRoot, 'index.html');
const docsIndex = path.join(docsDir, 'index.html');
const storesDir = path.join(projectRoot, 'stores');
const docsStoresDir = path.join(docsDir, 'stores');

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function copyFile(src, dest) {
  if (!fs.existsSync(src)) {
    console.warn(`⚠️ Missing file, skipping: ${src}`);
    return;
  }
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
  console.log(`✅ Copied ${path.relative(projectRoot, src)} -> ${path.relative(projectRoot, dest)}`);
}

function copyDirectory(src, dest) {
  if (!fs.existsSync(src)) {
    console.warn(`⚠️ Missing directory, skipping: ${src}`);
    return;
  }
  fs.rmSync(dest, { recursive: true, force: true });
  fs.cpSync(src, dest, { recursive: true });
  console.log(`📁 Synced ${path.relative(projectRoot, src)} -> ${path.relative(projectRoot, dest)}`);
}

function syncIndex() {
  ensureDir(docsDir);
  copyFile(sourceIndex, docsIndex);
}

function syncStores() {
  ensureDir(docsStoresDir);
  const stores = fs.readdirSync(storesDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory());

  stores.forEach((store) => {
    const storeName = store.name;
    const srcStoreDir = path.join(storesDir, storeName);
    const destStoreDir = path.join(docsStoresDir, storeName);

    // Copy index.html
    copyFile(
      path.join(srcStoreDir, 'index.html'),
      path.join(destStoreDir, 'index.html')
    );

    // Copy data directory
    copyDirectory(
      path.join(srcStoreDir, 'data'),
      path.join(destStoreDir, 'data')
    );
  });
}

function main() {
  console.log('🔄 Syncing docs folder with latest static site...');
  syncIndex();
  syncStores();
  console.log('✨ Docs folder is up to date.');
}

main();

