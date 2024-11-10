export default function Footer() {
  return (
    <footer className="w-full border-t">
      <div className="container flex h-16 items-center justify-between px-4">
        <p className="text-sm text-muted-foreground">
          © {new Date().getFullYear()} SponsorConnect. All rights reserved.
        </p>
      </div>
    </footer>
  );
}