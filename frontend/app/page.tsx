import { SearchPrompt } from "@/components/search-prompt"
import { Instructions } from "@/components/instructions"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24">
      <div className="w-full max-w-3xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white">Concert Scout AI</h1>
          <p className="text-lg text-gray-300">Discover live music events tailored to your taste ✨</p>
        </div>

        <Instructions type="above" />
        <SearchPrompt />
        <Instructions type="below" />
      </div>
    </main>
  )
}
