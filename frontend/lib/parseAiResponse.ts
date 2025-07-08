export interface Concert {
  id: string;
  artist: string;
  venue: string;
  location: string;
  date: string;
  time: string;
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
  time: string;
  url: string;
  genre: string;
  image_url: string;
  description: string;
}

interface AiResponseSchema {
  concerts_for_top_artists: ApiConcert[];
  concerts_for_top_genre: ApiConcert[];
  concerts_for_related_artists: ApiConcert[];
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
    console.log('Parsing AI response:', aiResponse);
    
    // Check if this is a follow-up question
    if (isFollowUpQuestion(aiResponse)) {
      console.log('Detected follow-up question');
      result.isFollowUpQuestion = true;
      result.followUpMessage = aiResponse.trim();
      return result;
    }
    
    // Parse the JSON response
    const parsedResponse: AiResponseSchema = JSON.parse(aiResponse);
    
    // Convert API format to Concert format
    result.topArtists = parsedResponse.concerts_for_top_artists.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'artists')
    );
    
    result.topGenre = parsedResponse.concerts_for_top_genre.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'genre')
    );
    
    result.relatedArtists = parsedResponse.concerts_for_related_artists.map((concert, index) => 
      convertApiConcertToConcert(concert, index, 'related')
    );
    
    // Set default AI commentary
    result.aiSections.topArtistsText = 'Here are concerts featuring your top artists!';
    result.aiSections.topGenreText = 'Here are concerts in your favorite genre!';
    result.aiSections.relatedArtistsText = 'Here are concerts by artists similar to your favorites!';
    
  } catch (error) {
    console.error('Error parsing AI response:', error);
  }

  return result;
}

function isFollowUpQuestion(response: string): boolean {
  // Check if it's not valid JSON and contains question indicators
  try {
    JSON.parse(response);
    return false; // Valid JSON, not a follow-up question
  } catch {
    // Not valid JSON, check if it's a question
    const isQuestion = response.includes('?') || 
                      response.toLowerCase().includes('need') ||
                      response.toLowerCase().includes('provide') ||
                      response.toLowerCase().includes('specify') ||
                      response.toLowerCase().includes('can you') ||
                      response.toLowerCase().includes('sorry') ||
                      response.toLowerCase().includes('unable') ||
                      response.toLowerCase().includes('cannot');
    
    return isQuestion && response.trim().length < 1000;
  }
}

function convertApiConcertToConcert(apiConcert: ApiConcert, index: number, category: string): Concert {
  const formattedDate = formatDate(apiConcert.date);
  const formattedTime = formatTime(apiConcert.time);
  
  return {
    id: `${category}-${index}-${Date.now()}-${Math.random()}`,
    artist: apiConcert.name,
    venue: apiConcert.venue_name,
    location: apiConcert.city_name,
    date: formattedDate,
    time: formattedTime,
    ticketUrl: apiConcert.url,
    genre: apiConcert.genre,
    description: apiConcert.description,
    imageUrl: apiConcert.image_url
  };
}

function formatDate(dateStr: string): string {
  try {
    if (dateStr.includes('-')) {
      // Handle YYYY-MM-DD format by parsing as local date to avoid timezone issues
      if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const [year, month, day] = dateStr.split('-').map(Number);
        const date = new Date(year, month - 1, day); // month is 0-indexed
        return date.toLocaleDateString('en-US', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        });
      } else {
        // Fallback for other date formats
        const date = new Date(dateStr);
        if (!isNaN(date.getTime())) {
          return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          });
        }
      }
    }
    return dateStr;
  } catch {
    return dateStr;
  }
}

function formatTime(timeStr: string): string {
  try {
    // Handle HH:MM:SS format (e.g., "18:00:00")
    if (timeStr.match(/^\d{1,2}:\d{2}:\d{2}$/)) {
      const [hours, minutes] = timeStr.split(':').map(Number);
      const date = new Date();
      date.setHours(hours, minutes, 0);
      
      return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
    }
    
    // Handle HH:MM format (e.g., "18:00")
    if (timeStr.match(/^\d{1,2}:\d{2}$/)) {
      const [hours, minutes] = timeStr.split(':').map(Number);
      const date = new Date();
      date.setHours(hours, minutes, 0);
      
      return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
    }
    
    // If it's already in a readable format, return as is
    return timeStr;
  } catch {
    return timeStr;
  }
}