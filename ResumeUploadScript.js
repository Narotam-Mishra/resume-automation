const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Helper function for random delays
const randomDelay = (min, max) => 
    new Promise(resolve => setTimeout(resolve, Math.random() * (max - min) + min));

(async () => {
    const username = process.env.NAUKRI_USERNAME;
    const password = process.env.NAUKRI_PASSWORD;
    
    if (!username || !password) {
        console.error("Missing credentials. Set NAUKRI_USERNAME and NAUKRI_PASSWORD environment variables.");
        process.exit(1);
    }
    
    console.log(`Starting the resume update process at ${new Date().toISOString()}...`);
    
    let browser;
    let page;
    
    try {
        // Launch browser with debugging options
        browser = await puppeteer.launch({
            headless: false, // Set to true for production
            args: [
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--window-size=1920,1080',
                '--start-maximized'
            ],
            defaultViewport: null,
            slowMo: 100 // Slows down Puppeteer operations by 100ms
        });
        
        page = await browser.newPage();
        
        // Enable request interception to monitor network activity
        await page.setRequestInterception(true);
        page.on('request', request => request.continue());
        
        // Set user agent and enable console logging
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
        
        // Open Naukri
        console.log('Opening Naukri website...');
        await page.goto('https://www.naukri.com/', { 
            waitUntil: 'networkidle2',
            timeout: 60000 
        });
        await randomDelay(2000, 5000);
        
        // Check for CAPTCHA
        const pageContent = await page.content();
        if (pageContent.includes('CAPTCHA') || pageContent.includes('Access Denied')) {
            console.log('CAPTCHA or blocking detected. Please solve it manually.');
            await page.screenshot({ path: 'captcha-detected.png' });
            await randomDelay(60000, 70000);
        }
        
        // Login
        console.log('Clicking login button...');
        await page.waitForSelector("a[title='Jobseeker Login']", { timeout: 15000 });
        await page.click("a[title='Jobseeker Login']");
        await randomDelay(1000, 3000);
        
        console.log('Entering username...');
        await page.waitForSelector("input[placeholder='Enter your active Email ID / Username']", { timeout: 10000 });
        await page.type("input[placeholder='Enter your active Email ID / Username']", username, { delay: 100 });
        await randomDelay(1000, 3000);
        
        console.log('Entering password...');
        await page.type("input[placeholder='Enter your password']", password, { delay: 100 });
        await randomDelay(1000, 3000);
        
        console.log('Submitting login...');
        await page.click("button[type='submit']");
        
        // Verify login success
        try {
            await page.waitForSelector('.nI-gNb-drawer__bars', { timeout: 15000 });
            console.log('Login successful');
        } catch {
            await page.screenshot({ path: 'login-failed.png' });
            throw new Error('Login failed - check credentials or CAPTCHA');
        }
        
        await randomDelay(3000, 5000);

        // Option 1: Direct profile URL navigation (most reliable)
        console.log('Navigating directly to profile page...');
        await page.goto('https://www.naukri.com/mnjuser/profile', { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });
        
        // Option 2: Menu navigation (fallback if direct URL doesn't work)
        if (!page.url().includes('/profile')) {
            console.log('Falling back to menu navigation...');
            try {
                await page.waitForSelector(".nI-gNb-drawer__bars .nI-gNb-bar2", { timeout: 10000 });
                await page.click(".nI-gNb-drawer__bars .nI-gNb-bar2");
                await randomDelay(2000, 4000);
                
                await page.waitForSelector("a[href*='view-and-update-profile']", { timeout: 10000 });
                await page.click("a[href*='view-and-update-profile']");
                await randomDelay(3000, 5000);
            } catch (menuError) {
                console.error('Menu navigation failed:', menuError);
                throw menuError;
            }
        }

        // Update resume
        console.log('Clicking update resume button...');
        await page.waitForSelector("input[value='Update resume']", { timeout: 15000 });
        await page.click("input[value='Update resume']");
        await randomDelay(2000, 4000);
        
        console.log('Uploading resume file...');
        const resumePath = path.join(__dirname, 'utils', 'Narotam_Resume_Mar25.pdf');
        if (!fs.existsSync(resumePath)) {
            console.error(`Resume file not found at: ${resumePath}`);
            process.exit(1);
        }
        
        const fileInput = await page.$("input[type='file']");
        await fileInput.uploadFile(resumePath);
        
        // Wait for upload to complete
        await page.waitForSelector('.success-msg, .error-msg', { timeout: 30000 })
                  .catch(() => console.log('No upload status message detected'));
        
        await randomDelay(5000, 7000);
        
        console.log(`Resume updated successfully on Naukri at: ${new Date().toISOString()}`);
        await page.screenshot({ path: 'success.png' });
        process.exit(0);
    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const screenshotPath = `error_${timestamp}.png`;
        
        if (page) {
            await page.screenshot({ 
                path: screenshotPath,
                fullPage: true 
            });
            console.log(`Screenshot saved to: ${screenshotPath}`);
        }
        
        process.exit(1);
    } finally {
        if (browser) {
            console.log('Closing browser...');
            await browser.close();
        }
    }
})();