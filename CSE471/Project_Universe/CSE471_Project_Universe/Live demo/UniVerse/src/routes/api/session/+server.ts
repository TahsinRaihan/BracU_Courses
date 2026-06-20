import type { RequestHandler } from './$types'

export const GET: RequestHandler = async ({ locals }) => {
  const session = await locals.getSession()
  console.log('Session endpoint called, session:', session ? 'exists' : 'null');
  if (!session) {
    return new Response(JSON.stringify({ session: null }), { headers: { 'content-type': 'application/json' } })
  }
  // Return minimal tokens needed to authenticate the browser client
  const response = {
    session: {
      access_token: session.access_token,
      refresh_token: session.refresh_token,
      user: { id: session.user.id, email: session.user.email },
    },
  };
  console.log('Returning session data for user:', session.user.id);
  return new Response(
    JSON.stringify(response),
    { headers: { 'content-type': 'application/json' } }
  )
}


