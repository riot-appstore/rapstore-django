export class Application {
  id: number;
  name: string;
  description: string;
}

export class Board {
  id: number;
  display_name: string;
  internal_name: string;
  flash_program: string;
  transction: number;
}

export class User {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  is_dev: boolean;
}
