export type Favorite = {
  id: number;
  user_id: string;
  menu_item_id: number;
  created_at: string;
};

// When you join favorites → menu_items, use this DTO
export type FavoriteItem = {
  id: number; // favorite row id
  menu_item: {
    id: number;
    name: string;
    description: string;
    price: number;
    image_url?: string | null;
  }
};
