import * as authService from '../services/authService';

export async function loginUser(email: string, password: string) {
  const error = await authService.signInWithPassword(email, password);
  return { error };
}

export async function signupUser(email: string, password: string, nickname: string) {
  const error = await authService.signUpUser(email, password, nickname);
  return { error };
}