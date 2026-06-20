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
      error: 'You must be logged in to access this page'
    };
  }

  // Check if user is admin
  const { data: userRole, error: roleError } = await locals.supabase.rpc('get_user_role', {
    user_id: session.user.id
  });

  if (roleError || userRole !== 'admin') {
    return {
      success: false,
      error: 'Admin access required'
    };
  }

  // Load banner requests
  const bannerController = new BannerController(locals.supabase);
  
  try {
    const [pendingResult, allResult] = await Promise.all([
      bannerController.getPendingBannerRequests(),
      bannerController.getAllBannerRequests()
    ]);

    return {
      pendingRequests: pendingResult.success ? pendingResult.data : [],
      allRequests: allResult.success ? allResult.data : [],
      error: null
    };
  } catch (error) {
    return {
      pendingRequests: [],
      allRequests: [],
      error: 'Failed to load banner requests'
    };
  }
};

export const actions: Actions = {
  approveBannerRequest: async ({ request, locals }) => {
    try {
      const formData = await request.formData();
      const requestId = formData.get('requestId') as string;

      // Get current user from session
      const { data: { session } } = await locals.supabase.auth.getSession();
      if (!session?.user) {
        return fail(401, { error: 'You must be logged in to approve requests' });
      }

      // Check if user is admin
      const { data: userRole, error: roleError } = await locals.supabase.rpc('get_user_role', {
        user_id: session.user.id
      });

      if (roleError || userRole !== 'admin') {
        return fail(403, { error: 'Admin access required' });
      }

      const bannerController = new BannerController(locals.supabase);
      const result = await bannerController.approveBannerRequest(requestId, session.user.id);

      if (result.success) {
        return { success: 'Banner request approved successfully' };
      } else {
        return fail(500, { error: result.error || 'Failed to approve banner request' });
      }
    } catch (error) {
      console.error('Error approving banner request:', error);
      return fail(500, { error: 'An unexpected error occurred' });
    }
  },

  rejectBannerRequest: async ({ request, locals }) => {
    try {
      const formData = await request.formData();
      const requestId = formData.get('requestId') as string;
      const adminNotes = formData.get('adminNotes') as string;

      // Get current user from session
      const { data: { session } } = await locals.supabase.auth.getSession();
      if (!session?.user) {
        return fail(401, { error: 'You must be logged in to reject requests' });
      }

      // Check if user is admin
      const { data: userRole, error: roleError } = await locals.supabase.rpc('get_user_role', {
        user_id: session.user.id
      });

      if (roleError || userRole !== 'admin') {
        return fail(403, { error: 'Admin access required' });
      }

      if (!adminNotes || adminNotes.trim().length === 0) {
        return fail(400, { error: 'Admin notes are required for rejection' });
      }

      const bannerController = new BannerController(locals.supabase);
      const result = await bannerController.rejectBannerRequest(requestId, session.user.id, adminNotes.trim());

      if (result.success) {
        return { success: 'Banner request rejected successfully' };
      } else {
        return fail(500, { error: result.error || 'Failed to reject banner request' });
      }
    } catch (error) {
      console.error('Error rejecting banner request:', error);
      return fail(500, { error: 'An unexpected error occurred' });
    }
  },

  deleteBannerRequest: async ({ request, locals }) => {
    try {
      const formData = await request.formData();
      const requestId = formData.get('requestId') as string;

      // Get current user from session
      const { data: { session } } = await locals.supabase.auth.getSession();
      if (!session?.user) {
        return fail(401, { error: 'You must be logged in to delete requests' });
      }

      // Check if user is admin
      const { data: userRole, error: roleError } = await locals.supabase.rpc('get_user_role', {
        user_id: session.user.id
      });

      if (roleError || userRole !== 'admin') {
        return fail(403, { error: 'Admin access required' });
      }

      const bannerController = new BannerController(locals.supabase);
      const result = await bannerController.deleteBannerRequest(requestId);

      if (result.success) {
        return { success: 'Banner request deleted successfully' };
      } else {
        return fail(500, { error: result.error || 'Failed to delete banner request' });
      }
    } catch (error) {
      console.error('Error deleting banner request:', error);
      return fail(500, { error: 'An unexpected error occurred' });
    }
  }
};
