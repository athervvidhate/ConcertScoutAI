import Link from "next/link"
import { Github, Linkedin} from "lucide-react"

export function Footer() {
  return (
    <div className="w-full py-8">
      <div className="flex flex-col items-center justify-center gap-3">
        <div className="text-sm text-gray-400 text-center">
          Created and Maintained by <span className="text-purple-400">Atherv Vidhate</span>{" "}
          {/* Leaving this commented until portfolio site is finished */}
          {/* <Link 
            href="https://atherv.com" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-purple-400 hover:text-purple-300 transition-colors"
          >
            Atherv Vidhate
          </Link> */}
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