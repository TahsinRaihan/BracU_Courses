export type MenuItem = {
  id: number;
  name: string;
  description: string;
  price: number;
  category_id: number;
  image_url?: string | null;
  is_available: boolean;
  created_at?: string;
};
