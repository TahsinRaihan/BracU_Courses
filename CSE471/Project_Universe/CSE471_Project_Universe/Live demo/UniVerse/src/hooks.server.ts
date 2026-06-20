import { createServerClient } from '@supabase/ssr'
import { type Handle } from '@sveltejs/kit'
import { sequence } from '@sveltejs/kit/hooks'
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public'

const supabase: Handle = async ({ event, resolve }) => {
  event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
    cookies: {
      getAll: () => event.cookies.getAll(),
      setAll: (cookiesToSet) => {
        try {
          cookiesToSet.forEach(({ name, value, options }) => {
            event.cookies.set(name, value, { path: '/', ...options })
          })
        } catch (error) {
          // Silently handle cookie setting errors
          console.warn('Failed to set cookies:', error)
        }
      },
    },
  })

  // Add getSession method to localsi
  event.locals.getSession = async () => {
    const { data: { session } } = await event.locals.supabase.auth.getSession()
    return session
  }
//cafeteria item/[id]/+page.svelte auth issue
  // Get the user from Supabase Auth server for authentication
  const { data: { user } } = await event.locals.supabase.auth.getUser();
  console.log('[HOOKS] User from getUser():', user); // Debug log
  event.locals.user = user;

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      return name === 'content-range'
    },
  })
}

export const handle = sequence(supabase)