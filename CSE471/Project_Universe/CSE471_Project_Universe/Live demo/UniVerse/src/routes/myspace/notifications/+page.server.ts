import { supabase } from '$lib/supabase';
import { NotificationController } from '$lib/controllers/notification.controller';
import type { PageServerLoad } from './$types';
import type { RequestEvent } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, parent }) => {
  // Get session data from parent layout
  const { session } = await parent();
  
  if (!session?.user) {
    return {
      notifications: [],
      error: 'You must be logged in to view notifications'
    };
  }

  const notificationController = new NotificationController(locals.supabase);
  
  // Process overdue event reminders first
  console.log('Processing overdue reminders for user:', session.user.id);
  const reminderResult = await notificationController.processOverdueEventReminders();
  console.log('Reminder processing result:', reminderResult);
  
  // Then get user notifications
  const result = await notificationController.getUserNotifications(session.user.id);
  console.log('Notifications result:', result);
  
  return {
    notifications: result.success && result.data ? result.data : [],
    session,
    error: result.success ? null : result.error
  };
};

export const actions = {
  processOverdue: async ({ locals }: RequestEvent) => {
    const notificationController = new NotificationController(locals.supabase);
    const result = await notificationController.processOverdueEventReminders();
    return result;
  },
  markAsRead: async ({ request, locals }: RequestEvent) => {
    const formData = await request.formData();
    const notificationId = formData.get('notificationId') as string;

    console.log('Mark as read - notificationId:', notificationId);

    const session = await locals.getSession();
    if (!session?.user) {
      console.log('Mark as read - user not authenticated');
      return { success: false, error: 'User not authenticated' };
    }

    console.log('Mark as read - user:', session.user.id);

    try {
      const notificationController = new NotificationController(locals.supabase);
      const result = await notificationController.markNotificationAsRead(notificationId);
      console.log('Mark as read - result:', result);
      return result;
    } catch (error) {
      console.error('Mark as read - error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'An error occurred'
      };
    }
  },

  markAllAsRead: async ({ request, locals }: RequestEvent) => {
    const session = await locals.getSession();
    if (!session?.user) {
      return { success: false, error: 'User not authenticated' };
    }

    try {
      const notificationController = new NotificationController(locals.supabase);
      const result = await notificationController.markAllNotificationsAsRead(session.user.id);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'An error occurred'
      };
    }
  },

  deleteNotification: async ({ request, locals }: RequestEvent) => {
    const formData = await request.formData();
    const notificationId = formData.get('notificationId') as string;

    console.log('Delete notification - notificationId:', notificationId);

    const session = await locals.getSession();
    if (!session?.user) {
      console.log('Delete notification - user not authenticated');
      return { success: false, error: 'User not authenticated' };
    }

    console.log('Delete notification - user:', session.user.id);

    try {
      const notificationController = new NotificationController(locals.supabase);
      const result = await notificationController.deleteNotification(notificationId);
      console.log('Delete notification - result:', result);
      return result;
    } catch (error) {
      console.error('Delete notification - error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'An error occurred'
      };
    }
  }
};
