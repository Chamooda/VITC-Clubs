import { Button } from '@/components/ui/button';
import { CalendarIcon, HandshakeIcon, UsersIcon } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex flex-col items-center">
      {/* Hero Section */}
      <section className="w-full py-12 md:py-24 lg:py-32 bg-background">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-4 text-center">
            <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
              Connect Clubs with Sponsors
            </h1>
            <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
              The easiest way to find sponsors for your club events or discover exciting sponsorship opportunities.
            </p>
            <div className="space-x-4">
              <Link href="/signup/club">
                <Button size="lg">Register Your Club</Button>
              </Link>
              <Link href="/signup/company">
                <Button size="lg" variant="outline">Become a Sponsor</Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="w-full py-12 md:py-24 lg:py-32 bg-muted">
        <div className="container px-4 md:px-6">
          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="p-4 bg-background rounded-full">
                <CalendarIcon className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold">Event Management</h3>
              <p className="text-muted-foreground">
                Easily post and manage your club events and sponsorship requirements.
              </p>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="p-4 bg-background rounded-full">
                <HandshakeIcon className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold">Direct Connections</h3>
              <p className="text-muted-foreground">
                Connect directly with potential sponsors interested in your events.
              </p>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="p-4 bg-background rounded-full">
                <UsersIcon className="h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold">Community Building</h3>
              <p className="text-muted-foreground">
                Build lasting relationships between clubs and companies.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}