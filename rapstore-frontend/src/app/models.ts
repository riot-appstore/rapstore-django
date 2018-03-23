export class Application {
  id: number;
  name: string;
  description: string;
}

export const APPS: Application[] = [
  { id: 1, name: 'GNRC Networking', description: "Standard network for RIOT" },
  { id: 2, name: 'My App', description: "This is my own app" },
];
