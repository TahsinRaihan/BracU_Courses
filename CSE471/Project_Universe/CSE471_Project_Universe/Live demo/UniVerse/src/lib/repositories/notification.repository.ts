import type { SupabaseClient } from '@supabase/supabase-js';
import type { Notification, CreateNotificationInput } from '$lib/types/event';

export async function getUserNotifications(supabase: SupabaseClient, userId: string): Promise<Notification[]> {
  const { data, error } = await supabase
    .from('notifications')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) {
    throw new Error(`Failed to fetch user notifications: ${error.message}`);
  }

  return data || [];
}

export async function getUnreadNotifications(supabase: SupabaseClient, userId: string): Promise<Notification[]> {
  const { data, error } = await supabase
    .from('notifications')
    .select('*')
    .eq('user_id', userId)
    .eq('is_read', false)
    .order('created_at', { ascending: false });

  if (error) {
    throw new Error(`Failed to fetch unread notifications: ${error.message}`);
  }

  return data || [];
}

export async function createNotification(supabase: SupabaseClient, userId: string, notificationData: CreateNotificationInput): Promise<Notification> {
  const { data, error } = await supabase
    .from('notifications')
    .insert({
      ...notificationData,
      user_id: userId
    })
    .select()
    .single();

  if (error) {
    throw new Error(`Failed to create notification: ${error.message}`);
  }

  return data;
}

export async function markNotificationAsRead(supabase: SupabaseClient, notificationId: string): Promise<Notification> {
  console.log('Repository - markNotificationAsRead - notificationId:', notificationId);
  
  const { data, error } = await supabase
    .from('notifications')
    .update({ is_read: true })
    .eq('id', notificationId)
    .select()
    .single();

  if (error) {
    console.error('Repository - markNotificationAsRead - error:', error);
    throw new Error(`Failed to mark notification as read: ${error.message}`);
  }

  console.log('Repository - markNotificationAsRead - success:', data);
  return data;
}

export async function markAllNotificationsAsRead(supabase: SupabaseClient, userId: string): Promise<void> {
  const { error } = await supabase
    .from('notifications')
    .update({ is_read: true })
    .eq('user_id', userId)
    .eq('is_read', false);

  if (error) {
    throw new Error(`Failed to mark all notifications as read: ${error.message}`);
  }
}

export async function deleteNotification(supabase: SupabaseClient, notificationId: string): Promise<void> {
  console.log('Repository - deleteNotification - notificationId:', notificationId);
  
  const { error } = await supabase
    .from('notifications')
    .delete()
    .eq('id', notificationId);

  if (error) {
    console.error('Repository - deleteNotification - error:', error);
    throw new Error(`Failed to delete notification: ${error.message}`);
  }

  console.log('Repository - deleteNotification - success');
}

export async function getNotificationCount(supabase: SupabaseClient, userId: string): Promise<number> {
  const { count, error } = await supabase
    .from('notifications')
    .select('*', { count: 'exact', head: true })
    .eq('user_id', userId)
    .eq('is_read', false);

  if (error) {
    throw new Error(`Failed to get notification count: ${error.message}`);
  }

  return count || 0;
}
