"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { PlusCircle, LogOut } from "lucide-react";
import { EventCard } from "@/components/event-card";
import { useRouter } from "next/navigation";
import { Event } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";

export default function Dashboard() {
  const router = useRouter();
  const { toast } = useToast();
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState<any>(null);

  // Fetch user data from sessionStorage on component mount
  useEffect(() => {
    const loggedInUser = sessionStorage.getItem("user");
    if (!loggedInUser) {
      router.push("/");
      return;
    }

    const userData = JSON.parse(loggedInUser);
    setUser(userData);

    // Fetch events from the API
    const fetchEvents = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("http://13.203.61.213:5000/get_events", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) throw new Error("Failed to fetch events.");

        const data = await response.json();
        // Transform API response data to match the Event type structure
        const formattedEvents = data.data.map((event: any) => ({
          id: event.id,
          title: event.title,
          clubName: event.clubName,
          date: new Date(event.date).toISOString().split("T")[0], // Format as YYYY-MM-DD
          location: event.location,
          description: event.description,
          sponsorshipNeeded: parseFloat(event.sponsorshipNeeded),
          image: event.image,
        }));

        setEvents(formattedEvents);
      } catch (error) {
        toast({
          title: "Error",
          description: error instanceof Error ? error.message : "Failed to fetch events.",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchEvents();
  }, [router, toast]);

  const handleCreateEvent = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const formData = new FormData(e.currentTarget);
      const newEvent = {
        title: formData.get("title"),
        date: formData.get("date"),
        location: formData.get("location"),
        sponsorshipNeeded: formData.get("sponsorshipNeeded"),
        description: formData.get("description"),
        image: formData.get("image"),
        clubEmail: user.email, // Add the club email here
      };

      const response = await fetch("http://13.203.61.213:5000/add_event", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newEvent),
      });

      if (!response.ok) throw new Error("Failed to create event");

      const createdEvent = await response.json();
      setEvents((prevEvents) => [...prevEvents, createdEvent]);

      toast({
        title: "Success!",
        description: "Event created successfully.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to create event.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSponsorEvent = async (eventId: number, amount: number, message: string) => {
    setIsLoading(true);

    // Get the sponsor's email from sessionStorage
    const sponsorEmail = user.email;
    
    // Check if the email exists
    if (!sponsorEmail) {
      toast({
        title: "Error",
        description: "Sponsor email not found. Please log in again.",
        variant: "destructive",
      });
      setIsLoading(false);
      return;
    }
    console.log(message)
    try {
      const response = await fetch("http://13.203.61.213:5000/confirm_sponsorship", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          eventId,
          amount,
          email: sponsorEmail,
          message,
        }),
      });

      if (!response.ok) throw new Error("Failed to sponsor event");

      toast({
        title: "Thank you!",
        description: "Sponsorship successful.",
      });

    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to sponsor event.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem("user");
    sessionStorage.removeItem("isLoggedIn");
    router.push("/");
  };

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
            {user.type === "club" && (
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
                      <Label htmlFor="sponsorshipNeeded">
                        Sponsorship Amount Needed ($)
                      </Label>
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
              isCompany={user.type === "company"}
              onSponsor={handleSponsorEvent} // Pass function directly
            />
          ))}
        </div>
      </main>
    </div>
  );
}
