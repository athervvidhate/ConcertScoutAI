import { Users, Disc3, Zap, MapPin, Star, Music, Ticket } from "lucide-react"

interface InstructionsProps {
  type: "above" | "below"
}

export function Instructions({ type }: InstructionsProps) {
  if (type === "above") {
    return (
      <div className="space-y-4 text-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4 max-w-2xl mx-auto">
          <div className="flex items-center gap-2 bg-purple-500/10 border border-purple-500/20 rounded-full px-4 py-2">
            <Star className="h-5 w-5 text-purple-400" />
            <span className="text-purple-100 text-sm">Personalized concert recommendations</span>
          </div>
          <div className="flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2">
            <Music className="h-5 w-5 text-blue-400" />
            <span className="text-blue-100 text-sm">Search by artist, genre, or Spotify playlist</span>
          </div>
          <div className="flex items-center gap-2 bg-pink-500/10 border border-pink-500/20 rounded-full px-4 py-2">
            <MapPin className="h-5 w-5 text-pink-400" />
            <span className="text-pink-100 text-sm">Find shows near you or anywhere in the world</span>
          </div>
          <div className="flex items-center gap-2 bg-green-500/10 border border-green-500/20 rounded-full px-4 py-2">
            <Ticket className="h-5 w-5 text-green-400" />
            <span className="text-green-100 text-sm">Get ticket links and event details instantly</span>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 text-sm">
      <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 space-y-4">
        <h3 className="font-medium text-center text-lg text-white mb-2">Ways to search for concerts</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex flex-col items-start gap-2 p-4 rounded-lg bg-gradient-to-r from-purple-500/10 to-transparent hover:from-purple-500/20 transition-all duration-300">
            <div className="flex items-center gap-2 mb-1">
              <Users className="h-5 w-5 text-purple-400 flex-shrink-0" />
              <span className="font-medium text-white">Artist + Location</span>
            </div>
            <p className="text-gray-300">Find concerts for your favorite artists in a specific place.</p>
            <span className="px-2 py-1 bg-purple-500/20 text-purple-200 rounded border border-purple-500/30 text-xs font-mono break-all">"Taylor Swift in New York"</span>
          </div>
          <div className="flex flex-col items-start gap-2 p-4 rounded-lg bg-gradient-to-r from-blue-500/10 to-transparent hover:from-blue-500/20 transition-all duration-300">
            <div className="flex items-center gap-2 mb-1">
              <Disc3 className="h-5 w-5 text-blue-400 flex-shrink-0" />
              <span className="font-medium text-white">Genre + Location</span>
            </div>
            <p className="text-gray-300">Search by music genre and location for broader recommendations.</p>
            <span className="px-2 py-1 bg-blue-500/20 text-blue-200 rounded border border-blue-500/30 text-xs font-mono break-all">"Rock concerts in Austin"</span>
          </div>
          <div className="flex flex-col items-start gap-2 p-4 rounded-lg bg-gradient-to-r from-pink-500/10 to-transparent hover:from-pink-500/20 transition-all duration-300">
            <div className="flex items-center gap-2 mb-1">
              <Zap className="h-5 w-5 text-pink-400 flex-shrink-0" />
              <span className="font-medium text-white">Spotify Playlist + Location</span>
            </div>
            <p className="text-gray-300">Paste a public Spotify playlist URL with a location for personalized picks.</p>
            <span className="px-2 py-1 bg-pink-500/20 text-pink-200 rounded border border-pink-500/30 text-xs font-mono break-all max-w-full">"https://open.spotify.com/playlist/... in Los Angeles"</span>
          </div>
          <div className="flex flex-col items-start gap-2 p-4 rounded-lg bg-gradient-to-r from-green-500/10 to-transparent hover:from-green-500/20 transition-all duration-300">
            <div className="flex items-center gap-2 mb-1">
              <MapPin className="h-5 w-5 text-green-400 flex-shrink-0" />
              <span className="font-medium text-white">Multiple Artists + Location</span>
            </div>
            <p className="text-gray-300">Find concerts for several artists at once in your chosen city.</p>
            <span className="px-2 py-1 bg-green-500/20 text-green-200 rounded border border-green-500/30 text-xs font-mono break-all">"Drake and Kendrick Lamar concerts in London"</span>
          </div>
        </div>
      </div>
    </div>
  )
}
