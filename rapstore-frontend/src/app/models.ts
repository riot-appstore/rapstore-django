export class ApplicationInstance {
  id: number;
  version_code: string;
  version_name: string;
}

export class Application {
  id: number;
  name: string;
  description: string;
  download_count: number;
  author: User;
  licenses: string;
  project_page: string;
  initial_instance: ApplicationInstance;
  updated_at: Date;
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
  location: string;
  company: string;
  gender: string;
  phone_number: string;
}

export class Signup {
  username: string;
  password: string;
  email: string;
  first_name: string;
  last_name: string;
}

export class Feedback {
  description: string;
}
