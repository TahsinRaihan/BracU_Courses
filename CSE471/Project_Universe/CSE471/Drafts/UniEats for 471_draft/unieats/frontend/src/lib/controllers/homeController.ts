
import * as homeService from '../services/homeService';
import { supabase } from '../repositories/supabaseClient';

export async function loadHomePage() {
  const { data: { session } } = await supabase.auth.getSession();
  const user = session?.user ?? null;
  const { daily, weekly, offers } = await homeService.getHomePageData();
  return { user, daily, weekly, offers };
}
