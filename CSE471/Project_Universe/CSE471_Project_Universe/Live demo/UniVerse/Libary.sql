
-- Books Table
CREATE TABLE public.books (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    published_year INTEGER,
    location VARCHAR(100) NOT NULL,
    image_url TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'borrowed', 'reserved')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Book Copies Table
CREATE TABLE public.book_copies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    book_id UUID NOT NULL REFERENCES public.books(id) ON DELETE CASCADE,
    status TEXT DEFAULT 'available' CHECK (status IN ('available', 'borrowed', 'reserved')),
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Book Reservations Table
CREATE TABLE public.book_reservations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES public.books(id) ON DELETE CASCADE,
    book_copy_id UUID REFERENCES public.book_copies(id) ON DELETE CASCADE,
    reservation_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expiry_date TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '7 days'),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled', 'fulfilled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, book_id, status)
);

-- Book Borrowings Table
CREATE TABLE public.book_borrowings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    book_copy_id UUID NOT NULL REFERENCES public.book_copies(id) ON DELETE CASCADE,
    borrow_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    due_date TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '14 days'),
    return_date TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'borrowed' CHECK (status IN ('borrowed', 'returned', 'overdue')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Book Reviews Table
CREATE TABLE public.book_reviews (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES public.books(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, book_id)
);




-- Library table indexes
CREATE INDEX IF NOT EXISTS idx_books_isbn ON public.books(isbn);
CREATE INDEX IF NOT EXISTS idx_books_title ON public.books(title);
CREATE INDEX IF NOT EXISTS idx_books_author ON public.books(author);
CREATE INDEX IF NOT EXISTS idx_books_category ON public.books(category);
CREATE INDEX IF NOT EXISTS idx_books_status ON public.books(status);
CREATE INDEX IF NOT EXISTS idx_book_copies_book_id ON public.book_copies(book_id);
CREATE INDEX IF NOT EXISTS idx_book_copies_status ON public.book_copies(status);
CREATE INDEX IF NOT EXISTS idx_book_reservations_user_id ON public.book_reservations(user_id);
CREATE INDEX IF NOT EXISTS idx_book_reservations_book_id ON public.book_reservations(book_id);
CREATE INDEX IF NOT EXISTS idx_book_reservations_status ON public.book_reservations(status);
CREATE INDEX IF NOT EXISTS idx_book_borrowings_user_id ON public.book_borrowings(user_id);
CREATE INDEX IF NOT EXISTS idx_book_borrowings_book_copy_id ON public.book_borrowings(book_copy_id);
CREATE INDEX IF NOT EXISTS idx_book_borrowings_status ON public.book_borrowings(status);
CREATE INDEX IF NOT EXISTS idx_book_reviews_user_id ON public.book_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_book_reviews_book_id ON public.book_reviews(book_id);


-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- =====================================================
-- STEP 6: CREATE LIBRARY MANAGEMENT FUNCTIONS
-- =====================================================

-- Function to reserve a book (only when no copies available)
CREATE OR REPLACE FUNCTION reserve_book_copy(
    p_user_id UUID,
    p_book_id UUID
)
RETURNS JSON AS $$
DECLARE
    available_copy_id UUID;
    reservation_id UUID;
    result JSON;
    earliest_return_date DATE;
    user_has_borrowing BOOLEAN;
BEGIN
    -- Check if any copies are currently available
    SELECT id INTO available_copy_id
    FROM public.book_copies 
    WHERE book_id = p_book_id 
      AND status = 'available' 
      AND is_available = true
    LIMIT 1;
    
    -- If copies are available, don't allow reservation
    IF available_copy_id IS NOT NULL THEN
        result := json_build_object(
            'success', false,
            'error', 'Cannot reserve book when copies are available. Please borrow the book instead.'
        );
        RETURN result;
    END IF;
    
    -- Check if user already has an active borrowing for this book
    SELECT EXISTS (
        SELECT 1 FROM public.book_borrowings bb
        JOIN public.book_copies bc ON bb.book_copy_id = bc.id
        WHERE bb.user_id = p_user_id 
          AND bc.book_id = p_book_id 
          AND bb.status = 'borrowed'
    ) INTO user_has_borrowing;
    
    -- If user has borrowed this book, don't allow reservation
    IF user_has_borrowing THEN
        result := json_build_object(
            'success', false,
            'error', 'You cannot reserve a book you have already borrowed. Please return it first if you want to reserve it again.'
        );
        RETURN result;
    END IF;
    
    -- Check if user already has an active reservation for this book
    IF EXISTS (
        SELECT 1 FROM public.book_reservations 
        WHERE user_id = p_user_id 
          AND book_id = p_book_id 
          AND status = 'active'
    ) THEN
        result := json_build_object(
            'success', false,
            'error', 'You already have an active reservation for this book'
        );
        RETURN result;
    END IF;
    
    -- Find the earliest date when a copy will be available
    SELECT MIN(due_date) INTO earliest_return_date
    FROM public.book_borrowings bb
    JOIN public.book_copies bc ON bb.book_copy_id = bc.id
    WHERE bc.book_id = p_book_id 
      AND bb.status = 'borrowed';
    
    -- Create the reservation
    INSERT INTO public.book_reservations (user_id, book_id, status, reservation_date, expiry_date)
    VALUES (p_user_id, p_book_id, 'active', NOW(), NOW() + INTERVAL '7 days')
    RETURNING id INTO reservation_id;
    
    result := json_build_object(
        'success', true,
        'message', 'Book reserved successfully. You will be notified when a copy becomes available.',
        'reservation_id', reservation_id,
        'expiry_date', NOW() + INTERVAL '7 days',
        'earliest_availability', earliest_return_date
    );
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to borrow a book
CREATE OR REPLACE FUNCTION borrow_book_copy(
    p_user_id UUID,
    p_book_id UUID
)
RETURNS JSON AS $$
DECLARE
    available_copy_id UUID;
    borrowing_id UUID;
    result JSON;
    user_has_reservation BOOLEAN;
BEGIN
    -- Find an available copy of the book
    SELECT id INTO available_copy_id
    FROM public.book_copies 
    WHERE book_id = p_book_id 
      AND status = 'available' 
      AND is_available = true
    LIMIT 1;
    
    -- Check if copy is available
    IF available_copy_id IS NULL THEN
        result := json_build_object(
            'success', false,
            'error', 'No available copies of this book'
        );
        RETURN result;
    END IF;
    
    -- Check if user already has an active borrowing for this book
    IF EXISTS (
        SELECT 1 FROM public.book_borrowings bb
        JOIN public.book_copies bc ON bb.book_copy_id = bc.id
        WHERE bb.user_id = p_user_id 
          AND bc.book_id = p_book_id 
          AND bb.status = 'borrowed'
    ) THEN
        result := json_build_object(
            'success', false,
            'error', 'You already have borrowed this book'
        );
        RETURN result;
    END IF;
    
    -- Check if user has an active reservation for this book
    SELECT EXISTS (
        SELECT 1 FROM public.book_reservations 
        WHERE user_id = p_user_id 
          AND book_id = p_book_id 
          AND status = 'active'
    ) INTO user_has_reservation;
    
    -- If user has a reservation, automatically cancel it when borrowing
    IF user_has_reservation THEN
        UPDATE public.book_reservations 
        SET status = 'fulfilled', updated_at = NOW()
        WHERE user_id = p_user_id 
          AND book_id = p_book_id 
          AND status = 'active';
    END IF;
    
    -- Create the borrowing
    INSERT INTO public.book_borrowings (user_id, book_copy_id)
    VALUES (p_user_id, available_copy_id)
    RETURNING id INTO borrowing_id;
    
    -- Update the book copy status to borrowed
    UPDATE public.book_copies 
    SET status = 'borrowed', is_available = false, updated_at = NOW()
    WHERE id = available_copy_id;
    
    result := json_build_object(
        'success', true,
        'message', CASE 
            WHEN user_has_reservation THEN 'Book borrowed successfully! Your reservation has been automatically fulfilled.'
            ELSE 'Book borrowed successfully'
        END,
        'borrowing_id', borrowing_id,
        'due_date', NOW() + INTERVAL '14 days',
        'reservation_fulfilled', user_has_reservation
    );
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to return a book
CREATE OR REPLACE FUNCTION return_book_copy(
    p_user_id UUID,
    p_book_id UUID
)
RETURNS JSON AS $$
DECLARE
    borrowing_record RECORD;
    result JSON;
BEGIN
    -- Find the user's active borrowing for this book
    SELECT bb.id, bb.book_copy_id INTO borrowing_record
    FROM public.book_borrowings bb
    JOIN public.book_copies bc ON bb.book_copy_id = bc.id
    WHERE bb.user_id = p_user_id 
      AND bc.book_id = p_book_id 
      AND bb.status = 'borrowed';
    
    -- Check if borrowing exists
    IF borrowing_record.id IS NULL THEN
        result := json_build_object(
            'success', false,
            'error', 'No active borrowing found for this book'
        );
        RETURN result;
    END IF;
    
    -- Update the borrowing to returned
    UPDATE public.book_borrowings 
    SET status = 'returned', return_date = NOW(), updated_at = NOW()
    WHERE id = borrowing_record.id;
    
    -- Update the book copy status back to available
    UPDATE public.book_copies 
    SET status = 'available', is_available = true, updated_at = NOW()
    WHERE id = borrowing_record.book_copy_id;
    
    result := json_build_object(
        'success', true,
        'message', 'Book returned successfully'
    );
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;
-- =====================================================
-- STEP 7: CREATE TRIGGERS
-- =====================================================





DROP TRIGGER IF EXISTS update_books_updated_at ON public.books;
DROP TRIGGER IF EXISTS update_book_copies_updated_at ON public.book_copies;
DROP TRIGGER IF EXISTS update_book_reservations_updated_at ON public.book_reservations;
DROP TRIGGER IF EXISTS update_book_borrowings_updated_at ON public.book_borrowings;
DROP TRIGGER IF EXISTS update_book_reviews_updated_at ON public.book_reviews;

-- Updated timestamp triggers

CREATE TRIGGER update_books_updated_at 
    BEFORE UPDATE ON public.books 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_copies_updated_at 
    BEFORE UPDATE ON public.book_copies 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_reservations_updated_at 
    BEFORE UPDATE ON public.book_reservations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_borrowings_updated_at 
    BEFORE UPDATE ON public.book_borrowings 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_book_reviews_updated_at 
    BEFORE UPDATE ON public.book_reviews 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();



-- Books policies
DROP POLICY IF EXISTS "Books are public" ON public.books;
DROP POLICY IF EXISTS "books_select_public" ON public.books;
DROP POLICY IF EXISTS "books_select_own" ON public.books;
DROP POLICY IF EXISTS "books_insert_own" ON public.books;
DROP POLICY IF EXISTS "books_update_own" ON public.books;

-- Book copies policies
DROP POLICY IF EXISTS "Book copies are public" ON public.book_copies;
DROP POLICY IF EXISTS "book_copies_select_public" ON public.book_copies;
DROP POLICY IF EXISTS "book_copies_select_own" ON public.book_copies;
DROP POLICY IF EXISTS "book_copies_insert_own" ON public.book_copies;
DROP POLICY IF EXISTS "book_copies_update_own" ON public.book_copies;

-- Book reservations policies
DROP POLICY IF EXISTS "Users can view own reservations" ON public.book_reservations;
DROP POLICY IF EXISTS "book_reservations_select_own" ON public.book_reservations;
DROP POLICY IF EXISTS "book_reservations_insert_own" ON public.book_reservations;
DROP POLICY IF EXISTS "book_reservations_update_own" ON public.book_reservations;
DROP POLICY IF EXISTS "book_reservations_delete_own" ON public.book_reservations;

-- Book borrowings policies
DROP POLICY IF EXISTS "Users can view own borrowings" ON public.book_borrowings;
DROP POLICY IF EXISTS "book_borrowings_select_own" ON public.book_borrowings;
DROP POLICY IF EXISTS "book_borrowings_insert_own" ON public.book_borrowings;
DROP POLICY IF EXISTS "book_borrowings_update_own" ON public.book_borrowings;
DROP POLICY IF EXISTS "book_borrowings_delete_own" ON public.book_borrowings;

-- Book reviews policies
DROP POLICY IF EXISTS "Book reviews are public" ON public.book_reviews;
DROP POLICY IF EXISTS "book_reviews_select_own" ON public.book_reviews;
DROP POLICY IF EXISTS "book_reviews_insert_own" ON public.book_reviews;
DROP POLICY IF EXISTS "book_reviews_update_own" ON public.book_reviews;
DROP POLICY IF EXISTS "book_reviews_delete_own" ON public.book_reviews;



-- Create library policies
CREATE POLICY "Books are public" ON public.books
  FOR SELECT USING (true);

CREATE POLICY "Book copies are public" ON public.book_copies
  FOR SELECT USING (true);

CREATE POLICY "Users can view own reservations" ON public.book_reservations
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own borrowings" ON public.book_borrowings
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Book reviews are public" ON public.book_reviews
  FOR SELECT USING (true);



-- Grant execute permissions on functions
GRANT EXECUTE ON FUNCTION public.reserve_book_copy(UUID, UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION public.borrow_book_copy(UUID, UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION public.return_book_copy(UUID, UUID) TO authenticated;


-- Grant table permissions

GRANT ALL ON public.books TO authenticated;
GRANT ALL ON public.book_copies TO authenticated;
GRANT ALL ON public.book_reservations TO authenticated;
GRANT ALL ON public.book_borrowings TO authenticated;
GRANT ALL ON public.book_reviews TO authenticated;





-- =====================================================
-- STEP 10: INSERT SAMPLE DATA
-- =====================================================

-- Insert sample books
INSERT INTO public.books (title, author, isbn, category, published_year, location, image_url) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0743273565', 'Fiction', 1925, 'Shelf A1', 'https://example.com/gatsby.jpg'),
('To Kill a Mockingbird', 'Harper Lee', '978-0446310789', 'Fiction', 1960, 'Shelf A2', 'https://example.com/mockingbird.jpg'),
('1984', 'George Orwell', '978-0451524935', 'Fiction', 1949, 'Shelf A3', 'https://example.com/1984.jpg'),
('Pride and Prejudice', 'Jane Austen', '978-0141439518', 'Fiction', 1813, 'Shelf A4', 'https://example.com/pride.jpg'),
('The Hobbit', 'J.R.R. Tolkien', '978-0547928241', 'Fantasy', 1937, 'Shelf B1', 'https://example.com/hobbit.jpg')
ON CONFLICT (isbn) DO NOTHING;

-- Insert sample book copies
INSERT INTO public.book_copies (book_id) 
SELECT id FROM public.books
ON CONFLICT DO NOTHING;





-- Check library data
SELECT 'Sample books added' as status, COUNT(*) as book_count FROM public.books;
SELECT 'Sample copies added' as status, COUNT(*) as copy_count FROM public.book_copies;  