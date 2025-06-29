import { ConcertCard } from "@/components/concert-card"
import { Music, Users, Sparkles } from "lucide-react"
import { apiService } from "@/lib/api"
import { parseAiResponse, type ParsedConcerts } from "@/lib/parseAiResponse"

// Mock data remains as fallback
const MOCK_CONCERTS = {
  topArtists: [
    {
      id: "1",
      artist: "The National",
      venue: "Madison Square Garden",
      location: "New York, NY",
      date: "2025-07-15",
      time: "8:00 PM",
      genre: "Indie Rock",
      imageUrl: "/placeholder.svg?height=300&width=500",
      ticketUrl: "https://example.com/tickets/1",
      description:
        "Perfect match for your indie rock taste - The National's atmospheric sound and introspective lyrics align with your music preferences.",
    },
    {
      id: "2",
      artist: "Arcade Fire",
      venue: "Brooklyn Bowl",
      location: "Brooklyn, NY",
      date: "2025-08-02",
      time: "9:00 PM",
      genre: "Indie Rock",
      imageUrl: "/placeholder.svg?height=300&width=500",
      ticketUrl: "https://example.com/tickets/2",
      description:
        "Their energetic live performances and anthemic indie rock sound make this a must-see show for fans of the genre.",
    },
  ],
  topGenre: [
    {
      id: "3",
      artist: "Vampire Weekend",
      venue: "Terminal 5",
      location: "New York, NY",
      date: "2025-07-28",
      time: "8:30 PM",
      genre: "Indie Rock",
      imageUrl: "/placeholder.svg?height=300&width=500",
      ticketUrl: "https://example.com/tickets/3",
      description:
        "A standout indie rock act known for their sophisticated songwriting and unique blend of preppy aesthetics with world music influences.",
    },
    {
      id: "4",
      artist: "MGMT",
      venue: "Webster Hall",
      location: "New York, NY",
      date: "2025-08-12",
      time: "7:30 PM",
      genre: "Indie Rock",
      imageUrl: "/placeholder.svg?height=300&width=500",
      ticketUrl: "https://example.com/tickets/4",
      description:
        "Their psychedelic indie rock sound and experimental approach make them a perfect fit for adventurous indie music lovers.",
    },
  ],
  relatedArtists: [
    {
      id: "5",
      artist: "Interpol",
      venue: "Bowery Ballroom",
      location: "New York, NY",
      date: "2025-09-05",
      time: "8:00 PM",
      genre: "Post-Punk Revival",
      imageUrl: "/placeholder.svg?height=300&width=500",
      ticketUrl: "https://example.com/tickets/5",
      description:
        "Based on your taste for moody indie rock, Interpol's dark, driving post-punk sound should resonate perfectly with you.",
    },
  ],
}

function getGridClasses(itemCount: number) {
  if (itemCount === 1) {
    return "grid grid-cols-1 max-w-md mx-auto"
  } else if (itemCount === 2) {
    return "grid grid-cols-1 md:grid-cols-2 gap-6"
  } else {
    return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
  }
}

export function ConcertResults({ 
  query, 
  aiResponse, 
  sessionId 
}: { 
  query: string; 
  aiResponse: string;
  sessionId?: string;
}) {
  console.log('ConcertResults received aiResponse:', aiResponse); // Debug log
  
  // Parse the AI response to get actual concert data
  const parsedData: ParsedConcerts = parseAiResponse(aiResponse);
  
  console.log('Parsed concert data:', parsedData); // Debug log
  
  // Use parsed data if available, otherwise fall back to mock data
  const concerts = {
    topArtists: parsedData.topArtists.length > 0 ? parsedData.topArtists.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : MOCK_CONCERTS.topArtists,
    topGenre: parsedData.topGenre.length > 0 ? parsedData.topGenre.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : MOCK_CONCERTS.topGenre,
    relatedArtists: parsedData.relatedArtists.length > 0 ? parsedData.relatedArtists.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : MOCK_CONCERTS.relatedArtists,
  };

  const hasResults =
    concerts.topArtists.length > 0 || concerts.topGenre.length > 0 || concerts.relatedArtists.length > 0

  if (!hasResults) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-medium text-white mb-4">No concerts found</h2>
        <p className="text-gray-400">Try broadening your search or check back later for new events.</p>
      </div>
    )
  }

  return (
    <div className="space-y-12">
      {concerts.topArtists.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <div className="flex items-center gap-3">
            <Users className="h-6 w-6 text-purple-400" />
            <h2 className="text-2xl font-bold text-purple-400">Concerts for Top Artists</h2>
          </div>
          <div className={getGridClasses(concerts.topArtists.length)}>
            {concerts.topArtists.map((concert, index) => (
              <div key={concert.id} className="animate-slide-up" style={{ animationDelay: `${0.2 + index * 0.1}s` }}>
                <ConcertCard concert={concert} />
              </div>
            ))}
          </div>
        </div>
      )}

      {concerts.topGenre.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.3s" }}>
          <div className="flex items-center gap-3">
            <Music className="h-6 w-6 text-blue-400" />
            <h2 className="text-2xl font-bold text-blue-400">Top Genre Concerts</h2>
          </div>
          <div className={getGridClasses(concerts.topGenre.length)}>
            {concerts.topGenre.map((concert, index) => (
              <div key={concert.id} className="animate-slide-up" style={{ animationDelay: `${0.4 + index * 0.1}s` }}>
                <ConcertCard concert={concert} />
              </div>
            ))}
          </div>
        </div>
      )}

      {concerts.relatedArtists.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.5s" }}>
          <div className="flex items-center gap-3">
            <Sparkles className="h-6 w-6 text-pink-400" />
            <h2 className="text-2xl font-bold text-pink-400">Recommended Related Artists</h2>
          </div>
          <div className={getGridClasses(concerts.relatedArtists.length)}>
            {concerts.relatedArtists.map((concert, index) => (
              <div key={concert.id} className="animate-slide-up" style={{ animationDelay: `${0.6 + index * 0.1}s` }}>
                <ConcertCard concert={concert} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
