export type Inventory = {
  id: number;
  menu_item_id: number;
  in_stock: boolean;
  quantity?: number | null;      
  updated_at?: string;
};
