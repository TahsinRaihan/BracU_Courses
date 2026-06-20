export type OrderItemRow = {
  quantity: number;
  menu_items: {
    name: string;
    price: number;
  };
};

export type Order = {
  id: number;
  user_id: string;
  created_at: string;
  scheduled_at: string | null;
  status: 'pending' | 'paid' | 'cancelled' | 'completed';
  order_items: OrderItemRow[];
};
