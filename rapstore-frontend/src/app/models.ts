export class ApplicationInstance {
  id: number;
  version_code: number;
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
  source: string;
}

export class Board {
  id: number;
  display_name: string;
  internal_name: string;
  flash_program: string;
  storage_flash_support: boolean;
  transaction: number;
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

export class FormElementBase<T> {
  value: T;
  key: string;
  label: string;
  required: boolean;
  order: number;
  controlType: string;
 
  constructor(options: {
      value?: T,
      key?: string,
      label?: string,
      required?: boolean,
      order?: number,
      controlType?: string
    } = {}) {
    this.value = options.value;
    this.key = options.key || '';
    this.label = options.label || '';
    this.required = !!options.required;
    this.order = options.order === undefined ? 1 : options.order;
    this.controlType = options.controlType || '';
  }
}

export class TextboxElement extends FormElementBase<string> {
  controlType = 'textbox';
  type: string;

  constructor(options: {} = {}) {
    super(options);
    this.type = options['type'] || '';
  }
}

export class TextareaElement extends FormElementBase<string> {
  controlType = 'textarea';
  type: string;
}
