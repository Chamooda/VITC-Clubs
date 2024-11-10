"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Users } from "lucide-react";
import Link from "next/link";

export default function ClubSignup() {
  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Add signup logic here
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <div className="container flex h-screen w-screen flex-col items-center justify-center">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
        <div className="flex flex-col space-y-2 text-center">
          <Users className="mx-auto h-6 w-6" />
          <h1 className="text-2xl font-semibold tracking-tight">Create a club account</h1>
          <p className="text-sm text-muted-foreground">
            Enter your details below to create your club account
          </p>
        </div>
        <form onSubmit={onSubmit}>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="clubName">Club name</Label>
              <Input id="clubName" placeholder="University Chess Club" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="m@example.com" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" required />
            </div>
            <Button className="w-full" type="submit" disabled={isLoading}>
              {isLoading ? "Creating account..." : "Create account"}
            </Button>
          </div>
        </form>
        <div className="px-8 text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/club/login" className="underline underline-offset-4 hover:text-primary">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  );
}