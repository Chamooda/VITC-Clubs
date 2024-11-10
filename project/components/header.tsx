'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { MoonIcon, SunIcon } from 'lucide-react';
import { useTheme } from 'next-themes';

export default function Header() {
  const { theme, setTheme } = useTheme();

  return (
    <header className="w-full border-b">
      <div className="container flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2">
          <span className="text-2xl font-bold">SponsorConnect</span>
        </Link>
        
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            <SunIcon className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <MoonIcon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          </Button>
          <div className="flex gap-2">
            <Link href="/login/club">
              <Button variant="outline">Club Login</Button>
            </Link>
            <Link href="/login/company">
              <Button>Company Login</Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}