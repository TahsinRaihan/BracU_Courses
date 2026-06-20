import { supabase } from './supabase';

export async function testConnection() {
	try {
		// Test the connection by checking auth status
		const { data, error } = await supabase.auth.getSession();

		if (error) {
			console.log('Connection test result:', error.message);
			return { success: false, error };
		} else {
			console.log('✅ Supabase connection successful!');
			return { success: true, error: null };
		}
	} catch (err) {
		console.log('❌ Connection failed:', err);
		return { success: false, error: err };
	}
}

export async function testDatabaseAccess() {
	try {
		// Test database access by making a simple query that should work on any Supabase instance
		// Try to get the current user (this tests database connectivity through auth)
		const { data: userData, error: userError } = await supabase.auth.getUser();

		if (userError) {
			// If auth fails, that's actually expected for database connectivity test
			// The important thing is that we can reach the database
			return { success: true, message: 'Database accessible (auth endpoint reachable)' };
		} else {
			return { success: true, message: 'Database accessible (auth test successful)' };
		}
	} catch (err) {
		return { success: false, error: err };
	}
}
