export type Review = {
  id: number;
  user_id: string;
  menu_item_id: number;
  rating: 1|2|3|4|5;
  comment?: string | null;
  created_at: string;
  user_nickname?: string; // optional denormalized field
};
