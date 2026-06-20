import * as homeService from '../services/homeService';
import { supabase } from '$lib/supabase';

export async function loadHomePage() {
	const {
		data: { user: authenticatedUser },
		error
	} = await supabase.auth.getUser();
	const user = authenticatedUser ?? null;
	if (error) {
		console.error('Error fetching authenticated user in loadHomePage:', error);
	}
	const { daily, weekly, offers } = await homeService.getHomePageData();
	return { user, daily, weekly, offers };
}
