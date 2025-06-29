export function ResultsSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 bg-muted rounded animate-pulse"></div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="rounded-lg border bg-card overflow-hidden">
            <div className="h-48 w-full bg-muted animate-pulse"></div>
            <div className="p-5 space-y-4">
              <div className="h-6 w-3/4 bg-muted rounded animate-pulse"></div>
              <div className="h-4 w-1/2 bg-muted rounded animate-pulse"></div>
              <div className="space-y-2">
                <div className="h-4 w-full bg-muted rounded animate-pulse"></div>
                <div className="h-4 w-full bg-muted rounded animate-pulse"></div>
                <div className="h-4 w-3/4 bg-muted rounded animate-pulse"></div>
              </div>
              <div className="h-10 w-full bg-muted rounded animate-pulse mt-4"></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
