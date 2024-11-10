"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { Users } from "lucide-react";
import { useUser } from "@/contexts/user-context";

export default function ClubAuth() {
  const router = useRouter();
  const { toast } = useToast();
  const { login } = useUser();
  const [isLoading, setIsLoading] = useState(false);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: Implement signup API call
    login('club');
    toast({
      title: "Success!",
      description: "Your club account has been created successfully.",
    });
    router.push("/dashboard");
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: Implement login API call
    login('club');
    router.push("/dashboard");
  };

  return (
    <div className="container mx-auto flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Users className="mx-auto h-12 w-12 text-primary" />
          <h2 className="mt-6 text-3xl font-bold">Club Portal</h2>
        </div>

        <Tabs defaultValue="login" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="signup">Sign up</TabsTrigger>
          </TabsList>

          <TabsContent value="login">
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input id="password" type="password" required />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                Login
              </Button>
            </form>
          </TabsContent>

          <TabsContent value="signup">
            <form onSubmit={handleSignup} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="clubName">Club Name</Label>
                <Input id="clubName" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="college">College</Label>
                <Input id="college" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="signupEmail">Email</Label>
                <Input id="signupEmail" type="email" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="signupPassword">Password</Label>
                <Input id="signupPassword" type="password" required />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                Sign up
              </Button>
            </form>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}