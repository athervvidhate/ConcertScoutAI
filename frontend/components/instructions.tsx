import { Music, Zap, Heart, MapPin } from "lucide-react"

interface InstructionsProps {
  type: "above" | "below"
}

export function Instructions({ type }: InstructionsProps) {
  if (type === "above") {
    return (
      <div className="space-y-4 text-center">
        <p className="text-gray-300 text-lg">Tell me what music you're interested in seeing live</p>
        <div className="flex flex-wrap justify-center gap-3 text-sm">
          <span className="px-3 py-2 bg-purple-500/20 text-purple-200 rounded-full border border-purple-500/30">
            "Indie rock bands in Austin"
          </span>
          <span className="px-3 py-2 bg-blue-500/20 text-blue-200 rounded-full border border-blue-500/30">
            "EDM festivals in Europe this summer"
          </span>
          <span className="px-3 py-2 bg-pink-500/20 text-pink-200 rounded-full border border-pink-500/30">
            "Concerts like Taylor Swift near New York"
          </span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 text-sm">
      <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-6 space-y-4">
        <h3 className="font-medium text-center text-lg text-white">How it works</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 to-transparent hover:from-purple-500/20 transition-all duration-300">
            <Music className="h-5 w-5 text-purple-400 flex-shrink-0" />
            <p className="text-gray-300">Enter artists, genres, or locations you're interested in</p>
          </div>
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-blue-500/10 to-transparent hover:from-blue-500/20 transition-all duration-300">
            <Zap className="h-5 w-5 text-blue-400 flex-shrink-0" />
            <p className="text-gray-300">Paste a Spotify playlist link to find concerts based on your music taste</p>
          </div>
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-pink-500/10 to-transparent hover:from-pink-500/20 transition-all duration-300">
            <MapPin className="h-5 w-5 text-pink-400 flex-shrink-0" />
            <p className="text-gray-300">Specify a location for more relevant results</p>
          </div>
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-green-500/10 to-transparent hover:from-green-500/20 transition-all duration-300">
            <Heart className="h-5 w-5 text-green-400 flex-shrink-0" />
            <p className="text-gray-300">Get personalized concert recommendations with ticket links</p>
          </div>
        </div>
      </div>
    </div>
  )
}
