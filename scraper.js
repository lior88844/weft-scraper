const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  baseUrl: 'https://www.nizat.com',
  outputDir: path.join(__dirname, 'data'),
  outputFile: 'products.json',
  delayBetweenRequests: 2000, // milliseconds
  headless: true,
  debug: false, // Set to true to save screenshots and see browser
  maxCategories: 20, // Maximum number of categories to scrape (set to null for all)
  maxProducts: 100, // Maximum number of products to scrape (only products with images)
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
};

// Ensure output directory exists
if (!fs.existsSync(CONFIG.outputDir)) {
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
}

/**
 * Sleep utility function
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main scraper function
 */
async function scrapeNitzatHaduvdevan() {
  console.log('🚀 Starting Nitzat Haduvdevan scraper...');
  
  const browser = await puppeteer.launch({
    headless: CONFIG.debug ? false : CONFIG.headless,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--lang=he']
  });

  try {
    const page = await browser.newPage();
    
    // Set user agent and viewport
    await page.setUserAgent(CONFIG.userAgent);
    await page.setViewport({ width: 1920, height: 1080 });
    
    console.log(`📡 Navigating to ${CONFIG.baseUrl}...`);
    await page.goto(CONFIG.baseUrl, { 
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    // Handle cookie consent if present
    try {
      const acceptCookiesButton = await page.$('button[class*="accept"], button[class*="אשר"]');
      if (acceptCookiesButton) {
        console.log('🍪 Accepting cookies...');
        await acceptCookiesButton.click();
        await sleep(1000);
      }
    } catch (e) {
      console.log('ℹ️  No cookie consent dialog found');
    }
    
    // Save screenshot if in debug mode
    if (CONFIG.debug) {
      const screenshotPath = path.join(CONFIG.outputDir, 'debug-homepage.png');
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`📸 Debug screenshot saved to: ${screenshotPath}`);
    }

    const allProducts = [];
    const usedImages = new Set(); // Track images that have been used

    // Wait for content to load
    await page.waitForSelector('body', { timeout: 10000 });
    await sleep(3000); // Give more time for dynamic content
    
    // Get all category links from the main menu
    console.log('📂 Extracting categories...');
    const categories = await page.evaluate(() => {
      const categoryLinks = [];
      
      // Try multiple selectors to find category links
      const selectors = [
        'a[href*="/category/"]',
        'a[href*="/cat/"]',
        'a[href*="/shop/"]',
        'nav a',
        '[class*="menu"] a',
        '[class*="category"] a'
      ];
      
      let allLinks = [];
      selectors.forEach(selector => {
        const links = document.querySelectorAll(selector);
        allLinks = [...allLinks, ...Array.from(links)];
      });
      
      allLinks.forEach(link => {
        const href = link.getAttribute('href');
        const text = link.textContent.trim();
        
        // Filter out empty, too short, or duplicate links
        // Only include links that look like actual pages (not # or javascript:)
        if (href && text && text.length > 2 && text.length < 100 && 
            !href.startsWith('#') && !href.startsWith('javascript:')) {
          // Avoid duplicates
          if (!categoryLinks.find(c => c.url === href || c.name === text)) {
            categoryLinks.push({
              name: text,
              url: href
            });
          }
        }
      });
      
      return categoryLinks;
    });

    console.log(`✅ Found ${categories.length} potential categories/pages`);

    // Filter categories - exclude fruits/vegetables/nuts/seeds, include snacks and dry goods
    const excludeKeywords = ['פירות', 'ירקות', 'ירוקים', 'נבטים', 'ירקניה', 'אגוז', 'זרעים', 'גרעינים'];
    const includeKeywords = ['חטיפ', 'דגנים', 'קטניות', 'פסטה', 'לחמים', 'מאפים', 
                             'ממרח', 'שימור', 'בוקר', 'שוקולד', 'חומרי', 'אפייה', 'בישול',
                             'תבלינים', 'קמח', 'שמן', 'סוכר', 'מלח', 'קקאו', 'קוקוס', 'רטב'];
    
    const filteredCategories = categories.filter(cat => {
      const name = cat.name.toLowerCase();
      // Exclude if contains exclude keywords
      if (excludeKeywords.some(keyword => name.includes(keyword.toLowerCase()))) {
        return false;
      }
      // Include if contains include keywords
      return includeKeywords.some(keyword => name.includes(keyword.toLowerCase()));
    });

    console.log(`🔍 Filtered to ${filteredCategories.length} relevant categories (snacks & dry goods)`);
    
    const maxCategories = CONFIG.maxCategories || filteredCategories.length;
    const categoriesToScrape = Math.min(filteredCategories.length, maxCategories);
    
    console.log(`\n🔄 Will scrape up to ${CONFIG.maxProducts} products with images from ${categoriesToScrape} categories...\n`);
    
    for (let i = 0; i < categoriesToScrape; i++) {
      // Check if we've reached the product limit
      if (allProducts.length >= CONFIG.maxProducts) {
        console.log(`\n✅ Reached maximum of ${CONFIG.maxProducts} products. Stopping scrape.`);
        break;
      }
      
      const category = filteredCategories[i];
      console.log(`\n📦 Scraping category: ${category.name} (${allProducts.length}/${CONFIG.maxProducts} products collected)`);
      
      try {
        // Construct full URL
        let categoryUrl;
        if (category.url.startsWith('http')) {
          categoryUrl = category.url;
        } else if (category.url.startsWith('/')) {
          categoryUrl = `${CONFIG.baseUrl}${category.url}`;
        } else {
          categoryUrl = `${CONFIG.baseUrl}/${category.url}`;
        }
        
        console.log(`   → ${categoryUrl}`);
        
        await page.goto(categoryUrl, { 
          waitUntil: 'networkidle2',
          timeout: 30000
        });
        
        await sleep(CONFIG.delayBetweenRequests);

        // Wait for content to load
        await sleep(3000);
        
        // Scroll page systematically to trigger lazy loading of all images
        console.log('   📜 Scrolling to load images...');
        await page.evaluate(async () => {
          await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 300; // Scroll distance
            const timer = setInterval(() => {
              const scrollHeight = document.body.scrollHeight;
              window.scrollBy(0, distance);
              totalHeight += distance;

              if (totalHeight >= scrollHeight) {
                clearInterval(timer);
                resolve();
              }
            }, 200); // Scroll every 200ms
          });
        });
        
        // Wait for images to load
        await sleep(2000);
        
        // Wait for images to have src attributes
        try {
          await page.waitForFunction(() => {
            const images = document.querySelectorAll('img');
            return Array.from(images).some(img => img.src || img.dataset.src);
          }, { timeout: 5000 });
        } catch (e) {
          console.log('   ⚠️  Timeout waiting for images, continuing...');
        }
        
        // Scroll back to top
        await page.evaluate(() => {
          window.scrollTo(0, 0);
        });
        await sleep(1000);
        
        // Save screenshot if in debug mode
        if (CONFIG.debug) {
          const screenshotPath = path.join(CONFIG.outputDir, `debug-category-${category.name.replace(/[^a-zA-Z0-9]/g, '_')}.png`);
          await page.screenshot({ path: screenshotPath, fullPage: false });
          console.log(`   📸 Debug screenshot: ${screenshotPath}`);
        }
        
        // Extract products from the page
        const products = await page.evaluate((categoryName) => {
          const extractedProducts = [];
          
          // Only keep images whose wrapping div has the required ID
          const getValidImageSrc = (imgElement) => {
            if (!imgElement || typeof imgElement.closest !== 'function') return null;
            
            const wrapper = imgElement.closest('#ContentPlaceHolder1_productpic');
            const hasRepeaterImageId = typeof imgElement.id === 'string' &&
              imgElement.id.startsWith('ContentPlaceHolder1_products_rptproducts_imgProductPic');
            
            if (!wrapper && !hasRepeaterImageId) return null;
            
            const attributeCandidates = [
              'src',
              'data-src',
              'data-lazy-src',
              'data-original',
              'data-srcset',
              'data-lazy',
              'srcset'
            ];
            
            for (const attr of attributeCandidates) {
              const value = imgElement.getAttribute(attr);
              if (value && value.trim() !== '') {
                return value.trim();
              }
            }
            
            if (imgElement.dataset) {
              const datasetKeys = ['src', 'lazySrc', 'original'];
              for (const key of datasetKeys) {
                if (imgElement.dataset[key] && imgElement.dataset[key].trim() !== '') {
                  return imgElement.dataset[key].trim();
                }
              }
            }
            
            const style = imgElement.getAttribute('style');
            if (style) {
              const urlMatch = style.match(/url\(['"]?([^'")\s]+)['"]?\)/);
              if (urlMatch && urlMatch[1]) {
                return urlMatch[1];
              }
            }
            
            return null;
          };
          
          // Try multiple product selectors
          const productSelectors = [
            'tr[id*="rptproducts_tr"]',  // ASP.NET repeater table rows
            'div[id*="_itemsContainer"] > div',  // Container items
            '[class*="product-item"]',
            '[class*="product"]',
            '[class*="item"]',
            'table tr[id]',  // Table rows with IDs
            '[data-product]',
            'article',
            '[class*="card"]',
            '.product',
            '.item'
          ];
          
          let productElements = [];
          for (const selector of productSelectors) {
            const elements = document.querySelectorAll(selector);
            if (elements.length > 0) {
              productElements = Array.from(elements);
              break;
            }
          }
          
          // Alternative approach: Start with product images and build products around them
          if (productElements.length > 0) {
            // Try image-first approach for better results
            const productImages = document.querySelectorAll('img[id*="products"], img[id*="item"], img[src*="productsimages"], img[src*="ProductsImages"]');
            
            productImages.forEach((img, imgIdx) => {
              try {
                // Get image URL
                const image = getValidImageSrc(img);
                if (!image) return;
                
                // Find nearest container
                const container = img.closest('tr, div[class*="product"], div[class*="item"], div[id], td');
                if (!container) return;
                
                // Find product name/link in container
                const links = container.querySelectorAll('a[href]');
                let name = null;
                let url = null;
                let price = null;
                
                // Look for product link (usually contains product ID like i8085)
                for (const link of links) {
                  const href = link.getAttribute('href');
                  const text = link.textContent.trim();
                  if (href && href.includes('-i') && text && text.length > 3 && text.length < 200) {
                    name = text;
                    url = href;
                    break;
                  }
                }
                
                // If still no name, try any link with substantial text
                if (!name) {
                  for (const link of links) {
                    const text = link.textContent.trim();
                    if (text && text.length > 10 && text.length < 200) {
                      name = text;
                      url = link.getAttribute('href');
                      break;
                    }
                  }
                }
                
                // Look for price
                const priceElement = container.querySelector('[class*="price"], [id*="price"]');
                if (priceElement) {
                  const priceText = priceElement.textContent.trim();
                  const priceMatch = priceText.match(/[\d,\.]+/);
                  price = priceMatch ? priceMatch[0] : null;
                }
                
                if (name && image) {
                  extractedProducts.push({
                    name,
                    price,
                    category: categoryName,
                    url,
                    image
                  });
                }
              } catch (err) {
                // Skip problematic images
              }
            });
          }
          
          // If no product containers found, try to find individual product components
          if (productElements.length === 0) {
            // Look for images with product-like patterns
            const allImages = document.querySelectorAll('img[alt]');
            const allLinks = document.querySelectorAll('a[href]');
            
            // Try to build products from visible links with text
            allLinks.forEach(link => {
              const text = link.textContent.trim();
              const href = link.getAttribute('href');
              
              if (text && text.length > 3 && text.length < 200 && href) {
                // Look for price near this link
                let price = null;
                const parent = link.closest('[class*="product"], [class*="item"], div');
                if (parent) {
                  const priceElement = parent.querySelector('[class*="price"], [class*="cost"], .price');
                  if (priceElement) {
                    const priceText = priceElement.textContent.trim();
                    const priceMatch = priceText.match(/[\d,\.]+/);
                    price = priceMatch ? priceMatch[0] : null;
                  }
                }
                
                // Find associated image - check multiple attributes and locations
                let image = null;
                let img = null;
                
                // Strategy 1: Inside the link itself
                img = link.querySelector('img');
                
                // Strategy 2: In the parent row/container (look up the tree)
                if (!img) {
                  let currentElement = link.parentElement;
                  let depth = 0;
                  while (currentElement && depth < 5 && !img) {
                    img = currentElement.querySelector('img');
                    if (img) break;
                    currentElement = currentElement.parentElement;
                    depth++;
                  }
                }
                
                // Strategy 3: Look for closest table row
                if (!img) {
                  const row = link.closest('tr');
                  if (row) {
                    img = row.querySelector('img');
                  }
                }
                
                // Strategy 4: Look in nearest divs
                if (!img) {
                  const nearestDiv = link.closest('div[class], div[id]');
                  if (nearestDiv) {
                    img = nearestDiv.querySelector('img');
                  }
                }
                
                if (img) {
                  image = getValidImageSrc(img);
                }
                
                if (text && !text.includes('בצ') && !text.includes('סגור')) { // Filter out UI text
                  extractedProducts.push({
                    name: text,
                    price: price,
                    category: categoryName,
                    url: href,
                    image: image
                  });
                }
              }
            });
          } else {
            // Process found product elements
            productElements.forEach((element, idx) => {
              try {
                // Try to find product name
                const nameElement = element.querySelector('[class*="name"], [class*="title"], h2, h3, h4, a[href]');
                const name = nameElement ? nameElement.textContent.trim() : null;

                // Try to find price
                const priceElement = element.querySelector('[class*="price"], [class*="cost"], .price');
                let price = null;
                if (priceElement) {
                  const priceText = priceElement.textContent.trim();
                  const priceMatch = priceText.match(/[\d,\.]+/);
                  price = priceMatch ? priceMatch[0] : null;
                }

                // Try to find product link
                const linkElement = element.querySelector('a');
                const url = linkElement ? linkElement.getAttribute('href') : null;

                // Try to find product image - search broadly in the element tree
                let imageElement = element.querySelector('img');
                
                // If not found in current element, search in parent/siblings
                if (!imageElement && element.parentElement) {
                  imageElement = element.parentElement.querySelector('img');
                }
                
                // Try searching in nearest container
                if (!imageElement) {
                  const container = element.closest('tr, div[class], div[id]');
                  if (container) {
                    imageElement = container.querySelector('img');
                  }
                }
                
                let image = null;
                if (imageElement) {
                  image = getValidImageSrc(imageElement);
                }

                
                // Only add if we have at least a name
                if (name && name.length > 3) {
                  extractedProducts.push({
                    name,
                    price,
                    category: categoryName,
                    url,
                    image
                  });
                }
              } catch (err) {
                // Skip problematic elements
              }
            });
          }
          
          
          // Remove duplicates based on name
          const uniqueProducts = [];
          const seen = new Set();
          extractedProducts.forEach(product => {
            if (!seen.has(product.name)) {
              seen.add(product.name);
              uniqueProducts.push(product);
            }
          });

          return uniqueProducts;
        }, category.name);

        // Filter products to only include those with both image AND price
        // Also exclude products with the default Nitzat logo image (placeholder)
        const placeholderImages = [
          'Q659875_80_40.png',  // Nitzat logo
          'productsimages/mfrimages/thumbs/Q659875_80_40.png'
        ];
        
        const completeProducts = products.filter(product => 
          product.image && product.image.trim() !== '' &&
          product.price && product.price.trim() !== '' &&
          !placeholderImages.some(placeholder => product.image.includes(placeholder))
        );
        
        // First, deduplicate within this category's products
        const categoryUniqueProducts = [];
        const categoryImages = new Set();
        for (const product of completeProducts) {
          if (!categoryImages.has(product.image) && !usedImages.has(product.image)) {
            categoryImages.add(product.image);
            categoryUniqueProducts.push(product);
          }
        }
        
        console.log(`   ✓ Found ${products.length} products in ${category.name} (${completeProducts.length} with complete data, ${categoryUniqueProducts.length} with unique images)`);
        
        // Add products up to the maximum limit and track their images
        const remainingSlots = CONFIG.maxProducts - allProducts.length;
        const productsToAdd = categoryUniqueProducts.slice(0, remainingSlots);
        
        // Track the images we're adding
        productsToAdd.forEach(product => {
          usedImages.add(product.image);
        });
        
        allProducts.push(...productsToAdd);
        
        if (allProducts.length >= CONFIG.maxProducts) {
          console.log(`   🎯 Reached maximum of ${CONFIG.maxProducts} products!`);
        }

      } catch (error) {
        console.error(`   ✗ Error scraping category ${category.name}:`, error.message);
      }
    }

    // Final deduplication pass - ensure absolutely no duplicate images
    const finalProducts = [];
    const finalUsedImages = new Set();
    
    for (const product of allProducts) {
      if (!finalUsedImages.has(product.image)) {
        finalUsedImages.add(product.image);
        finalProducts.push(product);
      }
    }
    
    console.log(`\n🔍 Final deduplication: ${allProducts.length} → ${finalProducts.length} unique image products`);

    // Save results to JSON file
    const outputPath = path.join(CONFIG.outputDir, CONFIG.outputFile);
    const output = {
      scrapedAt: new Date().toISOString(),
      totalProducts: finalProducts.length,
      products: finalProducts
    };

    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');
    
    console.log(`\n✅ Scraping completed!`);
    console.log(`📊 Total products scraped: ${allProducts.length}`);
    console.log(`💾 Data saved to: ${outputPath}`);

  } catch (error) {
    console.error('❌ Error during scraping:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

// Run the scraper
if (require.main === module) {
  scrapeNitzatHaduvdevan()
    .then(() => {
      console.log('\n🎉 Scraper finished successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('\n💥 Scraper failed:', error);
      process.exit(1);
    });
}

module.exports = { scrapeNitzatHaduvdevan };

