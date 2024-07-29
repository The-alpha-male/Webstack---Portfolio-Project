import { validate } from './login.vue';

describe('validate', () => {
  it('should return an error if email is missing', () => {
    const state = { email: '', password: 'password123' };
    const errors = validate(state);
    expect(errors).toEqual([{ path: 'email', message: 'Email is required' }]);
  });

  it('should return an error if password is missing', () => {
    const state = { email: 'test@example.com', password: '' };
    const errors = validate(state);
    expect(errors).toEqual([{ path: 'password', message: 'Password is required' }]);
  });

  it('should return errors if both email and password are missing', () => {
    const state = { email: '', password: '' };
    const errors = validate(state);
    expect(errors).toEqual([
      { path: 'email', message: 'Email is required' },
      { path: 'password', message: 'Password is required' }
    ]);
  });

  it('should return no errors if both email and password are provided', () => {
    const state = { email: 'test@example.com', password: 'password123' };
    const errors = validate(state);
    expect(errors).toEqual([]);
  });
});

