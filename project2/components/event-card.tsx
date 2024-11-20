"use client";

import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar, MapPin, DollarSign } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import Image from "next/image";
import { Event } from "@/lib/types";
import { useToast } from "@/hooks/use-toast";

interface EventCardProps {
  event: Event;
  isCompany: boolean;
  onSponsor: (eventId: number, amount: number) => void;
}

export function EventCard({ event, isCompany, onSponsor }: EventCardProps) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSponsorSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData(e.currentTarget);
    const amount = Number(formData.get("amount"));

    try {
      await onSponsor(event.id, amount);
      setIsDialogOpen(false);
      toast({
        title: "Success!",
        description: "Your sponsorship request has been sent.",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to submit sponsorship request.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Card className="overflow-hidden">
        <div className="relative h-48">
          <Image
            src={event.image}
            alt={event.title}
            fill
            className="object-cover"
          />
        </div>
        <CardHeader>
          <div className="space-y-1">
            <h3 className="text-xl font-semibold">{event.title}</h3>
            <p className="text-sm text-muted-foreground">{event.clubName}</p>
          </div>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <Calendar className="w-4 h-4" />
            <span>{new Date(event.date).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <MapPin className="w-4 h-4" />
            <span>{event.location}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <DollarSign className="w-4 h-4" />
            <span>Sponsorship needed: ${event.sponsorshipNeeded}</span>
          </div>
          <p className="mt-2 text-sm">{event.description}</p>
        </CardContent>
        <CardFooter>
          {isCompany && (
            <Button 
              onClick={() => setIsDialogOpen(true)} 
              className="w-full gap-2"
            >
              <DollarSign className="w-4 h-4" />
              Sponsor Event
            </Button>
          )}
        </CardFooter>
      </Card>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Sponsor {event.title}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSponsorSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="amount">Sponsorship Amount ($)</Label>
              <Input
                id="amount"
                name="amount"
                type="number"
                min="1"
                max={event.sponsorshipNeeded}
                required
              />
              <p className="text-sm text-muted-foreground">
                Maximum amount: ${event.sponsorshipNeeded}
              </p>
            </div>
            {/* <div className="space-y-2">
              <Label htmlFor="message">Message to Club (Optional)</Label>
              <Textarea
                id="message"
                name="message"
                placeholder="Include any specific requirements or questions..."
              />
            </div> */}
            <Button type="submit" className="w-full" disabled={isLoading}>
              Submit Sponsorship
            </Button>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}