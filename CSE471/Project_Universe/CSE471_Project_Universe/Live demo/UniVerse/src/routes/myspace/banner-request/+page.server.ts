import { supabase } from '$lib/supabase';
import { BannerController } from '$lib/controllers/banner.controller';
import type { PageServerLoad, Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals }) => {
  // Get session data
  const { data: { session } } = await locals.supabase.auth.getSession();
  
  if (!session?.user) {
    return {
      success: false,
      error: 'You must be logged in to request advertisements'
    };
  }

  return {
    success: null,
    error: null
  };
};

export const actions: Actions = {
  createBannerRequest: async ({ request, locals }) => {
    console.log('=== Banner Request Action Started ===');
    try {
      const formData = await request.formData();
      console.log('Form data received:', Object.fromEntries(formData.entries()));
      
      const title = formData.get('title') as string;
      const description = formData.get('description') as string;
      const duration_type = formData.get('duration_type') as 'minutes' | 'hours' | 'days';
      const duration_value = parseInt(formData.get('duration_value') as string);
      const schedule_type = formData.get('schedule_type') as 'immediate' | 'scheduled';
      const scheduled_date = formData.get('scheduled_date') as string;
      const scheduled_time = formData.get('scheduled_time') as string;

      console.log('Parsed form data:', {
        title,
        description,
        duration_type,
        duration_value,
        schedule_type,
        scheduled_date,
        scheduled_time
      });

      // Get current user from session
      const { data: { session } } = await locals.supabase.auth.getSession();
      console.log('Session check:', { hasSession: !!session, userId: session?.user?.id });
      
      if (!session?.user) {
        console.log('No session found - returning 401');
        return fail(401, { error: 'You must be logged in to request advertisements' });
      }

      // Validate input
      if (!title || title.trim().length === 0) {
        console.log('Title validation failed');
        return fail(400, { error: 'Advertisement text is required' });
      }

      if (title.length > 100) {
        console.log('Title length validation failed');
        return fail(400, { error: 'Advertisement text must be 100 characters or less' });
      }

      if (description && description.length > 500) {
        console.log('Description length validation failed');
        return fail(400, { error: 'Description must be 500 characters or less' });
      }

      if (!['minutes', 'hours', 'days'].includes(duration_type)) {
        console.log('Duration type validation failed');
        return fail(400, { error: 'Invalid duration type' });
      }

      if (duration_type === 'minutes') {
        if (duration_value < 1 || duration_value > 1440) {
          console.log('Minutes validation failed');
          return fail(400, { error: 'Duration must be between 1 and 1440 minutes' });
        }
      } else if (duration_type === 'hours') {
        if (duration_value < 1 || duration_value > 720) {
          console.log('Hours validation failed');
          return fail(400, { error: 'Duration must be between 1 and 720 hours' });
        }
      } else {
        if (duration_value < 1 || duration_value > 365) {
          console.log('Days validation failed');
          return fail(400, { error: 'Duration must be between 1 and 365 days' });
        }
      }

      if (!['immediate', 'scheduled'].includes(schedule_type)) {
        console.log('Schedule type validation failed');
        return fail(400, { error: 'Invalid schedule type' });
      }

      if (schedule_type === 'scheduled') {
        if (!scheduled_date || !scheduled_time) {
          console.log('Scheduled date/time validation failed');
          return fail(400, { error: 'Scheduled date and time are required for scheduled requests' });
        }

        // Validate that scheduled date is in the future
        // Convert local Bangladesh time to UTC for proper comparison
        // Create date in Bangladesh timezone (UTC+6)
        const localDateTime = new Date(`${scheduled_date}T${scheduled_time}:00+06:00`);
        const utcDateTime = new Date(localDateTime.toISOString());
        const now = new Date();
        
        console.log('Scheduled time conversion:', {
          localDateTime: localDateTime.toISOString(),
          utcDateTime: utcDateTime.toISOString(),
          now: now.toISOString(),
          isInPast: utcDateTime <= now
        });
        
        if (utcDateTime <= now) {
          console.log('Scheduled date in past validation failed');
          return fail(400, { 
            error: `Scheduled date and time must be in the future. You selected ${scheduled_date} ${scheduled_time} (Bangladesh time), which is ${utcDateTime.toISOString()} UTC, but current time is ${now.toISOString()} UTC.` 
          });
        }
      }

      console.log('All validations passed, calling BannerController');
      const bannerController = new BannerController(locals.supabase);
      const result = await bannerController.createBannerRequest(session.user.id, {
        title: title.trim(),
        description: description?.trim() || undefined,
        duration_type,
        duration_value,
        schedule_type,
        scheduled_date: schedule_type === 'scheduled' ? scheduled_date : undefined,
        scheduled_time: schedule_type === 'scheduled' ? scheduled_time : undefined
      });

      console.log('BannerController result:', result);

      if (result.success) {
        console.log('Success - returning success response');
        return { 
          success: true,
          message: 'Your advertisement request has been submitted successfully! An admin will review it soon.'
        };
      } else {
        console.log('BannerController failed:', result.error);
        return fail(500, { 
          error: result.error || 'Failed to create banner request',
          message: result.error || 'Failed to create banner request'
        });
      }
    } catch (error) {
      console.error('Unexpected error in createBannerRequest:', error);
      return fail(500, { 
        error: 'An unexpected error occurred',
        message: 'An unexpected error occurred'
      });
    }
  }
};
