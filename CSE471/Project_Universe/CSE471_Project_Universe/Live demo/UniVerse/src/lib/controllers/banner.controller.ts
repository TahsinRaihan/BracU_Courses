import type { SupabaseClient } from '@supabase/supabase-js';
import { BannerService } from '$lib/services/banner.service';
import type { BannerRequest, CreateBannerRequestInput, ActiveBanner } from '$lib/types/banner';

export class BannerController {
  private bannerService: BannerService;

  constructor(supabase: SupabaseClient) {
    this.bannerService = new BannerService(supabase);
  }

  async getAllBannerRequests(): Promise<{ success: boolean; data?: BannerRequest[]; error?: string }> {
    return await this.bannerService.getAllBannerRequests();
  }

  async getPendingBannerRequests(): Promise<{ success: boolean; data?: BannerRequest[]; error?: string }> {
    return await this.bannerService.getPendingBannerRequests();
  }

  async getActiveBanners(): Promise<{ success: boolean; data?: ActiveBanner[]; error?: string }> {
    return await this.bannerService.getActiveBanners();
  }

  async createBannerRequest(userId: string, requestData: CreateBannerRequestInput): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    return await this.bannerService.createBannerRequest(userId, requestData);
  }

  async approveBannerRequest(requestId: string, adminUserId: string, adminNotes?: string): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    return await this.bannerService.approveBannerRequest(requestId, adminUserId, adminNotes);
  }

  async rejectBannerRequest(requestId: string, adminUserId: string, adminNotes: string): Promise<{ success: boolean; data?: BannerRequest; error?: string }> {
    return await this.bannerService.rejectBannerRequest(requestId, adminUserId, adminNotes);
  }

  async deleteBannerRequest(requestId: string): Promise<{ success: boolean; error?: string }> {
    return await this.bannerService.deleteBannerRequest(requestId);
  }
}
