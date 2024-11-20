"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { Users } from "lucide-react";

export default function ClubAuth() {
  const router = useRouter();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [confirmationCode, setConfirmationCode] = useState("");
  const [email, setEmail] = useState("");
  const [isVerifying, setIsVerifying] = useState(false);

  // Check if the user is already logged in when the component is loaded
  useEffect(() => {
    const isLoggedIn = sessionStorage.getItem("isLoggedIn");

    if (isLoggedIn) {
      router.push("/dashboard");
    }
  }, [router]);

  // Function to handle signup
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    const clubName = (document.getElementById("clubName") as HTMLInputElement).value;
    const college = (document.getElementById("college") as HTMLInputElement).value;
    const signupEmail = (document.getElementById("signupEmail") as HTMLInputElement).value;
    const signupPassword = (document.getElementById("signupPassword") as HTMLInputElement).value;

    try {
      const response = await fetch("http://13.203.61.213:5000/club/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          club_name: clubName,
          email: signupEmail,
          password: signupPassword,
          college: college,
        }),
      });

      if (!response.ok) throw new Error("Signup failed");

      setEmail(signupEmail);
      toast({
        title: "Success!",
        description: "Please check your email for the verification code.",
      });

      setIsVerifying(true);
    } catch (error) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle login
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    const loginEmail = (document.getElementById("email") as HTMLInputElement).value;
    const loginPassword = (document.getElementById("password") as HTMLInputElement).value;

    try {
      const response = await fetch("http://13.203.61.213:5000/club/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: loginEmail, password: loginPassword }),
      });

      if (!response.ok) throw new Error("Invalid credentials");

      // Store user data in sessionStorage
      sessionStorage.setItem("user", JSON.stringify({ email: loginEmail, type: "club", name: "Club Name" }));
      sessionStorage.setItem("isLoggedIn", "true");

      // Redirect to the dashboard
      router.push("/dashboard");
    } catch (error) {
      toast({
        title: "Error",
        description: "Invalid credentials.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle email verification
  const handleVerifyEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch("http://13.203.61.213:5000/club/verify_email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          code: confirmationCode,
        }),
      });

      if (!response.ok) throw new Error("Invalid confirmation code");

      toast({
        title: "Account Verified!",
        description: "Your club account has been successfully activated.",
      });

      // Store verification state in sessionStorage
      sessionStorage.setItem("isVerified", "true");

      // Redirect to the dashboard after verification
      router.push("/dashboard");
    } catch (error) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
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

        {isVerifying && (
          <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50">
            <div className="bg-white p-6 rounded-md w-80">
              <h3 className="text-lg font-bold">Verify Email</h3>
              <form onSubmit={handleVerifyEmail} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="confirmationCode">Confirmation Code</Label>
                  <Input
                    id="confirmationCode"
                    type="text"
                    required
                    value={confirmationCode}
                    onChange={(e) => setConfirmationCode(e.target.value)}
                  />
                </div>
                <Button type="submit" className="w-full" disabled={isLoading}>
                  Verify
                </Button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
