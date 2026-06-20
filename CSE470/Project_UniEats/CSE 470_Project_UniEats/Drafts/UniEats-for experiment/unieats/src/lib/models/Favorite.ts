export type Favorite = {
  id: number;
  user_id: string;
  menu_item_id: number;
  created_at: string;
};


export type FavoriteItem = {
  id: number; 
  menu_item: {
    id: number;
    name: string;
    description: string;
    price: number;
    image_url?: string | null;
  }
};
