// Test the parsing logic with the problematic AI response
const testResponse = `Okay, I have some concert recommendations for you in Seattle based on the Country genre!

Concerts for Your Top Genre (Country):
\`\`\`json
[
    {
        "venue_name": "999 Building - Seattle",
        "city_name": "Seattle",
        "name": "The High Seagrass (FREE with RSVP)",
        "date": "2025-08-06",
        "url": "https://www.ticketweb.com/event/the-high-seagrass-free-with-999-building-seattle-tickets/13795344",
        "image_url": "https://s1.ticketm.net/dam/c/677/c58dd0af-cda8-49b2-bdaf-068540c3a677_106541_CUSTOM.jpg",
        "description": "The High Seagrass is playing a free show at the 999 Building in Seattle. This is a great opportunity to see some live country music without breaking the bank!"
    }
]
\`\`\`
Unfortunately, there are no concerts for your top artists and related artists in Seattle at this time.`;

console.log('Response structure analysis:');
console.log('Contains "Concerts for Your Top Genre":', testResponse.includes('Concerts for Your Top Genre'));
console.log('Contains "```json":', testResponse.includes('```json'));
console.log('Contains "```":', testResponse.includes('```'));

// Find the genre section
const genreSectionStart = testResponse.indexOf('Concerts for Your Top Genre');
console.log('Genre section starts at:', genreSectionStart);

if (genreSectionStart !== -1) {
  const genreSection = testResponse.substring(genreSectionStart);
  console.log('Genre section content:');
  console.log(genreSection.substring(0, 200) + '...');
  
  // Test pattern that includes the markdown code blocks
  const patternWithMarkdown = /Concerts for Your Top Genre\s*\([^)]*\)\s*:\s*```json\s*(\[[\s\S]*?\])\s*```/i;
  const matchWithMarkdown = testResponse.match(patternWithMarkdown);
  console.log('Pattern with markdown match:', matchWithMarkdown ? 'SUCCESS' : 'FAILED');
  if (matchWithMarkdown) {
    console.log('Extracted JSON length:', matchWithMarkdown[1].length);
    console.log('First 100 chars of JSON:', matchWithMarkdown[1].substring(0, 100));
  }
}

// Test the regex patterns
console.log('\nTesting regex patterns...');

// Test the new parentheses pattern
const parenthesesPattern = /Concerts for Your Top Genre\s*\([^)]*\)\s*:\s*(\[[\s\S]*?\])(?=\s*Concerts for Your Related Artists|$)/i;
const match1 = testResponse.match(parenthesesPattern);
console.log('Parentheses pattern match:', match1 ? 'SUCCESS' : 'FAILED');
if (match1) {
  console.log('Extracted JSON length:', match1[1].length);
  console.log('First 100 chars of JSON:', match1[1].substring(0, 100));
}

// Test the standard pattern
const standardPattern = /Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])(?=\s*Concerts for Your Related Artists|$)/i;
const match2 = testResponse.match(standardPattern);
console.log('Standard pattern match:', match2 ? 'SUCCESS' : 'FAILED');

// Test the flexible pattern
const flexiblePattern = /Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])\s*/i;
const match3 = testResponse.match(flexiblePattern);
console.log('Flexible pattern match:', match3 ? 'SUCCESS' : 'FAILED');

// Test genre name extraction
const genreNamePattern = /Concerts for Your Top Genre\s*\(([^)]+)\)/i;
const genreMatch = testResponse.match(genreNamePattern);
console.log('Genre name extraction:', genreMatch ? genreMatch[1] : 'FAILED'); 