"use client"

import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Calendar, MapPin, Music, ExternalLink, Heart } from "lucide-react"
import { useState } from "react"

export interface Concert {
  id: string
  artist: string
  venue: string
  location: string
  date: string
  time: string
  genre: string
  imageUrl: string
  ticketUrl: string
  description: string
}

export function ConcertCard({ concert }: { concert: Concert }) {
  const [isLiked, setIsLiked] = useState(false)

  const formattedDate = new Date(concert.date).toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  })

  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800/50 overflow-hidden flex flex-col hover:border-gray-600 hover:scale-[1.02] hover:shadow-lg hover:shadow-purple-500/10 transition-all duration-300">
      <div className="relative h-48 w-full overflow-hidden">
        <Image
          src={concert.imageUrl || "/placeholder.svg"}
          alt={`${concert.artist} concert`}
          fill
          className="object-cover transition-transform duration-300 hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
        <button
          onClick={() => setIsLiked(!isLiked)}
          className="absolute top-3 right-3 p-2 rounded-full bg-black/50 hover:bg-black/70 hover:scale-110 transition-all duration-200"
        >
          <Heart
            className={`h-4 w-4 transition-all duration-200 ${isLiked ? "text-red-500 fill-red-500 scale-110" : "text-white hover:text-red-400"}`}
          />
        </button>
      </div>

      <div className="p-6 flex flex-col flex-grow">
        <h3 className="font-bold text-xl text-white mb-2 hover:text-purple-300 transition-colors duration-200">
          {concert.artist}
        </h3>
        <p className="text-gray-400 mb-4 font-medium">{concert.venue}</p>

        <div className="space-y-3 mb-4">
          <div className="flex items-center gap-3 text-sm hover:bg-purple-500/5 p-2 rounded transition-colors duration-200">
            <Calendar className="h-4 w-4 text-purple-400" />
            <span className="text-gray-300">
              {formattedDate} • {concert.time}
            </span>
          </div>
          <div className="flex items-center gap-3 text-sm hover:bg-blue-500/5 p-2 rounded transition-colors duration-200">
            <MapPin className="h-4 w-4 text-blue-400" />
            <span className="text-gray-300">{concert.location}</span>
          </div>
          <div className="flex items-center gap-3 text-sm hover:bg-pink-500/5 p-2 rounded transition-colors duration-200">
            <Music className="h-4 w-4 text-pink-400" />
            <span className="text-gray-300">{concert.genre}</span>
          </div>
        </div>

        <div className="mb-6 flex-grow">
          <p className="text-sm text-gray-400 leading-relaxed p-3 rounded-lg bg-gray-900/30 border border-gray-700 hover:border-gray-600 transition-colors duration-200 italic">
            {concert.description}
          </p>
        </div>

        <Button
          asChild
          className="w-full mt-auto bg-purple-600 hover:bg-purple-700 hover:scale-105 text-white font-medium transition-all duration-200"
        >
          <a
            href={concert.ticketUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2"
          >
            Get Tickets
            <ExternalLink className="h-4 w-4" />
          </a>
        </Button>
      </div>
    </div>
  )
}
