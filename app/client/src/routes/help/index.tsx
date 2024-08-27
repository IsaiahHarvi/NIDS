import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/help/')({
  component: () => <div>Hello /help/!</div>
})