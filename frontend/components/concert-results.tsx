import { ConcertCard } from "@/components/concert-card"
import { AiChatBubble } from "@/components/ai-chat-bubble"
import { parseAiResponse, type ParsedConcerts } from "@/lib/parseAiResponse"
import type { Concert as CardConcert } from "@/components/concert-card"
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem
} from "@/components/ui/select"
import { useState } from "react"

function getGridClasses(itemCount: number) {
  if (itemCount === 1) {
    return "grid grid-cols-1 max-w-md mx-auto"
  } else if (itemCount === 2) {
    return "grid grid-cols-1 md:grid-cols-2 gap-6"
  } else {
    return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
  }
}

const SORT_OPTIONS = [
  { value: "date", label: "Date" },
  { value: "artist", label: "Artist" },
  { value: "venue", label: "Venue" }
]

function sortConcerts(concerts: CardConcert[], sortBy: string): CardConcert[] {
  if (!Array.isArray(concerts)) return [];
  return [...concerts].sort((a, b) => {
    if (sortBy === "date") {
      // Try to parse as date, fallback to string compare
      const dateA = Date.parse(a.date) || 0;
      const dateB = Date.parse(b.date) || 0;
      return dateA - dateB;
    } else if (sortBy === "artist") {
      return a.artist.localeCompare(b.artist);
    } else if (sortBy === "venue") {
      return a.venue.localeCompare(b.venue);
    }
    return 0;
  });
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
  const [sortBy, setSortBy] = useState("date");
  // Parse the AI response to get actual concert data
  const parsedData: ParsedConcerts = parseAiResponse(aiResponse);
    
  // Only use parsed data from the AI response, no fallback to mock data
  const concerts = {
    topArtists: parsedData.topArtists.length > 0 ? parsedData.topArtists.map(concert => ({
      ...concert,
      time: concert.time ?? "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    }) as CardConcert) : [],
    topGenre: parsedData.topGenre.length > 0 ? parsedData.topGenre.map(concert => ({
      ...concert,
      time: concert.time ?? "8:00 PM",
      genre: concert.genre || parsedData.topGenreName || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    }) as CardConcert) : [],
    relatedArtists: parsedData.relatedArtists.length > 0 ? parsedData.relatedArtists.map(concert => ({
      ...concert,
      time: concert.time ?? "8:00 PM",
      genre: concert.genre || "Music",
      imageUrl: concert.imageUrl || "/placeholder.svg?height=300&width=500"
    }) as CardConcert) : [],
  };

  // Apply sorting
  const sortedConcerts = {
    topArtists: sortConcerts(concerts.topArtists, sortBy),
    topGenre: sortConcerts(concerts.topGenre, sortBy),
    relatedArtists: sortConcerts(concerts.relatedArtists, sortBy),
  };

  const hasResults =
    sortedConcerts.topArtists.length > 0 || sortedConcerts.topGenre.length > 0 || sortedConcerts.relatedArtists.length > 0

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
      {/* Sort By Dropdown */}
      <div className="flex justify-end mb-4">
        <div className="w-48">
          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger>
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              {SORT_OPTIONS.map(option => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {sortedConcerts.topArtists.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <AiChatBubble 
            title="Top Artists"
            message={`I found ${sortedConcerts.topArtists.length} concerts for your favorite artists!`}
          />
          <div className={getGridClasses(sortedConcerts.topArtists.length)}>
            {sortedConcerts.topArtists.map((concert, index) => (
              <div key={concert.id} className="animate-slide-up" style={{ animationDelay: `${0.2 + index * 0.1}s` }}>
                <ConcertCard concert={concert} />
              </div>
            ))}
          </div>
        </div>
      )}

      {sortedConcerts.topGenre.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.3s" }}>
          <AiChatBubble 
            title="Top Genre"
            message={`Here are ${sortedConcerts.topGenre.length} great ${sortedConcerts.topGenre[0]?.genre || 'genre'} concerts you might enjoy!`}
          />
          <div className={getGridClasses(sortedConcerts.topGenre.length)}>
            {sortedConcerts.topGenre.map((concert, index) => (
              <div key={concert.id} className="animate-slide-up" style={{ animationDelay: `${0.4 + index * 0.1}s` }}>
                <ConcertCard concert={concert} />
              </div>
            ))}
          </div>
        </div>
      )}

      {sortedConcerts.relatedArtists.length > 0 && (
        <div className="space-y-6 animate-fade-in" style={{ animationDelay: "0.5s" }}>
          <AiChatBubble 
            title="Related Artists"
            message={`I discovered ${sortedConcerts.relatedArtists.length} concerts from artists similar to your favorites!`}
          />
          <div className={getGridClasses(sortedConcerts.relatedArtists.length)}>
            {sortedConcerts.relatedArtists.map((concert, index) => (
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
