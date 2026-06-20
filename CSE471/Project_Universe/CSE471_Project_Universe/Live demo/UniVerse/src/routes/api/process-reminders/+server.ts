import type { RequestHandler } from './$types'
import { serviceSupabase } from '$lib/server/supabaseService'

export const POST: RequestHandler = async () => {
  try {
    const nowIso = new Date().toISOString()

    const { data: reminders, error: rErr } = await serviceSupabase
      .from('event_reminders')
      .select('*')
      .lte('reminder_time', nowIso)
      .eq('is_sent', false)

    if (rErr) {
      return new Response(JSON.stringify({ error: rErr.message }), { status: 500 })
    }

    let processed = 0
    const errors: string[] = []

    for (const rem of reminders ?? []) {
      try {
        const { data: event, error: eErr } = await serviceSupabase
          .from('events')
          .select('title, description, event_date')
          .eq('id', rem.event_id)
          .single()
        if (eErr) throw eErr

        const eventDate = event?.event_date ? new Date(event.event_date) : new Date()
        // Add 6 hours to convert to Bangladesh time and use only the date portion
        const bangladeshDate = new Date(eventDate.getTime() + (6 * 60 * 60 * 1000));
        const dateOnly = bangladeshDate.toLocaleDateString();
        const msg = `Don't forget! ${event?.title ?? 'Event'} is happening on ${dateOnly}.`

        const { error: nErr } = await serviceSupabase
          .from('notifications')
          .insert({
            user_id: rem.user_id,
            title: `Event Reminder: ${event?.title ?? 'Event'}`,
            message: msg,
            type: 'event',
            action_url: `/myspace?eventId=${rem.event_id}`,
            expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
          })
        if (nErr) throw nErr

        const { error: uErr } = await serviceSupabase
          .from('event_reminders')
          .update({ is_sent: true })
          .eq('id', rem.id)
        if (uErr) throw uErr

        processed++
      } catch (err: any) {
        errors.push(err?.message ?? 'Unknown error')
      }
    }

    return new Response(JSON.stringify({ processed, errors }), {
      headers: { 'content-type': 'application/json' },
    })
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e?.message ?? 'Unknown server error' }), { status: 500 })
  }
}


