import { ConcertCard } from "@/components/concert-card"
import { AiChatBubble } from "@/components/ai-chat-bubble"
import { parseAiResponse, type ParsedConcerts } from "@/lib/parseAiResponse"

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
  
  // Only use parsed data from the AI response, no fallback to mock data
  const concerts = {
    topArtists: parsedData.topArtists.length > 0 ? parsedData.topArtists.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : [],
    topGenre: parsedData.topGenre.length > 0 ? parsedData.topGenre.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || parsedData.topGenreName || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : [],
    relatedArtists: parsedData.relatedArtists.length > 0 ? parsedData.relatedArtists.map(concert => ({
      ...concert,
      time: concert.time || "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    })) : [],
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
          <AiChatBubble 
            title="Top Artists"
            message={`I found ${concerts.topArtists.length} concerts for your favorite artists!`}
          />
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
          <AiChatBubble 
            title="Top Genre"
            message={`Here are ${concerts.topGenre.length} great ${concerts.topGenre[0]?.genre || 'genre'} concerts you might enjoy!`}
          />
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
          <AiChatBubble 
            title="Related Artists"
            message={`I discovered ${concerts.relatedArtists.length} concerts from artists similar to your favorites!`}
          />
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
