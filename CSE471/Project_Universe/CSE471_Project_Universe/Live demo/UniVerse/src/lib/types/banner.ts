export interface BannerRequest {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  image_url: string | null;
  target_url: string | null;
  admin_notes: string | null;
  reviewed_by: string | null;
  reviewed_at: string | null;
  start_date: string | null;
  end_date: string | null;
  duration_days: number;
  duration_hours: number | null;
  duration_minutes: number | null;
  schedule_type: 'immediate' | 'scheduled';
  scheduled_start_date: string | null;
  status: 'pending' | 'approved' | 'rejected' | 'expired';
  created_at: string;
  updated_at: string;
  user?: {
    id: string;
    email: string;
    profiles: {
      display_name: string | null;
      nickname: string | null;
      student_id: string | null;
    };
  };
}

export interface ActiveBanner {
  title: string;
  description: string | null;
}

export interface CreateBannerRequestInput {
  title: string;
  description?: string;
  duration_type: 'minutes' | 'hours' | 'days';
  duration_value: number;
  schedule_type: 'immediate' | 'scheduled';
  scheduled_date?: string;
  scheduled_time?: string;
}

export interface UpdateBannerRequestInput {
  status?: 'pending' | 'approved' | 'rejected' | 'expired';
  admin_notes?: string;
  start_date?: string;
  end_date?: string;
  reviewed_by?: string;
  reviewed_at?: string;
}
