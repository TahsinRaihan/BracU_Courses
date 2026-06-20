import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
	// Check if user is authenticated
	const {
		data: { user },
		error: authError
	} = await locals.supabase.auth.getUser();

	// Require authentication
	if (authError || !user) {
		throw redirect(303, '/auth/login');
	}

	// Return user data for the layout
	return {
		user: {
			id: user.id,
			email: user.email
		}
	};
};
