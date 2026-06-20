import type { SupabaseClient } from '@supabase/supabase-js';
import type { BannerRequest, CreateBannerRequestInput, UpdateBannerRequestInput, ActiveBanner } from '$lib/types/banner';

export async function getAllBannerRequests(supabase: SupabaseClient): Promise<BannerRequest[]> {
  const { data, error } = await supabase
    .from('banner_requests')
    .select('*')
    .order('created_at', { ascending: false });

  if (error) {
    throw new Error(`Failed to fetch banner requests: ${error.message}`);
  }

  return data || [];
}

export async function getPendingBannerRequests(supabase: SupabaseClient): Promise<BannerRequest[]> {
  const { data, error } = await supabase
    .from('banner_requests')
    .select('*')
    .eq('status', 'pending')
    .order('created_at', { ascending: false });

  if (error) {
    throw new Error(`Failed to fetch pending banner requests: ${error.message}`);
  }

  return data || [];
}

export async function getActiveBanners(supabase: SupabaseClient): Promise<ActiveBanner[]> {
  const now = new Date().toISOString();
  
  const { data, error } = await supabase
    .from('banner_requests')
    .select('title, description')
    .eq('status', 'approved')
    .lte('start_date', now)  // Banner should have started
    .gt('end_date', now)     // Banner should not have ended yet
    .order('created_at', { ascending: false });

  if (error) {
    throw new Error(`Failed to fetch active banners: ${error.message}`);
  }
  
  return data || [];
}

export async function getBannerRequestById(supabase: SupabaseClient, requestId: string): Promise<BannerRequest | null> {
  const { data, error } = await supabase
    .from('banner_requests')
    .select('*')
    .eq('id', requestId)
    .single();

  if (error) {
    if (error.code === 'PGRST116') {
      return null; // No rows returned
    }
    throw new Error(`Failed to fetch banner request: ${error.message}`);
  }

  return data;
}

export async function createBannerRequest(supabase: SupabaseClient, userId: string, requestData: CreateBannerRequestInput & { duration_days?: number | null; duration_hours?: number | null; duration_minutes?: number | null; scheduled_start_date?: string | null }): Promise<BannerRequest> {
  console.log('=== BannerRepository.createBannerRequest started ===');
  console.log('UserId:', userId);
  console.log('RequestData:', requestData);
  
  const insertData = {
    title: requestData.title,
    description: requestData.description,
    duration_days: requestData.duration_days,
    duration_hours: requestData.duration_hours,
    duration_minutes: requestData.duration_minutes,
    schedule_type: requestData.schedule_type,
    scheduled_start_date: requestData.scheduled_start_date,
    user_id: userId
  };
  
  console.log('Insert data:', insertData);
  
  const { data, error } = await supabase
    .from('banner_requests')
    .insert(insertData)
    .select()
    .single();

  if (error) {
    console.error('Supabase insert error:', error);
    throw new Error(`Failed to create banner request: ${error.message}`);
  }

  console.log('Supabase insert success:', data);
  return data;
}

export async function updateBannerRequest(supabase: SupabaseClient, requestId: string, updates: UpdateBannerRequestInput): Promise<BannerRequest> {
  const { data, error } = await supabase
    .from('banner_requests')
    .update({
      ...updates,
      updated_at: new Date().toISOString()
    })
    .eq('id', requestId)
    .select()
    .single();

  if (error) {
    throw new Error(`Failed to update banner request: ${error.message}`);
  }

  return data;
}

export async function deleteBannerRequest(supabase: SupabaseClient, requestId: string): Promise<void> {
  const { error } = await supabase
    .from('banner_requests')
    .delete()
    .eq('id', requestId);

  if (error) {
    throw new Error(`Failed to delete banner request: ${error.message}`);
  }
}
