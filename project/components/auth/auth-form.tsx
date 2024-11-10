'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from '@/components/ui/use-toast';

interface AuthFormProps {
  type: 'login' | 'signup';
  userType: 'club' | 'company';
}

export default function AuthForm({ type, userType }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement actual authentication
    toast({
      title: 'Success!',
      description: `${type === 'login' ? 'Logged in' : 'Signed up'} successfully as ${userType}`,
    });
    router.push(`/dashboard/${userType}`);
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>{type === 'login' ? 'Welcome back!' : 'Create your account'}</CardTitle>
        <CardDescription>
          {type === 'login' 
            ? `Sign in to your ${userType} account` 
            : `Register your ${userType} to get started`}
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {type === 'signup' && (
            <div className="space-y-2">
              <Label htmlFor="name">{userType === 'club' ? 'Club Name' : 'Company Name'}</Label>
              <Input
                id="name"
                type="text"
                placeholder={userType === 'club' ? 'Enter club name' : 'Enter company name'}
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full">
            {type === 'login' ? 'Sign In' : 'Sign Up'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}