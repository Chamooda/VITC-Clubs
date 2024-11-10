"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { PlusCircle, LogOut } from "lucide-react";
import { EventCard } from "@/components/event-card";
import { useUser } from "@/contexts/user-context";
import { useRouter } from "next/navigation";
import { Event } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";

// Mock data for demonstration
const mockEvents: Event[] = [
  {
    id: 1,
    title: "Tech Hackathon 2024",
    clubName: "Tech Club",
    date: "2024-04-15",
    location: "Main Campus Hall",
    description: "Join us for a 24-hour coding challenge!",
    sponsorshipNeeded: 5000,
    image: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&q=80&w=1000",
  },
  {
    id: 2,
    title: "Business Summit 2024",
    clubName: "Business Club",
    date: "2024-05-20",
    location: "Business School Auditorium",
    description: "Annual business leadership summit with industry experts",
    sponsorshipNeeded: 3000,
    image: "https://images.unsplash.com/photo-1515187029135-18ee286d815b?auto=format&fit=crop&q=80&w=1000",
  },
];

export default function Dashboard() {
  const { user, logout } = useUser();
  const router = useRouter();
  const [events] = useState(mockEvents);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    if (!user) {
      router.push('/');
    }
  }, [user, router]);

  const handleCreateEvent = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      // TODO: Implement event creation API call
      toast({
        title: "Success!",
        description: "Event created successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to create event.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSponsorEvent = async (eventId: number, amount: number) => {
    setIsLoading(true);
    try {
      // TODO: Implement sponsorship API call
      console.log(`Sponsoring event ${eventId} with amount ${amount}`);
    } catch (error) {
      throw new Error('Failed to sponsor event');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  // Show loading state or return null while checking authentication
  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Campus Events</h1>
          <div className="flex items-center gap-4">
            <span className="text-muted-foreground">
              {user.name} ({user.type})
            </span>
            {user.type === 'club' && (
              <Dialog>
                <DialogTrigger asChild>
                  <Button className="gap-2" disabled={isLoading}>
                    <PlusCircle className="w-4 h-4" />
                    Create Event
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Create New Event</DialogTitle>
                  </DialogHeader>
                  <form onSubmit={handleCreateEvent} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="title">Event Title</Label>
                      <Input id="title" name="title" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="date">Date</Label>
                      <Input id="date" name="date" type="date" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location">Location</Label>
                      <Input id="location" name="location" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="sponsorshipNeeded">Sponsorship Amount Needed ($)</Label>
                      <Input id="sponsorshipNeeded" name="sponsorshipNeeded" type="number" min="1" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea id="description" name="description" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="image">Image URL</Label>
                      <Input id="image" name="image" type="url" required />
                    </div>
                    <Button type="submit" className="w-full" disabled={isLoading}>
                      Create Event
                    </Button>
                  </form>
                </DialogContent>
              </Dialog>
            )}
            <Button 
              variant="outline" 
              onClick={handleLogout} 
              className="gap-2"
              disabled={isLoading}
            >
              <LogOut className="w-4 h-4" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              isCompany={user.type === 'company'}
              onSponsor={handleSponsorEvent}
            />
          ))}
        </div>
      </main>
    </div>
  );
}