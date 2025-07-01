export interface Concert {
  id: string;
  artist: string;
  venue: string;
  location: string;
  date: string;
  time?: string;
  genre?: string;
  imageUrl?: string;
  ticketUrl: string;
  description: string;
}

export interface ParsedConcerts {
  topArtists: Concert[];
  topGenre: Concert[];
  relatedArtists: Concert[];
  aiSections: {
    topArtistsText: string;
    topGenreText: string;
    relatedArtistsText: string;
  };
  topGenreName?: string;
  isFollowUpQuestion?: boolean;
  followUpMessage?: string;
}

interface ApiConcert {
  name: string;
  venue_name: string;
  city_name: string;
  date: string;
  url: string;
  image_url: string;
  description: string;
}

export function parseAiResponse(aiResponse: string): ParsedConcerts {
  const result: ParsedConcerts = {
    topArtists: [],
    topGenre: [],
    relatedArtists: [],
    aiSections: {
      topArtistsText: '',
      topGenreText: '',
      relatedArtistsText: ''
    }
  };

  try {
    // Decode URL-encoded response if needed
    let decodedResponse = aiResponse;

    
    console.log('Parsing AI response:', decodedResponse);
    
    // Check if this is a follow-up question
    if (isFollowUpQuestion(decodedResponse)) {
      console.log('Detected follow-up question');
      result.isFollowUpQuestion = true;
      result.followUpMessage = decodedResponse.trim();
      return result;
    }
    
    // Parse the new format with sections
    const sections = parseNewFormat(decodedResponse);
    
    // Convert API format to Concert format
    result.topArtists = sections.topArtists.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'artists')
    );
    
    result.topGenre = sections.topGenre.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'genre', sections.topGenreName)
    );
    
    result.relatedArtists = sections.relatedArtists.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'related')
    );
    
    // Extract AI commentary
    result.aiSections.topArtistsText = sections.topArtistsText;
    result.aiSections.topGenreText = sections.topGenreText;
    result.aiSections.relatedArtistsText = sections.relatedArtistsText;
    
    // Set the genre name
    result.topGenreName = sections.topGenreName;
    
    console.log('Parsed result:', result);

  } catch (error) {
    console.error('Error parsing AI response:', error);
  }

  return result;
}

function isFollowUpQuestion(response: string): boolean {
  const hasJsonBlocks = response.includes('```json');
  const isQuestion = response.includes('?') || 
                    response.toLowerCase().includes('need') ||
                    response.toLowerCase().includes('provide') ||
                    response.toLowerCase().includes('specify') ||
                    response.toLowerCase().includes('can you') ||
                    response.toLowerCase().includes('sorry') ||
                    response.toLowerCase().includes('unable') ||
                    response.toLowerCase().includes('cannot');
  
  // If no JSON blocks and it's a question or error response, it's likely a follow-up
  return !hasJsonBlocks && isQuestion && response.trim().length < 1000;
}

function parseNewFormat(response: string): {
  topArtists: ApiConcert[];
  topGenre: ApiConcert[];
  relatedArtists: ApiConcert[];
  topArtistsText: string;
  topGenreText: string;
  relatedArtistsText: string;
  topGenreName: string;
} {
  const result = {
    topArtists: [] as ApiConcert[],
    topGenre: [] as ApiConcert[],
    relatedArtists: [] as ApiConcert[],
    topArtistsText: '',
    topGenreText: '',
    relatedArtistsText: '',
    topGenreName: ''
  };

  // Extract sections using the new format
  const sections = extractSections(response);
  
  console.log('Extracted sections:', {
    topArtists: sections.topArtists ? `${sections.topArtists.substring(0, 100)}...` : 'empty',
    topGenre: sections.topGenre ? `${sections.topGenre.substring(0, 100)}...` : 'empty',
    relatedArtists: sections.relatedArtists ? `${sections.relatedArtists.substring(0, 100)}...` : 'empty'
  });
  
  // Parse each section
  result.topArtists = parseConcertSection(sections.topArtists);
  result.topGenre = parseConcertSection(sections.topGenre);
  result.relatedArtists = parseConcertSection(sections.relatedArtists);
  
  // Extract AI commentary
  result.topArtistsText = extractAICommentary(sections.topArtistsRaw);
  result.topGenreText = extractAICommentary(sections.topGenreRaw);
  result.relatedArtistsText = extractAICommentary(sections.relatedArtistsRaw);
  
  // Extract genre name from the section header
  result.topGenreName = extractGenreName(sections.topGenreRaw);

  return result;
}

