import { supabase } from '../repositories/supabaseClient';

export async function signInWithPassword(email: string, password: string) {
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  return error;
}

export async function signUpUser(email: string, password: string, nickname: string) {
  const { error } = await supabase.auth.signUp({
    email,
    password,
    options: { data: { nickname } }
  });
  return error;
}