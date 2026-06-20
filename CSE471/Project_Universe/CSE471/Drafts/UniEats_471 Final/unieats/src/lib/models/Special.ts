import type { MenuItem } from './MenuItem';

export type SpecialType = 'daily' | 'weekly' | 'offer';

export type Special = {
  id: number;
  menu_item_id: number;
  type: SpecialType;
  starts_on?: string | null;
  ends_on?: string | null;
  created_at?: string;
  menu_item?: MenuItem; 
};