function extractSections(response: string) {
  const sections = {
    topArtists: '',
    topGenre: '',
    relatedArtists: '',
    topArtistsRaw: '',
    topGenreRaw: '',
    relatedArtistsRaw: ''
  };

  console.log('Looking for sections in response...');
  console.log('Response length:', response.length);
  console.log('Response contains "Concerts for Your Top Artists":', response.includes('Concerts for Your Top Artists'));
  console.log('Response contains "Concerts for Your Top Genre":', response.includes('Concerts for Your Top Genre'));
  console.log('Response contains "Concerts for Your Related Artists":', response.includes('Concerts for Your Related Artists'));

  // Look for the main artist section (e.g., "Concerts for Your Top Artists:")
  const mainArtistMatch = response.match(/Concerts for Your Top Artists:\s*(\[[\s\S]*?\])(?=\s*Concerts for Your Top Genre|$)/i);
  if (mainArtistMatch) {
    console.log('Found top artists section');
    sections.topArtistsRaw = mainArtistMatch[0];
    sections.topArtists = mainArtistMatch[1];
  } else {
    console.log('No top artists section found');
  }

  // Look for genre section
  // This logic is not great and should be improved
  const genreMatch = response.match(/Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])(?=\s*Concerts for Your Related Artists|$)/i);
  if (genreMatch) {
    console.log('Found genre section');
    sections.topGenreRaw = genreMatch[0];
    sections.topGenre = genreMatch[1];
  } else {
    console.log('No genre section found with first pattern, trying alternative...');
    // Try a more flexible pattern for genre section that doesn't require following sections
    const genreMatch2 = response.match(/Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])\s*Concerts for Your Related Artists/i);
    if (genreMatch2) {
      console.log('Found genre section with alternative pattern');
      sections.topGenreRaw = genreMatch2[0].replace(/\s*Concerts for Your Related Artists.*$/, '');
      sections.topGenre = genreMatch2[1];
    } else {
      // Try a pattern that just looks for the genre section anywhere in the response
      const genreMatch3 = response.match(/Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])\s*$/i);
      if (genreMatch3) {
        console.log('Found genre section with end-of-response pattern');
        sections.topGenreRaw = genreMatch3[0];
        sections.topGenre = genreMatch3[1];
      } else {
        // Last resort: try to find any JSON array after "Concerts for Your Top Genre"
        const genreMatch4 = response.match(/Concerts for Your Top Genre[^:]*:\s*(\[[\s\S]*?\])\s*/i);
        if (genreMatch4) {
          console.log('Found genre section with last resort pattern');
          sections.topGenreRaw = genreMatch4[0];
          sections.topGenre = genreMatch4[1];
        }
      }
    }
  }

  // Look for related artists section
  const relatedMatch = response.match(/Concerts for Your Related Artists:\s*(\[[\s\S]*?\])(?=\s*$)/i);
  if (relatedMatch) {
    console.log('Found related artists section');
    sections.relatedArtistsRaw = relatedMatch[0];
    sections.relatedArtists = relatedMatch[1];
  } else {
    console.log('No related artists section found');
  }

  return sections;
}

function parseConcertSection(jsonString: string): ApiConcert[] {
  if (!jsonString.trim()) return [];
  
  try {
    const concerts: ApiConcert[] = JSON.parse(jsonString);
    return concerts;
  } catch (error) {
    console.error('Error parsing concert section:', error);
    return [];
  }
}

function extractAICommentary(sectionText: string): string {
  if (!sectionText) return '';
  
  // Extract text before the JSON array
  const beforeJson = sectionText.split('```json')[0];
  
  // Clean up the text by removing section headers
  const cleaned = beforeJson
    .replace(/Concerts for [^:]+:/i, '')
    .replace(/Concerts for Your Top Genre[^:]*:/i, '')
    .replace(/Concerts for Your Related Artists:/i, '')
    .trim();
  
  return cleaned || 'Here are some great concert recommendations for you!';
}

function extractGenreName(sectionText: string): string {
  if (!sectionText) return '';
  
  // Look for genre name in parentheses after "Concerts for Your Top Genre"
  const genreMatch = sectionText.match(/Concerts for Your Top Genre\s*\(([^)]+)\)/i);
  if (genreMatch) {
    return genreMatch[1].trim();
  }
  
  return '';
}

function convertApiConcertToConcert(apiConcert: ApiConcert, index: number, category: string, genre?: string): Concert {
  const formattedDate = formatDate(apiConcert.date);
  
  return {
    id: `${category}-${index}-${Date.now()}-${Math.random()}`,
    artist: apiConcert.name,
    venue: apiConcert.venue_name,
    location: apiConcert.city_name,
    date: formattedDate,
    ticketUrl: apiConcert.url,
    description: apiConcert.description, // Use the description from the API response
    imageUrl: apiConcert.image_url,
    genre: genre
  };
}

function formatDate(dateStr: string): string {
  try {
    if (dateStr.includes('-')) {
      const date = new Date(dateStr);
      if (!isNaN(date.getTime())) {
        return date.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        });
      }
    }
    return dateStr;
  } catch {
    return dateStr;
  }
} 