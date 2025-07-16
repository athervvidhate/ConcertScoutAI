import Link from "next/link"
import { Github, Linkedin} from "lucide-react"

export function Footer() {
  return (
    <div className="w-full py-8">
      <div className="flex flex-col items-center justify-center gap-3">
        <div className="text-sm text-gray-400 text-center">
          Created and Maintained by{" "}
          <Link 
            href="https://atherv.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-purple-400 hover:text-purple-300 transition-colors inline-flex items-center"
          >
            Atherv Vidhate
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-external-link h-3.5 w-3.5 ml-1 opacity-80"><path d="M18 13v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>
          </Link>
        </div>
        
        <div className="flex items-center gap-4">
          <Link
            href="https://github.com/athervvidhate"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
            aria-label="GitHub Profile"
          >
            <Github className="h-5 w-5" />
          </Link>
          
          <Link
            href="https://linkedin.com/in/athervvidhate"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-white transition-colors"
            aria-label="LinkedIn Profile"
          >
            <Linkedin className="h-5 w-5" />
          </Link>
        </div>
      </div>
    </div>
  )
} 