import AuthForm from '@/components/auth/auth-form';

export default function ClubLoginPage() {
  return (
    <div className="container flex items-center justify-center min-h-[calc(100vh-8rem)] py-8">
      <AuthForm type="login" userType="club" />
    </div>
  );
}