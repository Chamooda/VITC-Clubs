"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { Building2 } from "lucide-react";

export default function CompanyAuth() {
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
    const companyName = (document.getElementById("companyName") as HTMLInputElement).value;
    const industry = (document.getElementById("industry") as HTMLInputElement).value;
    const signupEmail = (document.getElementById("signupEmail") as HTMLInputElement).value;
    const signupPassword = (document.getElementById("signupPassword") as HTMLInputElement).value;

    try {
      // Call the API to sign up
      const response = await fetch("http://13.203.61.213:5000/company/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company_name: companyName,
          email: signupEmail,
          password: signupPassword,
          industry: industry,
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
        description: String(error) || "An unexpected error occurred.",        variant: "destructive",
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
      const response = await fetch("http://13.203.61.213:5000/company/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: loginEmail, password: loginPassword }),
      });

      if (!response.ok) throw new Error("Invalid credentials");

      // Store user data in sessionStorage
      sessionStorage.setItem("user", JSON.stringify({ email: loginEmail, type: "company", name: "Company Name" }));
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
      const response = await fetch("http://13.203.61.213:5000/company/verify_email", {
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
        description: "Your company account has been successfully activated.",
      });

      // Store verification state in sessionStorage
      sessionStorage.setItem("isVerified", "true");

      // Redirect to the dashboard after verification
      router.push("/dashboard");
    } catch (error) {
      toast({
        title: "Error",
        description: String(error) || "An unexpected error occurred.",        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <Building2 className="mx-auto h-12 w-12 text-primary" />
          <h2 className="mt-6 text-3xl font-bold">Company Portal</h2>
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
                <Label htmlFor="companyName">Company Name</Label>
                <Input id="companyName" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <Input id="industry" required />
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

        {/* Confirmation Popup */}
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
