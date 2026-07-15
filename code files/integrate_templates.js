const fs = require('fs');

// Read the generated HTML files
const homeHtml = fs.readFileSync('app/static/stitch_home.html', 'utf8');
const formHtml = fs.readFileSync('app/static/stitch_form.html', 'utf8');
const aboutHtml = fs.readFileSync('app/static/stitch_about.html', 'utf8');

// Helper to add Flask header
function addFlaskHeader(html, title) {
  const flaskHeader = `
    <title>${title}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">`;
  
  return html.replace(/<title>[^<]*<\/title>/, flaskHeader);
}

// Helper to fix navigation links for Flask
function fixNavLinks(html) {
  return html
    .replace(/<a[^>]*href="#"[^>]*class="[^"]*"[^>]*>Platform<\/a>/, 
      '<a href="/" class="text-primary border-b-2 border-primary pb-1">Home</a>')
    .replace(/<a[^>]*href="#"[^>]*>Analysis<\/a>/, 
      '<a href="/find_your_crop" class="text-on-surface-variant hover:text-on-surface">Find Your Crop</a>')
    .replace(/<a[^>]*href="#"[^>]*>Sustainability<\/a>/, 
      '<a href="/about" class="text-on-surface-variant hover:text-on-surface">About</a>')
    .replace(/<a[^>]*href="#"[^>]*>Insights<\/a>/, 
      '<a href="/history" class="text-on-surface-variant hover:text-on-surface">History</a>')
    .replace(/<button[^>]*>Get Started<\/button>/, 
      '<a href="/find_your_crop" class="bg-primary-container text-on-primary-container px-lg py-sm rounded-lg font-bold hover:opacity-80 transition-all active:scale-95">Find Your Crop</a>');
}

// Process Home template
let homeTemplate = homeHtml;
homeTemplate = addFlaskHeader(homeTemplate, 'OptiCrop - Smart Agricultural Production Optimization');
homeTemplate = fixNavLinks(homeTemplate);
// Add active class to Home nav
homeTemplate = homeTemplate.replace(
  'class="text-primary border-b-2 border-primary pb-1"',
  'class="text-primary border-b-2 border-primary pb-1"'
);
fs.writeFileSync('app/templates/index.html', homeTemplate);
console.log('Home template saved');

// Process Form template
let formTemplate = formHtml;
formTemplate = addFlaskHeader(formTemplate, 'Find Your Crop - OptiCrop');
formTemplate = fixNavLinks(formTemplate);
// Add active class to Find Your Crop nav
formTemplate = formTemplate.replace(
  'href="/find_your_crop" class="text-on-surface-variant hover:text-on-surface"',
  'href="/find_your_crop" class="text-primary border-b-2 border-primary pb-1"'
);
fs.writeFileSync('app/templates/find_your_crop.html', formTemplate);
console.log('Form template saved');

// Process About template
let aboutTemplate = aboutHtml;
aboutTemplate = addFlaskHeader(aboutTemplate, 'About - OptiCrop');
aboutTemplate = fixNavLinks(aboutTemplate);
// Add active class to About nav
aboutTemplate = aboutTemplate.replace(
  'href="/about" class="text-on-surface-variant hover:text-on-surface"',
  'href="/about" class="text-primary border-b-2 border-primary pb-1"'
);
fs.writeFileSync('app/templates/about.html', aboutTemplate);
console.log('About template saved');

console.log('\nAll templates integrated with Stitch designs!');
