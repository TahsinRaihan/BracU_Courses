import type { SupabaseClient } from '@supabase/supabase-js';
import * as BannerRepository from '$lib/repositories/banner.repository';
import type { BannerRequest, CreateBannerRequestInput, UpdateBannerRequestInput, ActiveBanner } from '$lib/types/banner';

export class BannerService {
  constructor(private supabase: SupabaseClient) {}

  async getAllBannerRequests(): Promise<{ success: boolean; data?: BannerRequest[]; error?: string }> {
    try {
      const data = await BannerRepository.getAllBannerRequests(this.supabase);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async getPendingBannerRequests(): Promise<{ success: boolean; data?: BannerRequest[]; error?: string }> {
    try {
      const data = await BannerRepository.getPendingBannerRequests(this.supabase);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async getActiveBanners(): Promise<{ success: boolean; data?: ActiveBanner[]; error?: string }> {
    try {
      const data = await BannerRepository.getActiveBanners(this.supabase);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async createBannerRequest(userId: string, requestData: CreateBannerRequestInput): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    
    try {
      // Set duration based on the type - only set the relevant field
      let duration_days: number | null = null;
      let duration_hours: number | null = null;
      let duration_minutes: number | null = null;
      
      if (requestData.duration_type === 'minutes') {
        duration_minutes = requestData.duration_value;
      } else if (requestData.duration_type === 'hours') {
        duration_hours = requestData.duration_value;
      } else {
        duration_days = requestData.duration_value;
      }

      // Handle scheduled start date
      let scheduled_start_date: string | null = null;
      if (requestData.schedule_type === 'scheduled' && requestData.scheduled_date && requestData.scheduled_time) {
        // Convert local Bangladesh time to UTC
        const localDateTime = new Date(`${requestData.scheduled_date}T${requestData.scheduled_time}:00+06:00`);
        const utcDateTime = new Date(localDateTime.toISOString());
        scheduled_start_date = utcDateTime.toISOString();
      }

      const data = await BannerRepository.createBannerRequest(this.supabase, userId, {
        ...requestData,
        duration_days,
        duration_hours,
        duration_minutes,
        scheduled_start_date
      });
      
      return { success: true, data };
    } catch (error) {
      console.error('BannerService.createBannerRequest error:', error);
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async approveBannerRequest(requestId: string, adminUserId: string, adminNotes?: string): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    try {
      const request = await BannerRepository.getBannerRequestById(this.supabase, requestId);
      if (!request) {
        return { success: false, error: 'Banner request not found' };
      }

      let startDate: Date;
      let endDate: Date;
      
      // Determine start date based on schedule type
      if (request.schedule_type === 'scheduled' && request.scheduled_start_date) {
        // Use the scheduled start date for scheduled requests (already in UTC)
        startDate = new Date(request.scheduled_start_date);
      } else {
        // Start immediately for immediate requests
        startDate = new Date();
      }
      
      // Calculate end date based on duration type
      if (request.duration_minutes) {
        // Use minutes for precise timing
        endDate = new Date(startDate.getTime() + (request.duration_minutes * 60 * 1000));
      } else if (request.duration_hours) {
        // Use hours
        endDate = new Date(startDate.getTime() + (request.duration_hours * 60 * 60 * 1000));
      } else {
        // Use days
        endDate = new Date(startDate.getTime() + (request.duration_days * 24 * 60 * 60 * 1000));
      }

      const updates: UpdateBannerRequestInput = {
        status: 'approved',
        admin_notes: adminNotes,
        reviewed_by: adminUserId,
        reviewed_at: new Date().toISOString(),
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString()
      };

      const data = await BannerRepository.updateBannerRequest(this.supabase, requestId, updates);

      // Create notification for the user
      try {
        const { NotificationController } = await import('$lib/controllers/notification.controller');
        const notificationController = new NotificationController(this.supabase);
        
        const notificationMessage = request.schedule_type === 'scheduled' 
          ? `Your banner request "${request.title}" has been approved and will start displaying on ${startDate.toLocaleString('en-US', { timeZone: 'Asia/Dhaka' })}`
          : `Your banner request "${request.title}" has been approved and is now live!`;
        
        await notificationController.createNotification(request.user_id, {
          title: 'Banner Request Approved',
          message: notificationMessage,
          type: 'banner_request',
          action_url: '/myspace'
        });
      } catch (notificationError) {
        console.error('Failed to create notification:', notificationError);
        // Don't fail the approval if notification fails
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async rejectBannerRequest(requestId: string, adminUserId: string, adminNotes: string): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    try {
      const updates: UpdateBannerRequestInput = {
        status: 'rejected',
        admin_notes: adminNotes,
        reviewed_by: adminUserId,
        reviewed_at: new Date().toISOString()
      };

      const data = await BannerRepository.updateBannerRequest(this.supabase, requestId, updates);
      return { success: true, data };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  async deleteBannerRequest(requestId: string): Promise<{ success: boolean; error?: string }> {
    try {
      await BannerRepository.deleteBannerRequest(this.supabase, requestId);
      return { success: true };
    } catch (error) {
      return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }
}
