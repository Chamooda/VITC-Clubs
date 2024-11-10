import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, Users, Building2, Calendar } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-600">
            Connect College Clubs with Sponsors
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            The ultimate platform for college clubs to showcase events and connect with potential sponsors
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/club">
              <Button size="lg" className="gap-2">
                <Users className="w-5 h-5" />
                Join as Club
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
            <Link href="/auth/company">
              <Button size="lg" variant="outline" className="gap-2">
                <Building2 className="w-5 h-5" />
                Join as Company
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-card p-6 rounded-lg shadow-lg">
            <Users className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">For Clubs</h3>
            <p className="text-muted-foreground">
              Showcase your events and connect with potential sponsors to make your events bigger and better.
            </p>
          </div>
          <div className="bg-card p-6 rounded-lg shadow-lg">
            <Building2 className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">For Companies</h3>
            <p className="text-muted-foreground">
              Discover and sponsor college events to increase your brand visibility among students.
            </p>
          </div>
          <div className="bg-card p-6 rounded-lg shadow-lg">
            <Calendar className="w-12 h-12 text-primary mb-4" />
            <h3 className="text-xl font-semibold mb-2">Events</h3>
            <p className="text-muted-foreground">
              Browse through upcoming events and find opportunities for collaboration.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}