export type UserType = 'club' | 'company';

export interface User {
  id: string;
  type: UserType;
  name: string;
  email: string;
}

export interface Event {
  id: number;
  title: string;
  clubName: string;
  date: string;
  location: string;
  description: string;
  sponsorshipNeeded: number;
  image: string;
}